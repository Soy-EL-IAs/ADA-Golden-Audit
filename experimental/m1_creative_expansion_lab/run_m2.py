#!/usr/bin/env python3
"""Run M2 fast, text-only Creative Expansion without invoking the image pipeline."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

if __package__:
    from .run_m1 import (
        ADA_ROOT,
        EXPECTED_COUNT,
        ExperimentError,
        LMStudioController,
        CharacterProfileDatabase,
        build_prompts,
        build_compact_prompts,
        concept_text,
        execute_once,
        chat_completion_content,
        http_json,
        native_content,
        native_payload,
        parse_json_object,
        _normalize_json_controls,
        structured_concept_payload,
        source_context,
        telemetry,
        temporal_leakage,
        utc_now,
        validate_structure,
        write_json_new,
    )
else:
    from run_m1 import (
        ADA_ROOT,
        EXPECTED_COUNT,
        ExperimentError,
        LMStudioController,
        CharacterProfileDatabase,
        build_prompts,
        build_compact_prompts,
        concept_text,
        execute_once,
        chat_completion_content,
        http_json,
        native_content,
        native_payload,
        parse_json_object,
        _normalize_json_controls,
        structured_concept_payload,
        source_context,
        telemetry,
        temporal_leakage,
        utc_now,
        validate_structure,
        write_json_new,
    )


if str(ADA_ROOT) not in sys.path:
    sys.path.insert(0, str(ADA_ROOT))
from scripts.ada_paths import MISSION_RUNS_ROOT


LAB_ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = LAB_ROOT / "m2_config.json"
RUNS_ROOT = MISSION_RUNS_ROOT


class CreativeOutputTruncated(ExperimentError):
    """The one allowed creative response exhausted its configured token budget."""


def creative_output_token_budget(requested_count: int, transport: dict[str, Any]) -> int:
    """Apply the documented per-concept policy without exceeding config.

    A specialist may use less than its configured ceiling only through this
    explicit policy.  There is intentionally no hidden local hard cap.
    """
    configured_max = int(transport["max_output_tokens"])
    tokens_per_concept = int(transport["output_tokens_per_concept"])
    minimum = int(transport["minimum_output_tokens"])
    if requested_count < 1 or configured_max < 1 or tokens_per_concept < 1 or minimum < 1:
        raise ExperimentError("M2 token-budget values must be positive integers")
    return min(configured_max, max(minimum, requested_count * tokens_per_concept))


def response_reached_token_limit(response: dict[str, Any], budget: int) -> tuple[bool, int | None]:
    """Return explicit native-transport truncation evidence when available."""
    stats = response.get("stats", {}) if isinstance(response, dict) else {}
    actual = stats.get("total_output_tokens") if isinstance(stats, dict) else None
    try:
        actual_tokens = int(actual)
    except (TypeError, ValueError):
        return False, None
    return actual_tokens >= budget, actual_tokens


def parse_and_validate_creative_response(
    response: dict[str, Any], *, budget: int, character: str,
) -> dict[str, Any]:
    """Parse the single creative response and distinguish truncation cleanly."""
    try:
        parsed = parse_compact_concepts(native_content(response))
        validate_structure(parsed, character=character)
        return parsed
    except ExperimentError as exc:
        reached_limit, actual_tokens = response_reached_token_limit(response, budget)
        if reached_limit:
            raise CreativeOutputTruncated(
                "M1→M2 creative output was truncated at its configured budget: "
                f"{actual_tokens}/{budget} output tokens; no creative retry was attempted"
            ) from exc
        raise


def without_reasoning_content(value: Any) -> Any:
    """Keep operational receipts useful without storing model chain-of-thought."""
    if isinstance(value, dict):
        return {key: without_reasoning_content(item) for key, item in value.items() if key not in {"reasoning_content", "reasoning"}}
    if isinstance(value, list):
        return [without_reasoning_content(item) for item in value]
    return value


def parse_compact_concepts(content: str) -> dict[str, Any]:
    """Normalize the two bounded shapes LM Studio may emit at M1→M2."""
    text = content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else ""
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
    try:
        value, _ = json.JSONDecoder().raw_decode(_normalize_json_controls(text.lstrip()))
    except json.JSONDecodeError as exc:
        raise ExperimentError(f"M1→M2 response is not valid JSON after control-character normalization: {exc}") from exc
    if isinstance(value, list):
        return {"concepts": value}
    if isinstance(value, dict) and isinstance(value.get("concepts"), list):
        return {"concepts": value["concepts"]}
    if isinstance(value, dict) and value and all(
        isinstance(key, str)
        and isinstance(item, dict)
        and item.get("concept_id") == key
        for key, item in value.items()
    ):
        return {"concepts": list(value.values())}
    raise ExperimentError(
        "M1→M2 response must be a concepts array, an object containing concepts, "
        "or an object keyed by matching concept_id values"
    )


def load_config(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ExperimentError(f"Invalid M2 config: {path}") from exc
    if not isinstance(value, dict):
        raise ExperimentError("M2 config must be an object")
    for key in ("creative_expansion_model", "strong_evaluation_model", "character", "version", "native_transport", "execution"):
        if key not in value:
            raise ExperimentError(f"M2 config is missing {key}")
    if value["creative_expansion_model"] == value["strong_evaluation_model"]:
        raise ExperimentError("M2 fast and strong models must be different")
    if value.get("requested_count") is None:
        value["requested_count"] = 12
    if value["native_transport"].get("reasoning") != "off":
        raise ExperimentError("M2 native transport must force reasoning: off")
    for key in ("max_output_tokens", "output_tokens_per_concept", "minimum_output_tokens"):
        if key not in value["native_transport"]:
            raise ExperimentError(f"M2 native transport is missing explicit token-budget policy {key}")
    if value["execution"].get("creative_calls") != 1 or value["execution"].get("creative_retries") != 0:
        raise ExperimentError("M2 permits exactly one creative call and no retries")
    if value["execution"].get("rendering_enabled") is not False or value["execution"].get("selection_enabled") is not False:
        raise ExperimentError("M2 must remain text-only with no selection")
    return value


def loaded_instances(inventory: dict[str, Any], model: str) -> list[dict[str, Any]]:
    models = inventory.get("models", [])
    if not isinstance(models, list):
        return []
    for item in models:
        if isinstance(item, dict) and item.get("key") == model:
            return [instance for instance in item.get("loaded_instances", []) if isinstance(instance, dict)]
    return []


def supports_reasoning_parameter(inventory: dict[str, Any], model: str) -> bool:
    models = inventory.get("models", [])
    if not isinstance(models, list):
        return False
    for item in models:
        if not isinstance(item, dict) or item.get("key") != model:
            continue
        capabilities = item.get("capabilities", {})
        reasoning = capabilities.get("reasoning", {}) if isinstance(capabilities, dict) else {}
        return isinstance(reasoning, dict) and "off" in reasoning.get("allowed_options", [])
    return False


def preflight(base_url: str, config: dict[str, Any], profile: dict[str, Any], guide_manifest: dict[str, Any]) -> dict[str, Any]:
    if profile.get("character_profile_used") is not True or profile.get("version_match") is not True:
        raise ExperimentError("M2 requires a resolved, version-matched character profile")
    if len(guide_manifest.get("routed_sources", [])) != 4:
        raise ExperimentError("M2 guide routing is incomplete")
    inventory = http_json(f"{base_url}/api/v1/models")
    fast_instances = loaded_instances(inventory, config["creative_expansion_model"])
    if not fast_instances:
        raise ExperimentError(f"M2 fast model is not loaded: {config['creative_expansion_model']}")
    strong_instances = loaded_instances(inventory, config["strong_evaluation_model"])
    if strong_instances:
        raise ExperimentError(
            f"M2 must not load the strong model without an explicit escalation: {config['strong_evaluation_model']}"
        )
    active_config = fast_instances[0].get("config", {})
    actual_context = active_config.get("context_length") if isinstance(active_config, dict) else None
    if actual_context != config["context_length"]:
        raise ExperimentError(
            f"Fast model context is {actual_context}; M2 requires configured context {config['context_length']}"
        )
    return {
        "passed": True,
        "checked_at": utc_now(),
        "native_endpoint": config["native_transport"]["endpoint"],
        "creative_expansion_model": config["creative_expansion_model"],
        "strong_evaluation_model": config["strong_evaluation_model"],
        "strong_model_loaded": False,
        "loaded_context_length": actual_context,
        "reasoning_parameter_supported": supports_reasoning_parameter(inventory, config["creative_expansion_model"]),
        "character_profile_resolved": True,
        "guide_source_count": len(guide_manifest["routed_sources"]),
        "creative_calls_planned": 1,
        "comfyui_calls_planned": 0,
        "selection_enabled": False,
    }


def proposal_records(value: dict[str, Any], *, character: str, model: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for concept in value["concepts"]:
        findings = temporal_leakage({"concepts": [concept]})
        records.append({
            "concept_id": concept["concept_id"],
            "character": character,
            "source_model": model,
            "status": "FAIL" if findings else "PASS",
            "fail_reasons": findings,
            "hook": concept.get("hook", concept.get("visual_hook", "")),
            "composition": concept.get("camera", concept.get("composition_intent", "")),
            "mechanism": concept.get("action", concept.get("provocative_mechanism", "")),
            "proposal": concept,
        })
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()

    config_path = args.config.resolve()
    config = load_config(config_path)
    run_id = args.run_id or f"m2_{re.sub(r'[^a-z0-9]+', '_', str(config['character']).casefold()).strip('_') or 'character'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", run_id):
        raise ExperimentError("run-id must be a safe 1-80 character identifier")
    run_dir = RUNS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    started_at = utc_now()

    try:
        # Initialization is part of the run contract.  Keeping it inside this
        # boundary ensures a failed Mission always has a durable failure.json.
        profile = CharacterProfileDatabase().get_character_profile(config["character"], config["version"])
        guide_context, guide_manifest = source_context()
        controller = LMStudioController()
        user_intent = config.get("creative_intent", {}) if isinstance(config.get("creative_intent"), dict) else {}
        generation_context = config.get("generation_context", {})
        generation_mode = generation_context.get("mode", "direct")
        system, task = build_compact_prompts(config["character"], config["version"], profile, user_intent, generation_mode)

        write_json_new(run_dir / "m2_config_snapshot.json", config)
        write_json_new(run_dir / "character_profile.json", profile)
        write_json_new(run_dir / "guide_context.json", {"manifest": guide_manifest, "excerpts": guide_context})
        preflight_result = preflight(controller.base_url, config, profile, guide_manifest)
        write_json_new(run_dir / "preflight.json", preflight_result)
        transport = config["native_transport"]
        reasoning_parameter = transport["reasoning"] if preflight_result["reasoning_parameter_supported"] else None
        output_token_budget = creative_output_token_budget(int(config["requested_count"]), transport)
        # The capability preflight refers to LM Studio's native endpoint.
        # Use that same endpoint: its reasoning=off flag controls this model,
        # unlike the OpenAI-compatible route which emitted reasoning only.
        request = native_payload(
            config["creative_expansion_model"],
            system + "\n\n" + task,
            temperature=float(transport["temperature"]),
            max_output_tokens=output_token_budget,
            reasoning=reasoning_parameter,
        )
        write_json_new(run_dir / "model_request.json", request)
        raw, latency = execute_once(controller.base_url, request, endpoint=transport["endpoint"])
        write_json_new(run_dir / "raw_model_response.json", without_reasoning_content(raw))
        parsed = parse_and_validate_creative_response(
            raw, budget=output_token_budget, character=config["character"],
        )
        write_json_new(run_dir / "concept_proposals_raw.json", parsed)
        records = proposal_records(parsed, character=config["character"], model=config["creative_expansion_model"])
        valid_count = sum(record["status"] == "PASS" for record in records)
        rejected_count = len(records) - valid_count
        write_json_new(run_dir / "proposal_records.json", {
            "requested_count": config["requested_count"],
            "output_token_budget": output_token_budget,
            "valid_count": valid_count,
            "semantic_guard_rejected_count": rejected_count,
            "selection_performed": False,
            "records": records,
        })
        run_telemetry = telemetry(raw, latency)
        run_telemetry.update({
            "creative_expansion_model": config["creative_expansion_model"],
            "strong_evaluation_model": config["strong_evaluation_model"],
            "reasoning_policy": transport["reasoning"],
            "reasoning_parameter_sent": reasoning_parameter is not None,
            "requested_count": config["requested_count"],
            "valid_count": valid_count,
            "semantic_guard_rejected_count": rejected_count,
            "retries": 0,
            "fallbacks": 0,
        })
        write_json_new(run_dir / "telemetry.json", run_telemetry)
        write_json_new(run_dir / "report.json", {
            "status": "COMPLETE_TEXT_ONLY",
            "creative_expansion_model": config["creative_expansion_model"],
            "requested_count": config["requested_count"],
            "valid_count": valid_count,
            "semantic_guard_rejected_count": rejected_count,
            "selection_performed": False,
            "rendering_performed": False,
            "comfyui_executed": False,
            "minimax_executed": False,
            "telemetry": run_telemetry,
        })
        write_json_new(run_dir / "manifest.json", {
            "experiment": config["experiment"],
            "status": "COMPLETE_TEXT_ONLY",
            "started_at": started_at,
            "completed_at": utc_now(),
            "creative_expansion_model": config["creative_expansion_model"],
            "strong_evaluation_model": config["strong_evaluation_model"],
            "strong_model_loaded": False,
            "creative_calls": 1,
            "creative_retries": 0,
            "creative_fallbacks": 0,
            "selection_performed": False,
            "rendering_performed": False,
            "comfyui_executed": False,
            "artifacts": {path.stem: str(path.resolve()) for path in sorted(run_dir.iterdir())},
        })
    except Exception as exc:
        write_json_new(run_dir / "failure.json", {
            "experiment": config["experiment"],
            "status": "STOPPED",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "started_at": started_at,
            "stopped_at": utc_now(),
            "creative_calls_at_most": 1,
            "creative_retries": 0,
            "creative_fallbacks": 0,
            "comfyui_executed": False,
        })
        raise

    print(json.dumps({"status": "COMPLETE_TEXT_ONLY", "run_dir": str(run_dir.resolve())}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"M2 stopped: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
