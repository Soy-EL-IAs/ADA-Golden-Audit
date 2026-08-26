#!/usr/bin/env python3
"""Materialize the one-queue Illustrious→Krea workflow for one JSONL record."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from luna_pipeline import (
    ILLUSTRIOUS_WORKFLOW,
    KREA_WORKFLOW,
    PACKAGE_ROOT,
    find_premise,
    illustrious_negative,
    illustrious_positive,
    join_tags,
)


TEMPLATE = PACKAGE_ROOT / "workflows" / "legacy" / "specialist" / "illustrious_to_krea_fast_chained_api.json"


def krea_record_prompt(record: dict[str, object]) -> str:
    """Use only record facts and preserve Illustrious as the composition reference."""
    return (
        "Preserve the Illustrious source image as the composition reference. "
        f"Character: {record['character']} ({record['franchise']}). "
        f"Identity: {join_tags(record['identity'])}. "
        f"Premise: {record['premise']}. "
        f"Required elements: {join_tags(record['must_include'])}. "
        f"Environment: {join_tags(record['environment'])}. "
        f"Avoid: {join_tags(record['avoid'])}. "
        f"Final-render direction: {record['krea_direction']}. "
        "Preserve identity, clothing, pose, action, props, environment and framing. "
        "Do not add or remove characters, props, locations or events."
    )


def replace_text(value: object, replacements: dict[str, str]) -> object:
    if isinstance(value, str):
        for old, new in replacements.items():
            value = value.replace(old, new)
    elif isinstance(value, list):
        return [replace_text(item, replacements) for item in value]
    elif isinstance(value, dict):
        return {key: replace_text(item, replacements) for key, item in value.items()}
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--premises", type=Path, required=True)
    parser.add_argument("--premise-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    record = find_premise(args.premises, args.premise_id)
    workflow = copy.deepcopy(json.loads(TEMPLATE.read_text(encoding="utf-8")))
    replacements = {
        "ILLUSTRIOUS_PROMPT_REPLACED_BY_ORCHESTRATOR": illustrious_positive(record),
        "ILLUSTRIOUS_NEGATIVE_REPLACED_BY_ORCHESTRATOR": illustrious_negative(record),
        "KREA_PROMPT_REPLACED_BY_ORCHESTRATOR": krea_record_prompt(record),
        "RECORD_ID_REPLACED_BY_ORCHESTRATOR": record["id"],
    }
    workflow = replace_text(workflow, replacements)
    workflow["5"]["inputs"]["seed"] = record["seed_base"]
    workflow["18"]["inputs"]["seed"] = record["krea_seed_base"]
    workflow["_meta"]["record"] = {
        "id": record["id"],
        "illustrious_seed": record["seed_base"],
        "krea_seed": record["krea_seed_base"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(workflow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
