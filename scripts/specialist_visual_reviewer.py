#!/usr/bin/env python3
"""Illustrious/Klein boundary review using ADA's versioned visual contract."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

from scripts.ada_paths import ADA_ROOT
from scripts.character_reference_manifest import load_character_reference_manifest

if __package__:
    from .agent_contracts import ContractError, response_format, validate_contract
    from .visual_reviewer import _content_text, _native_content_text, _parse_json_object, _request, _save_diagnostic, image_data_url
else:
    from agent_contracts import ContractError, response_format, validate_contract
    from visual_reviewer import _content_text, _native_content_text, _parse_json_object, _request, _save_diagnostic, image_data_url


class VisualReviewTransportError(RuntimeError):
    """No valid VisualReview crossed the mandatory boundary."""


RUNTIME_INSTRUCTION = (Path(__file__).resolve().parents[1] / "config" / "runtime_instructions" / "visual_review_runtime_v2.md").read_text(encoding="utf-8").strip()

IDENTITY_FAILURE_RATING_CAP = 4.0
SUBJECT_COUNT_FAILURE_RATING_CAP = 4.5
HARD_CONSTRAINT_RATING_CAP = 5.0
COMPACT_REVIEW_LIMITS_INSTRUCTION = (
    "Keep candidate_observations, reference_observations, and identity_comparison under 50 words each; "
    "keep outfit_design_adherence under 35 words and summary under 30 words. "
    "Return at most 6 defects and 6 hard_constraint_failures, each under 18 words. "
    "State each observation once; never repeat or pad phrases."
)


def canonical_reference_paths(semantic_spec: dict[str, Any], character_contract: dict[str, Any] | None = None, limit: int = 2) -> list[Path]:
    """Resolve only canonical ADA references; generated references are excluded."""
    contract = character_contract if isinstance(character_contract, dict) else {}
    if not contract:
        contract = semantic_spec.get("character_contract", {}) if isinstance(semantic_spec.get("character_contract"), dict) else {}
    manifest_ref = ""
    for evidence in contract.get("evidence", []) if isinstance(contract.get("evidence"), list) else []:
        if isinstance(evidence, dict) and evidence.get("source") == "character_refs_manifest":
            manifest_ref = str(evidence.get("reference", "")).strip()
            break
    if not manifest_ref:
        profile = contract.get("source_profile", {}) if isinstance(contract.get("source_profile"), dict) else {}
        manifest_ref = str(profile.get("refs_manifest", "")).strip()
    if not manifest_ref:
        # Production specs normally carry the Character Contract separately.
        manifest_ref = str(semantic_spec.get("character_refs_manifest", "")).strip()
    if not manifest_ref:
        return []
    manifest_path = Path(manifest_ref)
    if not manifest_path.is_absolute():
        manifest_path = ADA_ROOT / manifest_path
    try:
        manifest = load_character_reference_manifest(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError):
        return []
    refs = manifest["canonical_references"]
    root = manifest_path.parent.resolve()
    result: list[Path] = []
    for item in refs:
        relative = Path(str(item.get("file", ""))) if isinstance(item, dict) else Path()
        if relative.is_absolute() or ".." in relative.parts:
            continue
        candidate = (root / relative).resolve()
        if candidate.is_relative_to(root) and candidate.is_file():
            result.append(candidate)
        if len(result) >= limit:
            break
    return result


def _ground_review_claims(items: list[str], *, semantic_spec: dict[str, Any]) -> list[str]:
    """Discard a review claim that contradicts the contract rather than pixels.

    Vision models occasionally invent an expected colour (for example, `red eyes`)
    even though the contract supplied a different explicit cue.  Such a claim must
    not reject a correct render.  Real mismatches remain intact and are still
    subject to the identity/rating cap below.
    """
    character = semantic_spec.get("character", {}) if isinstance(semantic_spec, dict) else {}
    cues = [str(item).casefold().replace("_", " ") for item in character.get("must_preserve", [])]
    expected = {(match.group("feature").rstrip("s"), match.group("colour"))
                for cue in cues
                for match in [re.fullmatch(r"(?P<colour>[a-z]+) (?P<feature>eyes?|hair)", cue)]
                if match}
    kept: list[str] = []
    for item in items:
        claim = str(item)
        assertions = re.findall(r"(?:expected|required|specified)\s+([a-z]+)[ _-](eyes?|hair)", claim.casefold())
        if assertions and any((feature.rstrip("s"), colour) not in expected for colour, feature in assertions):
            continue
        kept.append(claim)
    return kept


def _rated_review(value: dict[str, Any], *, identifier: str, stage: str, semantic_spec: dict[str, Any] | None = None) -> dict[str, Any]:
    """Code owns the aggregate rating and conservative hard-failure caps."""
    validate_contract("visual_review_v3", value)
    if value["id"] != identifier or value["stage"] != stage:
        raise ValueError("Visual specialist changed the requested id or stage")
    scores = {name: float(score) for name, score in value["scores"].items()}
    rating = min(9.5, round(scores["identity"] * .25 + scores["anatomy"] * .25 + scores["prompt_adherence"] * .20 + scores["composition"] * .15 + scores["visual_quality"] * .15, 1))
    spec = semantic_spec if isinstance(semantic_spec, dict) else {}
    identity_failures = _ground_review_claims(value.get("identity_failures", []), semantic_spec=spec)
    defects = _ground_review_claims(value["defects"], semantic_spec=spec)
    hard_constraint_failures = _ground_review_claims(value["hard_constraint_failures"], semantic_spec=spec)
    text = " ".join(identity_failures + defects + hard_constraint_failures).casefold()
    normalized_text = text.replace("_", " ").replace("-", " ")
    character = semantic_spec.get("character", {}) if isinstance(semantic_spec, dict) else {}
    visible = set(semantic_spec.get("expected_visibility", [])) if isinstance(semantic_spec, dict) else set()
    cues = [str(item).casefold().replace("_", " ").replace("-", " ") for item in character.get("must_preserve", []) if item in visible]
    contradiction = any(marker in normalized_text for marker in ("not visible", "not visibly", "missing", "wrong", "contradict", "does not match", "appears light"))
    cue_contradiction = contradiction and any(cue in normalized_text for cue in cues if len(cue) >= 4)
    if cue_contradiction and not identity_failures:
        identity_failures = [defect for defect in defects if any(cue in defect.casefold().replace("_", " ").replace("-", " ") for cue in cues)] or ["Visible identity cue contradicted by review evidence"]
    verdict = value["verdict"]
    if scores["anatomy"] <= 4 or any(marker in text for marker in ("extra hand", "extra limb", "missing limb", "critical anatomy")):
        rating, verdict = min(rating, 5.5), "FAIL"
    elif identity_failures or scores["identity"] <= 4 or ("identity" in text and ("missing" in text or "wrong" in text)):
        rating, verdict = min(rating, 5.5), "FAIL"
    elif hard_constraint_failures:
        rating = min(rating, 6.0)
    return {**value, "identity_failures": identity_failures, "defects": defects, "hard_constraint_failures": hard_constraint_failures, "verdict": verdict, "agent_scores": scores, "agent_rating": rating}


def _rated_grounded_review(value: dict[str, Any], *, identifier: str, stage: str, semantic_spec: dict[str, Any], reference_count: int = 0) -> dict[str, Any]:
    """Code owns verdict/rating; identity and subject count are hard gates."""
    validate_contract("visual_review_v4", value)
    if value["id"] != identifier or value["stage"] != stage:
        raise ValueError("Visual specialist changed the requested id or stage")
    expected = int(semantic_spec.get("expected_subject_count", 1) or 1)
    if value["subject_count"]["expected"] != expected:
        raise ValueError("Visual specialist changed expected_subject_count")
    actual = value["subject_count"]["actual"]
    visible_extra_subject_claim = bool(re.search(
        r"\b(with|beside|facing)\s+(a|another|the)\s+(friend|person|companion|woman|man|girl|boy)\b|\b(second|another)\s+(person|subject|woman|man|girl|boy)\b|\btwo\s+(people|persons|subjects|women|men|girls|boys)\b",
        " ".join([str(value.get("summary", "")), *[str(item) for item in value.get("defects", [])], *[str(item) for item in value.get("hard_constraint_failures", [])]]),
        flags=re.IGNORECASE,
    ))
    if expected == 1 and actual == 1 and visible_extra_subject_claim:
        actual = 2
    subject_result = "PASS" if actual == expected else "FAIL"
    identity = dict(value["identity"])
    scores = {"identity": float(identity["score"]), **{name: float(score) for name, score in value["scores"].items()}}
    rating = min(9.5, round(
        scores["identity"] * .30 + scores["anatomy"] * .20 + scores["prompt_adherence"] * .20
        + scores["composition"] * .15 + scores["visual_quality"] * .15,
        1,
    ))
    defects = _ground_review_claims(value.get("defects", []), semantic_spec=semantic_spec)
    hard_failures = _ground_review_claims(value.get("hard_constraint_failures", []), semantic_spec=semantic_spec)
    identity_failures: list[str] = []
    verdict = "MINOR_DEFECT" if defects else "PASS"
    applied_caps: list[dict[str, Any]] = []
    if identity["result"] == "FAIL":
        identity_failures = ["Generated protagonist does not match ADA canonical character references"]
        verdict = "FAIL"
        rating = min(rating, IDENTITY_FAILURE_RATING_CAP)
        applied_caps.append({"reason": "identity_fail", "cap": IDENTITY_FAILURE_RATING_CAP})
    elif identity["result"] == "UNCERTAIN":
        verdict = "HUMAN_REVIEW_REQUIRED"
        rating = min(rating, 6.0)
        applied_caps.append({"reason": "identity_uncertain", "cap": 6.0})
    if subject_result == "FAIL":
        hard_failures.append(f"Expected {expected} visible subject(s), found {actual}")
        verdict = "FAIL"
        rating = min(rating, SUBJECT_COUNT_FAILURE_RATING_CAP)
        applied_caps.append({"reason": "subject_count_fail", "cap": SUBJECT_COUNT_FAILURE_RATING_CAP})
    if scores["anatomy"] <= 4:
        verdict = "FAIL"
        rating = min(rating, 5.5)
        applied_caps.append({"reason": "anatomy_fail", "cap": 5.5})
    if hard_failures:
        verdict = "FAIL"
        rating = min(rating, HARD_CONSTRAINT_RATING_CAP)
        applied_caps.append({"reason": "hard_constraint_failure", "cap": HARD_CONSTRAINT_RATING_CAP})
    return {
        **value,
        "identity": identity,
        "subject_count": {**value["subject_count"], "expected": expected, "actual": actual, "result": subject_result},
        "identity_failures": identity_failures,
        "defects": defects,
        "hard_constraint_failures": list(dict.fromkeys(hard_failures)),
        "verdict": verdict,
        "agent_scores": scores,
        "agent_rating": rating,
        "rating_before_caps": min(9.5, round(
            scores["identity"] * .30 + scores["anatomy"] * .20 + scores["prompt_adherence"] * .20
            + scores["composition"] * .15 + scores["visual_quality"] * .15,
            1,
        )),
        "applied_caps": applied_caps,
        "canonical_reference_count": reference_count,
    }


def _normalize_grounded_review(value: dict[str, Any], *, identifier: str, stage: str, expected_subject_count: int) -> dict[str, Any]:
    """Repair common compact VLM aliases without weakening deterministic gates."""
    if not isinstance(value, dict):
        raise ValueError("Visual review must be a JSON object")

    def score(raw: Any, default: float = 5.0) -> float:
        try:
            return max(1.0, min(10.0, float(raw)))
        except (TypeError, ValueError):
            return default

    identity_raw = value.get("identity", {})
    if isinstance(identity_raw, str):
        identity_result = identity_raw.strip().upper()
        identity_score = score(value.get("identity_score"), 9.0 if identity_result == "PASS" else 3.0 if identity_result == "FAIL" else 5.0)
        confidence = 0.75
    else:
        identity_raw = identity_raw if isinstance(identity_raw, dict) else {}
        identity_result = str(identity_raw.get("result", "UNCERTAIN")).strip().upper()
        identity_score = score(identity_raw.get("score"))
        try:
            confidence = float(identity_raw.get("confidence", 0.5))
        except (TypeError, ValueError):
            confidence = 0.5
        if 1 < confidence <= 100:
            confidence /= 100.0
    if identity_result not in {"PASS", "FAIL", "UNCERTAIN"}:
        identity_result = "UNCERTAIN"
    confidence = max(0.0, min(1.0, confidence))

    subject_raw = value.get("subject_count", {}) if isinstance(value.get("subject_count"), dict) else {}
    try:
        actual_subject_count = max(0, int(subject_raw.get("actual", expected_subject_count)))
    except (TypeError, ValueError):
        actual_subject_count = expected_subject_count
    scores_raw = value.get("scores", {}) if isinstance(value.get("scores"), dict) else value
    dimensions = ("anatomy", "prompt_adherence", "composition", "visual_quality")
    defects = value.get("defects", []) if isinstance(value.get("defects"), list) else []
    hard_failures = value.get("hard_constraint_failures", []) if isinstance(value.get("hard_constraint_failures"), list) else []
    if identity_result == "FAIL" and not defects:
        defects = ["Identity mismatch reported by grounded visual review"]
    summary = str(value.get("summary") or f"Compact grounded review: identity {identity_result.lower()}.").strip()
    return {
        "id": value.get("id") or identifier,
        "stage": value.get("stage") or stage,
        "candidate_observations": str(value.get("candidate_observations", "")).strip(),
        "reference_observations": str(value.get("reference_observations", "")).strip(),
        "identity_comparison": str(value.get("identity_comparison", "")).strip(),
        "outfit_design_adherence": str(value.get("outfit_design_adherence", "")).strip(),
        "identity": {"result": identity_result, "score": identity_score, "confidence": confidence},
        "subject_count": {
            "expected": int(subject_raw.get("expected", expected_subject_count) or expected_subject_count),
            "actual": actual_subject_count,
            "result": "PASS" if actual_subject_count == expected_subject_count else "FAIL",
        },
        "scores": {dimension: score(scores_raw.get(dimension)) for dimension in dimensions},
        "defects": [str(item) for item in defects if str(item).strip()],
        "hard_constraint_failures": [str(item) for item in hard_failures if str(item).strip()],
        "summary": summary,
    }


def _normalize_native_review(value: dict[str, Any], *, identifier: str, stage: str) -> dict[str, Any]:
    """Map the native model's descriptive aliases into the strict boundary contract."""
    compact_dimensions = ("identity", "anatomy", "prompt_adherence", "composition", "visual_quality")
    if set(value) == set(compact_dimensions) and all(isinstance(value[key], str) for key in compact_dimensions):
        normalized = {key: value[key].strip().upper() for key in compact_dimensions}
        scores = {key: 9 if result == "PASS" else 3 if result == "FAIL" else 5 for key, result in normalized.items()}
        failed = [key.replace("_", " ") for key, result in normalized.items() if result == "FAIL"]
        return {
            "id": identifier, "stage": stage,
            "verdict": "FAIL" if failed else "PASS", "scores": scores,
            "identity_failures": ["identity failed visual review"] if "identity" in failed else [],
            "defects": [f"{item} failed visual review" for item in failed],
            "hard_constraint_failures": [],
            "summary": "Native compact review: " + (", ".join(failed) if failed else "all evaluated dimensions passed") + ".",
        }
    identity_ok = value.get("identity_ok", value.get("preserved_elements", []))
    identity_ok = identity_ok if isinstance(identity_ok, list) else []
    scene_ok = value.get("scene_requirements_ok", [])
    scene_ok = scene_ok if isinstance(scene_ok, list) else []
    defects = value.get("defects", value.get("actual_visible_defects", []))
    defects = defects if isinstance(defects, list) else []
    drift = value.get("drift", value.get("narrative_compositional_drift", []))
    drift = drift if isinstance(drift, list) else []
    verdict = {
        "RETRY_ILLUSTRIOUS": "RETRY_RENDER",
        "RETRY_KLEIN": "RETRY_RENDER",
        "REVIEW": "REVIEW_REQUIRED",
        "REJECT": "FAIL",
    }.get(value.get("verdict"), value.get("verdict"))
    if verdict not in {"PASS", "MINOR_DEFECT", "FAIL", "RETRY_RENDER", "REVIEW_REQUIRED"}:
        raise ContractError(f"native review missing valid verdict (got {verdict!r})")
    rating = value.get("agent_rating")
    if isinstance(rating, bool) or not isinstance(rating, (int, float)) or not 1 <= float(rating) <= 10:
        raise ContractError("native review missing a real agent_rating from 1.0 to 10.0")
    requirements = value.get("requirements", [])
    requirements = requirements if isinstance(requirements, list) else []

    summary_parts = []
    if defects:
        summary_parts.append(f"Defects: {'; '.join(defects)}")
    if drift:
        summary_parts.append(f"Drift: {'; '.join(drift)}")
    return {
        "id": identifier,
        "stage": stage,
        "verdict": verdict,
        "agent_rating": float(rating),
        "identity_ok": identity_ok,
        "scene_requirements_ok": scene_ok,
        "requirements": requirements,
        "defects": defects,
        "drift": drift,
        "uncertainty": str(value.get("uncertainty", "")).strip(),
        "summary": " ".join(summary_parts) or "No visible defects or compositional drift detected.",
    }


