#!/usr/bin/env python3
"""Non-ComfyUI ADA migration smoke checks for paths, data and compilation."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ada_paths import (  # noqa: E402
    ADA_ROOT, CHARACTER_DB_ROOT, COMFYUI_ROOT, CONFIG_ROOT, GENERATED_ASSETS_ROOT,
    KLEIN_BATCH_RUNS_ROOT, PROMPTS_ROOT, VISUAL_REVIEW_RUNS_ROOT, WORKFLOWS_ROOT,
    path_summary, resolve_legacy_path,
)
from character_dataset import CharacterDatasetBuilder  # noqa: E402
from character_profile import CharacterProfileDatabase  # noqa: E402
from run_klein_jsonl_batch import (  # noqa: E402
    apply_klein_preset, bind_record, compile_api, load_dataset, load_klein_preset_plan,
)


def main() -> int:
    result: dict = {"created_at": datetime.now(timezone.utc).isoformat(), "tests": {}}

    summary = path_summary()
    required = [ADA_ROOT, CHARACTER_DB_ROOT, PROMPTS_ROOT, KLEIN_BATCH_RUNS_ROOT,
                VISUAL_REVIEW_RUNS_ROOT, WORKFLOWS_ROOT, COMFYUI_ROOT]
    result["tests"]["A_path_resolution"] = {
        "status": "pass" if all(path is not None and Path(path).exists() for path in required) else "fail",
        "paths": summary,
        "generated_assets_exists_before_strategy_file": GENERATED_ASSETS_ROOT.exists(),
    }

    profile = CharacterProfileDatabase().get_character_profile("2B", "NieR:Automata")
    result["tests"]["B_character_profile"] = {
        "status": "pass" if profile.get("character_profile_used") is True and
                            profile.get("matched_tag") == "2b_(nier:automata)" else "fail",
        "result": profile,
    }

    dataset_id = "ada_migration_smoke_2"
    builder = CharacterDatasetBuilder()
    prepared = builder.prepare("2B", "NieR:Automata", 2, dataset_id)
    entries = [
        {
            "id": "ada_smoke_2b_closeup_01", "category": "closeup",
            "premise": "A restrained portrait for migration validation.",
            "illustrious_prompt": "2B from NieR:Automata, beautiful, canonical black YoRHa outfit and black blindfold, tight close-up framing, eye-level view, neutral expression, plain industrial interior",
            "klein_prompt": "2B from NieR:Automata, beautiful, preserve canonical black YoRHa outfit, black blindfold and facial identity, tight close-up framing, eye-level view, realistic finish",
            "illustrious_seed": 918273645, "klein_seed": 918273646,
        },
        {
            "id": "ada_smoke_2b_medium_01", "category": "medium",
            "premise": "A simple standing view for workflow compilation validation.",
            "illustrious_prompt": "2B from NieR:Automata, beautiful, canonical black YoRHa outfit and black blindfold, medium framing, three-quarter view, calm standing pose, ruined city background",
            "klein_prompt": "2B from NieR:Automata, beautiful, preserve canonical black YoRHa outfit, black blindfold, identity and pose, medium framing, three-quarter view, realistic finish",
            "illustrious_seed": 918273647, "klein_seed": 918273648,
        },
    ]
    appended = builder.append(dataset_id, entries)
    finalized = builder.finalize("2B", "NieR:Automata", 2, dataset_id)
    result["tests"]["C_dataset_pipeline"] = {
        "status": "pass" if finalized.get("status") == "valid" else "fail",
        "prepared": {key: prepared.get(key) for key in ("dataset_id", "distribution", "refs_cache_used", "character_profile_used")},
        "appended": appended, "finalized": finalized,
    }

    existing_dataset = PROMPTS_ROOT / "tifa_lockhart_ff7_remake_pilot_v2_6.jsonl"
    existing_plan = CONFIG_ROOT / "klein_presets_tifa_remake_pilot_v2_6.json"
    existing_manifest = KLEIN_BATCH_RUNS_ROOT / "tifa_remake_pilot_v2_6_001" / "manifest.json"
    existing_review = VISUAL_REVIEW_RUNS_ROOT / "worker_vs_master_v1_20260821_003" / "results.json"
    loaded_documents = {
        "dataset_records": len(load_dataset(existing_dataset, take=None)),
        "preset_plan_schema": json.loads(existing_plan.read_text(encoding="utf-8")).get("schema_version"),
        "generation_manifest_status": json.loads(existing_manifest.read_text(encoding="utf-8")).get("status"),
        "visual_review_status": json.loads(existing_review.read_text(encoding="utf-8")).get("status"),
    }
    result["tests"]["F_existing_data"] = {"status": "pass", **loaded_documents}

    records = load_dataset(existing_dataset, take=None)
    presets = load_klein_preset_plan(existing_plan, records)
    base = json.loads((WORKFLOWS_ROOT / "illustrious_to_klein_batch_base_ui.json").read_text(encoding="utf-8"))
    compiled = compile_api(bind_record(base, records[0], "LunaKleinBatch/ada_migration_validation_only"))
    apply_klein_preset(compiled, presets[records[0]["id"]])
    result["tests"]["G_runner_validation"] = {
        "status": "pass", "workflow": str(WORKFLOWS_ROOT / "illustrious_to_klein_batch_base_ui.json"),
        "dataset": str(existing_dataset), "preset_plan": str(existing_plan),
        "record_id": records[0]["id"], "compiled_nodes": len(compiled), "comfyui_executed": False,
    }

    case_document = json.loads((VISUAL_REVIEW_RUNS_ROOT / "worker_vision_v1_20260821_003" / "input_cases.json").read_text(encoding="utf-8"))
    legacy_value = case_document["cases"][0]["comparison_image"]
    resolved = resolve_legacy_path(legacy_value)
    result["tests"]["H_generated_asset"] = {
        "status": "pass" if resolved.is_file() else "fail", "legacy_value": legacy_value,
        "resolved": str(resolved), "bytes": resolved.stat().st_size if resolved.is_file() else None,
        "junction_used": False,
    }

    target = ROOT / "migration" / "data_smoke_results.json"
    with target.open("x", encoding="utf-8") as output:
        json.dump(result, output, ensure_ascii=False, indent=2)
        output.write("\n")
    print(json.dumps({name: data["status"] for name, data in result["tests"].items()}))
    return 0 if all(data["status"] == "pass" for data in result["tests"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
