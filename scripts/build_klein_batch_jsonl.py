#!/usr/bin/env python3
"""Build one self-contained JSONL dataset for the reusable Illustrious -> Klein workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_SOURCE = ("id", "character", "illustrious_prompt", "klein_prompt")


def load_records(path: Path) -> list[dict]:
    records: list[dict] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        value = json.loads(raw)
        missing = [field for field in REQUIRED_SOURCE if not isinstance(value.get(field), str) or not value[field].strip()]
        if missing:
            raise ValueError(f"{path}:{line_number}: missing required fields: {', '.join(missing)}")
        records.append(value)
    if not records:
        raise ValueError("The source dataset is empty")
    ids = [item["id"] for item in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Dataset contains duplicate ids")
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--take", type=int, default=None, help="Write only the first N records")
    parser.add_argument("--illustrious-seed-base", type=int, default=1_000_001)
    parser.add_argument("--klein-seed-base", type=int, default=2_000_001)
    args = parser.parse_args()
    records = load_records(args.source)
    if args.take is not None:
        if args.take < 1:
            raise ValueError("--take must be positive")
        records = records[:args.take]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        for index, source in enumerate(records):
            record = {
                "id": source["id"],
                "character": source["character"],
                "illustrious_prompt": source["illustrious_prompt"],
                "klein_prompt": source["klein_prompt"],
                "illustrious_seed": int(source.get("illustrious_seed", args.illustrious_seed_base + index)),
                "klein_seed": int(source.get("klein_seed", args.klein_seed_base + index)),
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps({"status": "ok", "count": len(records), "output": str(args.output.resolve())}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