def _validate_current_review(value: dict[str, Any], *, identifier: str, stage: str, semantic_spec: dict[str, Any]) -> dict[str, Any]:
    if isinstance(value.get("identity"), dict):
        return _rated_grounded_review(value, identifier=identifier, stage=stage, semantic_spec=semantic_spec)
    if "scores" in value:
        return _rated_review(value, identifier=identifier, stage=stage, semantic_spec=semantic_spec)
    validate_contract("visual_review_v2", value)
    if value["id"] != identifier or value["stage"] != stage:
        raise ValueError("Visual specialist changed the requested id or stage")
    if value["verdict"] == "PASS":
        supplied = semantic_spec.get("validation_requirements", []) if isinstance(semantic_spec, dict) else []
        required_ids = {item.get("requirement_id") for item in supplied if isinstance(item, dict) and item.get("applicability") == "REQUIRED"}
        results = {item.get("requirement_id"): item.get("result") for item in value["requirements"] if isinstance(item, dict)}
        if required_ids and not any(results.get(key) == "PASS" for key in required_ids):
            raise ContractError("PASS requires visible evidence for an important required condition")
        if any(results.get(key) == "FAIL" for key in required_ids):
            raise ContractError("PASS conflicts with a failed required condition")
        if not required_ids and not (value["identity_ok"] or value["scene_requirements_ok"]):
            raise ContractError("PASS requires visible evidence for at least one important requirement")
    return value


