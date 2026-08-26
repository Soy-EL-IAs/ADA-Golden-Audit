#!/usr/bin/env python3
"""One-shot, non-destructive ADA 1.0 Library ownership migration."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ADA_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ADA_ROOT))

from ada_app.managed_assets import adopt_library_record, verify_managed_record
from scripts.ada_paths import LIBRARY_ROOT


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


PATH_MOVES = [
    (ADA_ROOT / "experimental_runs" / "m2_fast_creative_expansion", ADA_ROOT / "data" / "runs" / "missions"),
    (ADA_ROOT / "data" / "reinterpretations", ADA_ROOT / "data" / "runs" / "renderer" / "reinterpretations"),
]


def remap_text(value: str) -> str:
    normalized = os.path.normcase(value)
    for old, new in PATH_MOVES:
        old_text = str(old.resolve())
        if normalized == os.path.normcase(old_text) or normalized.startswith(os.path.normcase(old_text + os.sep)):
            return str(new.resolve()) + value[len(old_text):]
        old_relative = old.relative_to(ADA_ROOT).as_posix()
        if value == old_relative or value.startswith(old_relative + "/"):
            return new.relative_to(ADA_ROOT).as_posix() + value[len(old_relative):]
    return value


def remap(value: Any) -> Any:
    if isinstance(value, str):
        return remap_text(value)
    if isinstance(value, list):
        return [remap(item) for item in value]
    if isinstance(value, dict):
        return {key: remap(item) for key, item in value.items()}
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def migrate() -> dict[str, Any]:
    index_path = LIBRARY_ROOT / "index.json"
    explicit_path = LIBRARY_ROOT / "explicit_images.json"
    reviews_path = LIBRARY_ROOT / "asset_review.json"
    indexed = json.loads(index_path.read_text(encoding="utf-8"))
    explicit = json.loads(explicit_path.read_text(encoding="utf-8")) if explicit_path.is_file() else []
    if not isinstance(indexed, list) or not all(isinstance(item, dict) for item in indexed):
        raise ValueError("Library index must be a list of records")
    explicit_by_id = {item.get("asset_id"): item for item in explicit if isinstance(item, dict) and item.get("asset_id")}
    assets = [item for item in indexed if item.get("asset_id") not in explicit_by_id] + list(explicit_by_id.values())

    ids = [str(item.get("asset_id") or "") for item in assets]
    sources = [Path(str(item.get("full_image_path") or "")) for item in assets]
    if len(ids) != len(set(ids)) or any(not asset_id for asset_id in ids):
        raise ValueError("Library index contains missing or duplicate asset IDs")
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Refusing migration; {len(missing)} Library source images are missing")

    review_sha_before = sha256(reviews_path) if reviews_path.is_file() else None
    source_hashes = {asset_id: sha256(path) for asset_id, path in zip(ids, sources)}
    migrated: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for record in assets:
        try:
            legacy_artifact_root = record.get("source_artifact_root")
            prepared = remap(record)
            if legacy_artifact_root and legacy_artifact_root != prepared.get("source_artifact_root"):
                prepared["layout_provenance"] = {
                    **(prepared.get("layout_provenance") if isinstance(prepared.get("layout_provenance"), dict) else {}),
                    "legacy_source_artifact_root": legacy_artifact_root,
                }
            adopted = adopt_library_record(prepared)
            if source_hashes[record["asset_id"]] != adopted["storage_provenance"]["sha256"]:
                raise RuntimeError("source/destination hash mismatch")
            migrated.append(adopted)
        except Exception as exc:
            failures.append({"asset_id": str(record.get("asset_id")), "error": f"{type(exc).__name__}: {exc}"})

    if failures or len(migrated) != len(assets) or not all(verify_managed_record(item) for item in migrated):
        raise RuntimeError(f"Library migration validation failed: {failures[:3]}")

    by_id = {item["asset_id"]: item for item in migrated}
    migrated_explicit = [by_id[item["asset_id"]] for item in explicit if item.get("asset_id") in by_id]
    write_json(index_path, migrated)
    write_json(explicit_path, migrated_explicit)
    review_sha_after = sha256(reviews_path) if reviews_path.is_file() else None
    if review_sha_before != review_sha_after:
        raise RuntimeError("Human review state changed during image migration")

    report = {
        "schema_version": "ada_1_0_storage_migration_v1",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "assets_before": len(assets),
        "assets_after": len(migrated),
        "derived_index_records_before": len(indexed),
        "explicit_compatibility_records": len(explicit),
        "unique_asset_ids_before": len(set(ids)),
        "unique_asset_ids_after": len({item["asset_id"] for item in migrated}),
        "source_images_found": len(sources),
        "source_images_missing": len(missing),
        "hashes_verified": len(migrated),
        "failed": len(failures),
        "unique_managed_blobs": len({item["storage_provenance"]["sha256"] for item in migrated}),
        "reviews_sha256_before": review_sha_before,
        "reviews_sha256_after": review_sha_after,
        "originals_deleted": 0,
        "failures": failures,
    }
    write_json(LIBRARY_ROOT / "migration_manifest.json", report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(migrate(), ensure_ascii=False, indent=2))
