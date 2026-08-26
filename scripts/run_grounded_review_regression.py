#!/usr/bin/env python3
"""Re-review the fixed three-image corpus without generating new images."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.ada_paths import ADA_ROOT
from scripts.specialist_visual_reviewer import review_stage_image


MODEL = "qwen/qwen3-vl-8b"
from scripts.ada_paths import MISSION_RUNS_ROOT, REVIEW_RUNS_ROOT
OUTPUT_ROOT = REVIEW_RUNS_ROOT / "grounded_identity_subject_count_v3"
CASES = [
    {
        "case_id": "chun_li_expected_pass",
        "expected": {"identity": "PASS", "subject_count": "PASS", "verdict": "PASS"},
        "candidate_dir": "data/runs/missions/m2_mission_20260825_110816_d940a0_r01_110825345470/pilot/m1_chun_li_01",
    },
    {
        "case_id": "nanally_expected_identity_fail",
        "expected": {"identity": "FAIL", "verdict": "FAIL", "maximum_rating": 4.0},
        "candidate_dir": "data/runs/missions/m2_mission_20260825_111112_757917_r01_111116827612/pilot/m1_nanally_de_nte_01",
    },
    {
        "case_id": "hinata_expected_subject_count_fail",
        "expected": {"identity": "PASS", "subject_count": "FAIL", "verdict": "FAIL", "maximum_rating": 4.5},
        "candidate_dir": "data/runs/missions/m2_mission_20260825_110555_5090de_r01_110602370180/pilot/m1_hyuuga_hinata_03",
    },
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def old_raw_review(candidate_dir: Path) -> dict:
    response = read_json(candidate_dir / "visual_review" / "lustify" / "attempt_01_schema.json")
    return json.loads(response["choices"][0]["message"]["content"])


def run() -> dict:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "input_cases.json").write_text(
        json.dumps({"schema_version": "grounded_review_regression_v1", "cases": CASES}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    results = []
    for case in CASES:
        candidate_dir = ADA_ROOT / case["candidate_dir"]
        spec = read_json(candidate_dir / "resolved_render_spec_v3.json")
        contract = read_json(candidate_dir / "character_contract_v1.json")
        receipt = read_json(candidate_dir / "render_receipts" / "lustify_attempt_01.json")
        image = Path(receipt["output_asset"])
        review = review_stage_image(
            image,
            identifier=spec["concept_id"],
            stage="lustify",
            premise_spec=spec,
            character_contract=contract,
            model=MODEL,
            diagnostic_dir=OUTPUT_ROOT / case["case_id"],
            context_length=8192,
        )
        results.append({
            "case_id": case["case_id"],
            "image": str(image),
            "expected": case["expected"],
            "old_raw_review": old_raw_review(candidate_dir),
            "new_review": review,
        })
    report = {
        "schema_version": "grounded_review_regression_results_v1",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "new_images_generated": 0,
        "results": results,
    }
    (OUTPUT_ROOT / "results.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


if __name__ == "__main__":
    value = run()
    for item in value["results"]:
        review = item["new_review"]
        print(item["case_id"], review["identity"]["result"], review["subject_count"]["result"], review["verdict"], review["agent_rating"])