def _save_telemetry(directory: Path | None, name: str, response: dict[str, Any], *, model: str, latency: float, context_length: int | None, transport: str) -> None:
    if directory is None:
        return
    usage = response.get("usage", {}) if isinstance(response, dict) else {}
    stats = response.get("stats", {}) if isinstance(response, dict) else {}
    details = usage.get("completion_tokens_details", {}) if isinstance(usage, dict) else {}
    choices = response.get("choices", []) if isinstance(response, dict) else []
    finish_reason = choices[0].get("finish_reason") if choices and isinstance(choices[0], dict) else response.get("stop_reason")
    _save_diagnostic(directory, name, {
        "model": model, "agent": "visual_review", "prompt_tokens": usage.get("prompt_tokens", stats.get("input_tokens")),
        "completion_tokens": usage.get("completion_tokens", stats.get("total_output_tokens")), "reasoning_tokens": details.get("reasoning_tokens", stats.get("reasoning_output_tokens", 0)),
        "context_length": context_length, "latency_seconds": round(latency, 3),
        "finish_reason": finish_reason, "transport": transport,
        "time_to_first_token_seconds": (response.get("stats", {}) or {}).get("time_to_first_token_seconds") if isinstance(response, dict) else None,
    })


def review_stage_image(
    image_path: Path, *, identifier: str, stage: str, premise_spec: dict[str, Any],
    model: str, base_url: str = "http://127.0.0.1:1234", ttl_seconds: int | None = None,
    diagnostic_dir: Path | None = None, context_length: int | None = 8192,
    character_contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Review one boundary artifact with one fallback; failure remains hard."""
    if stage not in {"illustrious", "klein", "lustify", "miaomiao"}:
        raise ValueError("Unsupported renderer review stage")
    if not image_path.is_file():
        raise FileNotFoundError(image_path)
    spec_label = "ResolvedRenderSpec" if str(premise_spec.get("schema_version", "")).startswith("resolved_render_spec") else "approved semantic specification"
    character = premise_spec.get("character", {}) if isinstance(premise_spec.get("character"), dict) else {}
    must_preserve = character.get("must_preserve", []) if isinstance(character, dict) else []
    expected_visible = premise_spec.get("expected_visibility", [])
    identity_cues = [item for item in must_preserve if item in expected_visible and item not in {character.get("display_name"), character.get("canonical_tag")}]
    is_stock = premise_spec.get("creation_mode") == "stock"
    references = canonical_reference_paths(premise_spec, character_contract, limit=1 if is_stock else 2)
    expected_subject_count = int(premise_spec.get("expected_subject_count", 1) or 1)
    locked_requirements = [item for item in premise_spec.get("validation_requirements", []) if isinstance(item, dict) and item.get("applicability") == "REQUIRED"]
    normalized_contract = character_contract if isinstance(character_contract, dict) else {}
    review_context = {"character": character.get("display_name", ""), "identity_cues": identity_cues, "character_contract": {"character_id": normalized_contract.get("character_id", ""), "display_name": normalized_contract.get("display_name", ""), "identity": normalized_contract.get("identity", {}), "outfit": normalized_contract.get("outfit", {})}, "render_intent": premise_spec.get("render_intent"), "setting": premise_spec.get("hook_premise", {}).get("setting", ""), "composition": premise_spec.get("composition_intent", ""), "expected_visible": expected_visible, "environment_anchors": premise_spec.get("environment_anchors", []), "creation_mode": premise_spec.get("creation_mode", "scene"), "stock_render_policy": premise_spec.get("stock_render_policy", {}), "outfit_override": premise_spec.get("outfit_override"), "expected_subject_count": expected_subject_count, "locked_requirements": locked_requirements, "canonical_reference_count": len(references)}
    stock_instruction = " This is Stock, not a scene: evaluate white-background adherence, exactly one person, absence of environment/scenery/props/text/logos, neutral standing composition, outfit adherence, identity, anatomy, and visual quality. Do not require or invent scene/action evidence." if is_stock else ""
    prompt = RUNTIME_INSTRUCTION + "\n" + (f"Review the rendered {stage} image using the compact v4 contract. Return id exactly {identifier!r} and stage exactly {stage!r}; never substitute an agent or schema name. The first image is the IMAGE UNDER REVIEW. Any later images are CANONICAL REFERENCES and must never be counted as subjects in the generated image. FIRST decide identity and subject_count from pixels, before scoring image quality. CANONICAL REFERENCES ARE THE AUTHORITY FOR IDENTITY: textual tags and the character name are only context and must not override a visible mismatch. Identity PASS requires the same distinctive character design shown by the references, not merely a few generic shared colors, ears, hair, or clothing tags. If signature face, hairstyle, headwear, species design, or overall character design visibly differs, return identity FAIL even when the generated image satisfies textual tags and looks beautiful. Use UNCERTAIN when pixels or references are insufficient. For subject_count, count every distinct visible person in the IMAGE UNDER REVIEW, including partial profiles, heads, bodies, or hands belonging to another person at a frame edge. Do not count only the protagonist. Return expected={expected_subject_count}; actual is the objective number visible. If your summary mentions a friend or second person, actual cannot be 1. A beautiful image of the wrong character is identity FAIL. A clearly failed locked action, setting, outfit, or subject count belongs in hard_constraint_failures. Scores are whole numbers from 1 to 10; reserve 10 for exceptionally strong visible evidence and do not default all dimensions to the same score. {COMPACT_REVIEW_LIMITS_INSTRUCTION} Do not emit a verdict or overall rating because ADA computes both deterministically.{stock_instruction} Context: {json.dumps(review_context, ensure_ascii=False, separators=(',', ':'))}")
    content: list[dict[str, Any]] = [
        {"type": "text", "text": prompt + "\nIMAGE UNDER REVIEW:"},
        {"type": "image_url", "image_url": {"url": image_data_url(image_path)}},
    ]
    for index, reference in enumerate(references, start=1):
        content.extend([
            {"type": "text", "text": f"CANONICAL REFERENCE {index}:"},
            {"type": "image_url", "image_url": {"url": image_data_url(reference)}},
        ])
    payload: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "temperature": 0,
        "max_tokens": 4096,
        "response_format": response_format("visual_review_v4"),
    }
    if ttl_seconds is not None:
        payload["ttl"] = ttl_seconds
    errors: list[str] = []
    started = time.perf_counter()
    req_ts = int(time.time() * 1000)
    safe_id = identifier.replace(":", "_")
    for attempt in range(2):
        try:
            response = _request(f"{base_url.rstrip('/')}/v1/chat/completions", payload, timeout=600)
            _save_diagnostic(diagnostic_dir, f"{safe_id}_{req_ts}_attempt_0{attempt+1}_schema.json", response)
            _save_telemetry(diagnostic_dir, f"{safe_id}_{req_ts}_attempt_0{attempt+1}_schema_telemetry.json", response, model=model, latency=time.perf_counter() - started, context_length=context_length, transport="openai")
            value = _parse_json_object(_content_text(response))
            value = _normalize_grounded_review(value, identifier=identifier, stage=stage, expected_subject_count=expected_subject_count)

            # Sanity Check for Role Swapping
            if "reference" in value["candidate_observations"].lower() and attempt == 0:
                if value["identity"]["result"] == "FAIL":
                    errors.append("schema: Suspected role swapping (Candidate/Reference). Retrying.")
                    continue

            value = _rated_grounded_review(
                value, identifier=identifier, stage=stage,
                semantic_spec=premise_spec, reference_count=len(references),
            )
            value["provenance"] = {
                "asset_id": identifier,
                "character_id": str(character.get("slug") or character.get("canonical_tag") or character.get("display_name", "")),
                "candidate_path": str(image_path),
                "reference_paths": [str(r) for r in references],
                "model": model,
                "evaluator_version": "v4",
                "timestamp": time.time(),
                "request_id": f"rev_{safe_id}_{req_ts}"
            }

            return value
        except Exception as exc:
            errors.append(f"schema attempt {attempt+1}: {type(exc).__name__}: {exc}")

    native_input: list[dict[str, Any]] = [
        {"type": "text", "content": prompt + " Return only the v4 JSON object. Reasoning text is forbidden.\nIMAGE UNDER REVIEW:"},
        {"type": "image", "data_url": image_data_url(image_path)},
    ]
    for index, reference in enumerate(references, start=1):
        native_input.extend([
            {"type": "text", "content": f"CANONICAL REFERENCE {index}:"},
            {"type": "image", "data_url": image_data_url(reference)},
        ])
    native_payload: dict[str, Any] = {
        "model": model,
        "input": native_input,
        "temperature": 0,
        "max_output_tokens": 4096,
        "store": False,
    }
    if ttl_seconds is not None:
        native_payload["ttl"] = ttl_seconds
    native_started = time.perf_counter()
    try:
        native = _request(f"{base_url.rstrip('/')}/api/v1/chat", native_payload, timeout=600)
        _save_diagnostic(diagnostic_dir, f"{safe_id}_{req_ts}_attempt_02_native.json", native)
        _save_telemetry(diagnostic_dir, f"{safe_id}_{req_ts}_attempt_02_native_telemetry.json", native, model=model, latency=time.perf_counter() - native_started, context_length=context_length, transport="native")
        value = _parse_json_object(_native_content_text(native))
        value = _normalize_grounded_review(value, identifier=identifier, stage=stage, expected_subject_count=expected_subject_count)
        value = _rated_grounded_review(
            value, identifier=identifier, stage=stage,
            semantic_spec=premise_spec, reference_count=len(references),
        )
        value["provenance"] = {
            "asset_id": identifier,
            "character_id": str(character.get("slug") or character.get("canonical_tag") or character.get("display_name", "")),
            "candidate_path": str(image_path),
            "reference_paths": [str(r) for r in references],
            "model": model,
            "evaluator_version": "v4",
            "timestamp": time.time(),
            "request_id": f"rev_{safe_id}_{req_ts}",
        }
        return value
    except Exception as exc:
        errors.append(f"native: {type(exc).__name__}: {exc}")
    raise VisualReviewTransportError("Visual Review failed hard after controlled transports: " + " | ".join(errors))
