#!/usr/bin/env python3
"""Run one explicit historical ProductionCandidate through the isolated image pipeline."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

ADA_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ADA_ROOT))
sys.path.insert(0, str(ADA_ROOT / "scripts"))

from ada_app.pilot_runner import read_json, run_pilot_pipeline, write_json
from scripts.ada_paths import MISSION_RUNS_ROOT


RUNS_ROOT = MISSION_RUNS_ROOT


def optional_json(path: Path) -> Any | None:
    return read_json(path) if path.is_file() else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-run", default="m2_2b_test_retry_001")
    parser.add_argument("--concept-id", default="m1_2b_02")
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()

    source_run = RUNS_ROOT / args.source_run
    target_run = RUNS_ROOT / args.run_id
    if target_run.exists():
        raise FileExistsError(f"Smoke target already exists: {target_run}")
    if not source_run.is_dir():
        raise FileNotFoundError(f"Explicit source run does not exist: {source_run}")

    source_candidates = read_json(source_run / "pilot_candidates.json")
    source_candidate = next(
        (candidate for candidate in source_candidates if candidate.get("concept_id") == args.concept_id),
        None,
    )
    if source_candidate is None:
        raise ValueError(f"Concept {args.concept_id!r} is not in explicit source run {args.source_run!r}")

    candidate = {
        "concept_id": args.concept_id,
        "candidate_id": f"{args.run_id}:{args.concept_id}",
        "source_mission_id": f"workflow-separation-smoke:{args.run_id}",
        "source_run_id": args.source_run,
        "original_proposal": copy.deepcopy(source_candidate["original_proposal"]),
        "pipeline_state": "PENDING",
        "quality_retries": 0,
        "runtime_retries": 0,
        "max_retries": 2,
    }
    write_json(target_run / "character_profile.json", read_json(source_run / "character_profile.json"))
    write_json(target_run / "pilot_candidates.json", [candidate])
    write_json(target_run / "workflow_separation_smoke_request.json", {
        "source_run_id": args.source_run,
        "source_concept_id": args.concept_id,
        "candidate_count": 1,
        "expected_comfy_submissions_happy_path": 2,
    })

    run_pilot_pipeline(target_run, [candidate], target_approvals=1)

    final_candidate = read_json(target_run / "pilot_candidates.json")[0]
    pilot_dir = target_run / "pilot" / args.concept_id
    submission_paths = sorted((pilot_dir / "submissions").glob("*.json"))
    submissions = [read_json(path) for path in submission_paths]
    report = {
        "run_id": args.run_id,
        "character": (
            read_json(target_run / "character_profile.json").get("name")
            or candidate["original_proposal"].get("character")
        ),
        "concept_id": args.concept_id,
        "candidate_id": candidate["candidate_id"],
        "pipeline_state": final_candidate.get("pipeline_state"),
        "illustrious_prompt": optional_json(pilot_dir / "illustrious_result.json"),
        "illustrious_review": optional_json(pilot_dir / "illustrious_review.json"),
        "klein_prompt": optional_json(pilot_dir / "klein_result.json"),
        "final_review": optional_json(pilot_dir / "final_review.json"),
        "submissions": submissions,
    }
    write_json(target_run / "workflow_separation_smoke_report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if final_candidate.get("pipeline_state") == "APPROVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
