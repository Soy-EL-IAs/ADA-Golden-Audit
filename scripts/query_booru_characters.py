#!/usr/bin/env python3
"""Read-only local lookup utility for Sn0w123/booru-characters."""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import CHARACTER_DB_ROOT
else:
    from ada_paths import CHARACTER_DB_ROOT


DEFAULT_DATASET = CHARACTER_DB_ROOT / "booru_characters" / "characters.jsonl"


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower().replace("_", " ")).strip()


def load_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        if not isinstance(record, dict):
            raise ValueError(f"{path}:{line_number}: record must be an object")
        records.append(record)
    return records


def score_candidate(record: dict[str, Any], query: str, copyright_query: str | None) -> int:
    name = normalized(str(record.get("name", "")))
    query_tokens = set(normalized(query).split())
    name_tokens = set(name.split())
    score = 0
    if name == normalized(query):
        score += 1000
    elif name.startswith(normalized(query) + " "):
        score += 800
    score += 100 * len(query_tokens & name_tokens)

    if copyright_query:
        copyright_tokens = set(normalized(copyright_query).split())
        record_copyright = " ".join(normalized(str(item)) for item in record.get("copyright", []))
        score += 80 * len(copyright_tokens & set(record_copyright.split()))
        if normalized(copyright_query) in record_copyright:
            score += 400
    return score


def candidates(records: list[dict[str, Any]], query: str, copyright_query: str | None, limit: int) -> list[dict[str, Any]]:
    query_tokens = set(normalized(query).split())
    copyright_tokens = set(normalized(copyright_query or "").split())
    matches: list[tuple[int, dict[str, Any]]] = []
    for record in records:
        name_tokens = set(normalized(str(record.get("name", ""))).split())
        series_tokens = set(
            token
            for item in record.get("copyright", [])
            for token in normalized(str(item)).split()
        )
        if not (query_tokens & name_tokens) and not (copyright_tokens & series_tokens):
            continue
        score = score_candidate(record, query, copyright_query)
        if score:
            matches.append((score, record))
    matches.sort(key=lambda item: (-item[0], -int(item[1].get("post_count", 0)), str(item[1].get("name", ""))))
    return [{"score": score, "record": record} for score, record in matches[:limit]]


def normalize_record(record: dict[str, Any], records_by_id: dict[int, dict[str, Any]]) -> dict[str, Any]:
    relationships = record.get("relationships") or {}
    related_tags = {
        relation: [
            records_by_id[related_id]["name"]
            for related_id in related_ids
            if related_id in records_by_id
        ]
        for relation, related_ids in relationships.items()
        if isinstance(related_ids, list)
    }
    return {
        "canonical_tag": record.get("name"),
        "post_count": record.get("post_count"),
        "gender": record.get("gender"),
        "copyright": record.get("copyright", []),
        "appearance_characteristics": record.get("characteristics", []),
        "clothing_outfit_tags": record.get("clothing", []),
        "relationship_ids": relationships,
        "related_character_tags": related_tags,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--query", required=True)
    parser.add_argument("--copyright")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 20:
        raise ValueError("limit must be between 1 and 20")

    started = time.perf_counter()
    records = load_records(args.dataset)
    load_ms = (time.perf_counter() - started) * 1000
    by_id = {int(record["id"]): record for record in records if isinstance(record.get("id"), int)}

    started = time.perf_counter()
    found = candidates(records, args.query, args.copyright, args.limit)
    lookup_ms = (time.perf_counter() - started) * 1000
    selected = found[0]["record"] if found else None
    output = {
        "dataset": str(args.dataset),
        "record_count": len(records),
        "query": args.query,
        "copyright_query": args.copyright,
        "load_milliseconds": round(load_ms, 3),
        "lookup_milliseconds": round(lookup_ms, 3),
        "candidates": [
            {
                "score": item["score"],
                "canonical_tag": item["record"].get("name"),
                "copyright": item["record"].get("copyright", []),
                "post_count": item["record"].get("post_count"),
            }
            for item in found
        ],
        "selected_raw": selected,
        "selected_normalized": normalize_record(selected, by_id) if selected else None,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
