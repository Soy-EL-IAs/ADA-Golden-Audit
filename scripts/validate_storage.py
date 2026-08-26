#!/usr/bin/env python3
"""Read-only structural and data-integrity smoke test for ADA storage."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ADA_ROOT_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ADA_ROOT_PATH))

from ada_app.asset_library import AssetLibrary
from ada_app.character_capabilities import build_character_catalog
from scripts.ada_paths import (
    ADA_ROOT, CHARACTERS_ROOT, LIBRARY_ASSETS_ROOT, LIBRARY_ROOT,
    MISSIONS_ROOT, REFERENCES_ROOT,
)
from scripts.character_reference_manifest import normalize_character_reference_manifest


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    index = read_json(LIBRARY_ROOT / "index.json")
    reviews = read_json(LIBRARY_ROOT / "asset_review.json")
    catalog = read_json(CHARACTERS_ROOT / "catalog.json")
    heroes_path = CHARACTERS_ROOT / "heroes.json"
    heroes = read_json(heroes_path) if heroes_path.is_file() else {}
    runtime_assets = AssetLibrary().get_assets()

    asset_ids = [item.get("asset_id") for item in index]
    if len(index) != len(set(asset_ids)):
        failures.append("Library index contains duplicate or missing asset IDs")
    image_failures = 0
    hashes_verified = 0
    images_opened = 0
    try:
        from PIL import Image
    except ImportError:
        Image = None

    for item in index:
        path = Path(str(item.get("full_image_path") or ""))
        storage = item.get("storage_provenance", {})
        expected = storage.get("sha256") if isinstance(storage, dict) else None
        try:
            path.resolve().relative_to(LIBRARY_ASSETS_ROOT.resolve())
            if not path.is_file() or not isinstance(expected, str) or sha256(path) != expected:
                raise ValueError("missing image or hash mismatch")
            hashes_verified += 1
            if Image is not None:
                with Image.open(path) as image:
                    image.verify()
                images_opened += 1
        except Exception as exc:
            image_failures += 1
            failures.append(f"{item.get('asset_id')}: {exc}")
        artifact_root = item.get("source_artifact_root")
        if artifact_root and not Path(str(artifact_root)).is_dir():
            failures.append(f"{item.get('asset_id')}: missing source_artifact_root")

    reference_manifests = 0
    reference_images = 0
    for name, entry in catalog.items():
        if not isinstance(entry, dict) or not entry.get("refs_manifest"):
            continue
        manifest_path = ADA_ROOT / str(entry["refs_manifest"])
        if not manifest_path.is_file():
            failures.append(f"{name}: missing reference manifest")
            continue
        reference_manifests += 1
        manifest = normalize_character_reference_manifest(read_json(manifest_path))
        refs = manifest["canonical_references"]
        for ref in refs if isinstance(refs, list) else []:
            image_path = manifest_path.parent / str(ref.get("file") or "")
            if not image_path.is_file():
                failures.append(f"{name}: missing reference image {image_path}")
                continue
            expected = ref.get("sha256")
            if isinstance(expected, str) and len(expected) == 64 and sha256(image_path) != expected:
                failures.append(f"{name}: reference hash mismatch {image_path}")
                continue
            reference_images += 1

    visible_ids = {item["asset_id"] for item in runtime_assets if item.get("is_visible_library_asset")}
    broken_heroes = {name: asset_id for name, asset_id in heroes.items() if asset_id not in visible_ids}
    if broken_heroes:
        warnings.append(f"stale character heroes safely ignored: {broken_heroes}")
    character_catalog = build_character_catalog(catalog, runtime_assets, heroes)

    mission_files = sorted(MISSIONS_ROOT.glob("mission_*.json"))
    parsed_missions = 0
    for path in mission_files:
        try:
            if isinstance(read_json(path), dict):
                parsed_missions += 1
        except Exception as exc:
            failures.append(f"invalid mission {path.name}: {exc}")

    review_values = reviews.values() if isinstance(reviews, dict) else []
    hard_history_entries = sum(
        len(review.get("hard_rating_history", []))
        for review in review_values if isinstance(review, dict) and isinstance(review.get("hard_rating_history", []), list)
    )
    report = {
        "status": "ok" if not failures else "failed",
        "library_assets": len(index),
        "runtime_library_assets": len(runtime_assets),
        "unique_asset_ids": len(set(asset_ids)),
        "hashes_verified": hashes_verified,
        "images_opened": images_opened,
        "image_failures": image_failures,
        "review_records": len(reviews) if isinstance(reviews, dict) else 0,
        "hard_rating_history_entries": hard_history_entries,
        "characters": len(catalog) if isinstance(catalog, dict) else 0,
        "reference_manifests": reference_manifests,
        "reference_images_verified": reference_images,
        "missions": len(mission_files),
        "missions_parsed": parsed_missions,
        "heroes": len(heroes) if isinstance(heroes, dict) else 0,
        "characters_with_cover": sum(1 for item in character_catalog if item.get("registered") and item.get("has_cover")),
        "stale_heroes_safely_ignored": len(broken_heroes),
        "warnings": warnings,
        "failures": failures,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
