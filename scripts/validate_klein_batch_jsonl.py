#!/usr/bin/env python3
"""Validate records consumed by the one reusable Illustrious -> Klein workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = ("id", "character", "illustrious_prompt", "klein_prompt", "illustrious_seed", "klein_seed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    args = parser.parse_args()
    ids: list[str] = []
    for line_number, raw in enumerate(args.dataset.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        value = json.loads(raw)
        missing = [key for key in REQUIRED if key not in value]
        if missing:
            raise ValueError(f"{args.dataset}:{line_number}: missing {', '.join(missing)}")
        for key in ("id", "character", "illustrious_prompt", "klein_prompt"):
            if not isinstance(value[key], str) or not value[key].strip():
                raise ValueError(f"{args.dataset}:{line_number}: {key} must be non-empty text")
        for key in ("illustrious_seed", "klein_seed"):
            if not isinstance(value[key], int) or value[key] < 0:
                raise ValueError(f"{args.dataset}:{line_number}: {key} must be a non-negative integer")
        ids.append(value["id"])
    if not ids:
        raise ValueError("Dataset is empty")
    if len(ids) != len(set(ids)):
        raise ValueError("Dataset has duplicate ids")
    print(json.dumps({"status": "ok", "count": len(ids), "first_id": ids[0], "last_id": ids[-1]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
