#!/usr/bin/env python3
"""One-shot ADA end-to-end certification. No retries and no Master review."""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
os.environ["ADA_ROOT"] = str(ROOT)
os.environ["PIPELINE_ORCHESTRATION"] = "1"

from ada_paths import ADA_ROOT, COMFYUI_ROOT  # noqa: E402
from lmstudio_operator import (  # noqa: E402
    CHARACTER_DATASETS, CONTROLLER, image_path, tool_append_character_dataset_entries,
    tool_finalize_character_dataset, tool_generate_character_dataset, tool_review_batch, tool_run_batch,
)


DATASET_ID = "ada_e2e_v1"
BATCH_ID = "ada_e2e_v1_001"
CATEGORIES = ["closeup", "fullbody", "dynamic", "cinematic"]
LEGACY_ROOT_TEXT = r"C:\Users\ELIAS\Documents\Codex\2026-08-20\referenced-chatgpt-conversation-this-is-an\outputs\luna_pipeline"


def loaded_models() -> list[str]:
    return [str(item.get("model")) for item in CONTROLLER.list_models()["loaded"]]


def normalize_loras(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        lora = value.get("lora")
        strength = value.get("strength")
        if isinstance(lora, str) and isinstance(strength, (int, float)):
            found.append({"lora": lora.replace("\\", "/"), "strength": float(strength)})
        for child in value.values():
            found.extend(normalize_loras(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(normalize_loras(child))
    return found


def unique_loras(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[tuple[str, float]] = set()
    for item in items:
        key = (item["lora"], item["strength"])
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def png_metadata(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    with Image.open(path) as image:
        prompt = json.loads(image.info["prompt"])
        workflow = json.loads(image.info["workflow"])
    return prompt, workflow


def expected_loras(category: str) -> list[dict[str, Any]]:
    if category == "closeup":
        return [
            {"lora": "flux/klein_snofs_v1_3.safetensors", "strength": 0.6},
            {"lora": "flux/A2R_Klein_Standard.safetensors", "strength": 0.5},
        ]
    return [
        {"lora": "flux/klein_snofs_v1_3.safetensors", "strength": 0.6},
        {"lora": "flux/anime2real-semi.safetensors", "strength": 0.8},
    ]


def has_expected(actual: list[dict[str, Any]], expected: list[dict[str, Any]]) -> bool:
    return all(item in actual for item in expected)


def contains_legacy_text(path: Path) -> bool:
    if path.suffix.lower() not in {".json", ".jsonl", ".md", ".txt"}:
        return False
    return LEGACY_ROOT_TEXT.lower() in path.read_text(encoding="utf-8", errors="replace").lower()


def entries() -> list[dict[str, Any]]:
    return [
        {
            "id": "ada_e2e_2b_closeup_01", "category": "closeup",
            "premise": "A calm close portrait for checking 2B identity, blindfold and facial clarity.",
            "illustrious_prompt": "2B from NieR:Automata, beautiful, short white hair, black blindfold, canonical black YoRHa dress, black gloves and thigh boots, tight close-up framing, eye-level view, calm determined expression, softly lit Resistance camp interior",
            "klein_prompt": "2B from NieR:Automata, beautiful, preserve short white hair, black blindfold, canonical black YoRHa dress and facial identity, tight close-up framing, eye-level view, realistic finish",
            "illustrious_seed": 421001, "klein_seed": 421002,
        },
        {
            "id": "ada_e2e_2b_fullbody_01", "category": "fullbody",
            "premise": "A neutral full-body view to verify the canonical YoRHa silhouette and outfit.",
            "illustrious_prompt": "2B from NieR:Automata, beautiful, short white hair, black blindfold, canonical black YoRHa dress, black gloves, thigh boots and sword, full-body framing, three-quarter view, neutral standing pose, ruined city street at dawn",
            "klein_prompt": "2B from NieR:Automata, beautiful, preserve the canonical black YoRHa dress, blindfold, white hair, gloves, thigh boots and sword, full-body framing, three-quarter view, realistic finish",
            "illustrious_seed": 421003, "klein_seed": 421004,
        },
        {
            "id": "ada_e2e_2b_dynamic_01", "category": "dynamic",
            "premise": "A clear evasive sword action to test anatomy, single subject and motion.",
            "illustrious_prompt": "2B from NieR:Automata, beautiful, short white hair, black blindfold, canonical black YoRHa dress, black gloves and thigh boots, full-body framing, low-angle view, dynamic evasive leap with a sword, crumbling industrial ruins and drifting dust",
            "klein_prompt": "2B from NieR:Automata, beautiful, preserve canonical YoRHa identity, black blindfold, black dress, gloves, thigh boots, sword and leaping pose, full-body framing, low-angle view, realistic finish",
            "illustrious_seed": 421005, "klein_seed": 421006,
        },
        {
            "id": "ada_e2e_2b_cinematic_01", "category": "cinematic",
            "premise": "A quiet cinematic departure through a devastated machine-city corridor.",
            "illustrious_prompt": "2B from NieR:Automata, beautiful, short white hair, black blindfold, canonical black YoRHa dress, black gloves and thigh boots, cinematic framing, profile view, walking through a rain-soaked abandoned machine-city corridor with distant warm lights",
            "klein_prompt": "2B from NieR:Automata, beautiful, preserve canonical YoRHa identity, black blindfold, black dress, white hair, gloves and thigh boots, cinematic framing, profile view, realistic finish",
            "illustrious_seed": 421007, "klein_seed": 421008,
        },
    ]


def main() -> int:
    report_path = ROOT / "migration" / "ADA_E2E_CERTIFICATION_V1.json"
    if report_path.exists():
        raise FileExistsError(f"Refusing to overwrite certification report: {report_path}")
    report: dict[str, Any] = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dataset_id": DATASET_ID, "batch_id": BATCH_ID, "ada_root": str(ADA_ROOT),
        "categories": CATEGORIES, "legacy_runtime_used": False, "comfyui_executed": True,
        "master_visual_review_executed": False, "models": {"inventories": {}}, "timings_seconds": {},
    }
    status = "FAIL"
    try:
        report["models"]["inventories"]["initial"] = loaded_models()
        prepared = tool_generate_character_dataset("2B", "NieR:Automata", 4, DATASET_ID, CATEGORIES)
        report["dataset_prepare"] = prepared
        profile_path = CHARACTER_DATASETS.character_profiles.dataset_path.resolve()
        report["profile"] = {
            "character_profile_used": prepared["character_profile_used"],
            "matched_tag": prepared["character_profile"].get("matched_tag"),
            "dataset_path": str(profile_path),
            "under_ada": profile_path.is_relative_to(ADA_ROOT),
        }
        if prepared["categories_plan"] != CATEGORIES or not prepared["character_profile_used"] or not report["profile"]["under_ada"]:
            raise RuntimeError("Dataset preparation did not use the requested local category/profile plan")

        appended = tool_append_character_dataset_entries(DATASET_ID, entries())
        finalized = tool_finalize_character_dataset("2B", 4, DATASET_ID, "NieR:Automata")
        report["dataset_append"] = appended
        report["dataset_finalize"] = finalized
        if finalized.get("status") != "valid":
            raise RuntimeError("Dataset finalize did not return valid")

        dataset_path = (ADA_ROOT / finalized["dataset"]).resolve()
        preset_path = (ADA_ROOT / finalized["preset_plan"]).resolve()
        if not dataset_path.is_file() or not preset_path.is_file() or not dataset_path.is_relative_to(ADA_ROOT) or not preset_path.is_relative_to(ADA_ROOT):
            raise RuntimeError("Dataset or preset plan was not created inside Ada")
        report["paths"] = {"dataset": str(dataset_path), "preset_plan": str(preset_path), "comfyui_root": str(COMFYUI_ROOT)}

        started = time.perf_counter()
        batch = tool_run_batch(finalized["dataset"], BATCH_ID, finalized["preset_plan"])
        report["timings_seconds"]["batch"] = round(time.perf_counter() - started, 3)
        report["batch"] = batch
        report["models"]["inventories"]["after_batch"] = loaded_models()
        if batch.get("exit_code") != 0:
            raise RuntimeError(f"Batch failed without retry: {batch.get('error') or batch}")

        manifest_path = ADA_ROOT / "klein_batch_runs" / BATCH_ID / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        completed = [record for record in manifest.get("records", []) if record.get("status") == "complete"]
        if manifest.get("status") != "complete" or len(completed) != 4:
            raise RuntimeError(f"Expected exactly four completed records, got {len(completed)}")
        report["generation"] = {"manifest": str(manifest_path), "status": manifest["status"], "records": []}

        for record in completed:
            category = next(item["category"] for item in entries() if item["id"] == record["id"])
            compare_path = image_path(record["compare"][0]).resolve()
            if not compare_path.is_file() or not str(compare_path).lower().startswith(str(COMFYUI_ROOT).lower()):
                raise RuntimeError(f"Generated asset did not resolve through Ada's external ComfyUI root: {compare_path}")
            runtime, workflow = png_metadata(compare_path)
            positive = str(runtime.get("2", {}).get("inputs", {}).get("text", ""))
            runtime_loras = unique_loras(normalize_loras(runtime))
            workflow_loras = unique_loras(normalize_loras(workflow))
            expected = expected_loras(category)
            runtime_ok = has_expected(runtime_loras, expected)
            report["generation"]["records"].append({
                "id": record["id"], "category": category, "compare_png": str(compare_path),
                "illustrious_positive_has_1girl": bool(re.search(r"(?<![a-z0-9])1girl(?![a-z0-9])", positive, re.I)),
                "runtime_loras": runtime_loras, "runtime_loras_match": runtime_ok,
                "workflow_loras": workflow_loras,
            })
            if not runtime_ok or not report["generation"]["records"][-1]["illustrious_positive_has_1girl"]:
                raise RuntimeError(f"PNG runtime metadata validation failed for {record['id']}")

        workflow_checks = []
        for chosen in ("ada_e2e_2b_closeup_01", "ada_e2e_2b_dynamic_01"):
            item = next(record for record in report["generation"]["records"] if record["id"] == chosen)
            expected = expected_loras(item["category"])
            workflow_checks.append({"id": chosen, "match": has_expected(item["workflow_loras"], expected)})
        report["embedded_workflow_checks"] = workflow_checks
        if not all(check["match"] for check in workflow_checks):
            raise RuntimeError("Embedded workflow LoRA metadata does not match runtime for required samples")

        started = time.perf_counter()
        review = tool_review_batch(BATCH_ID, 4, deep=False)
        report["timings_seconds"]["worker_review"] = round(time.perf_counter() - started, 3)
        report["worker_review"] = review
        review_path = Path(review["report"]).resolve()
        review_document = json.loads(review_path.read_text(encoding="utf-8"))
        if review_document.get("model") != CONTROLLER.role("worker").model or review_document.get("count") != 4:
            raise RuntimeError("Worker review did not produce four expected reviews")
        report["models"]["inventories"]["after_worker_review"] = loaded_models()

        runtime_text_paths = [dataset_path, preset_path, manifest_path, review_path,
                              ADA_ROOT / "character_dataset_staging" / DATASET_ID / "metadata.json",
                              ADA_ROOT / "character_dataset_staging" / DATASET_ID / "entries.jsonl"]
        legacy_hits = [str(path) for path in runtime_text_paths if contains_legacy_text(path)]
        report["legacy_runtime_used"] = bool(legacy_hits)
        report["legacy_runtime_hits"] = legacy_hits
        if legacy_hits:
            raise RuntimeError(f"New runtime artifacts contain legacy project paths: {legacy_hits}")
        status = "PASS"
    except Exception as exc:
        report["error"] = str(exc)
    finally:
        # The current reviewer intentionally leaves its Worker loaded; this
        # certification restores the documented stable state explicitly.
        CONTROLLER.unload_all()
        CONTROLLER.wait_for_vram_release()
        CONTROLLER.ensure_loaded("master")
        report["models"]["inventories"]["final"] = loaded_models()
        report["master_only_final"] = report["models"]["inventories"]["final"] == [CONTROLLER.role("master").model]
        if not report["master_only_final"]:
            status = "FAIL"
        report["status"] = status
        with report_path.open("x", encoding="utf-8") as output:
            json.dump(report, output, ensure_ascii=False, indent=2)
            output.write("\n")
    print(json.dumps({"status": status, "report": str(report_path), "master_only_final": report["master_only_final"]}, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
