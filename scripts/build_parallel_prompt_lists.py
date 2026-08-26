#!/usr/bin/env python3
"""Build and validate index-aligned Illustrious/Klein prompt lists from JSONL."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = ("id", "illustrious_prompt", "klein_prompt")


def read_jsonl(path: Path) -> list[dict]:
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        missing = [key for key in REQUIRED if not isinstance(record.get(key), str) or not record[key].strip()]
        if missing:
            raise ValueError(f"{path}:{number} missing required fields: {', '.join(missing)}")
        records.append(record)
    ids = [record["id"] for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Prompt source has duplicate ids")
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--take", type=int, default=3)
    args = parser.parse_args()
    if args.take < 1:
        raise ValueError("--take must be positive")

    records = read_jsonl(args.source)[:args.take]
    if len(records) != args.take:
        raise ValueError(f"Requested {args.take} records but source contains {len(records)}")
    payload = {
        "ids": [record["id"] for record in records],
        "illustrious_prompts": [record["illustrious_prompt"] for record in records],
        "klein_prompts": [record["klein_prompt"] for record in records],
        "illustrious_seeds": [record.get("illustrious_seed", 1000000 + index) for index, record in enumerate(records)],
        "klein_seeds": [record.get("klein_seed", 2000000 + index) for index, record in enumerate(records)],
    }
    lengths = {len(value) for value in payload.values()}
    if lengths != {len(records)}:
        raise ValueError(f"Parallel list length mismatch: {sorted(lengths)}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "count": len(records), "ids": payload["ids"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
