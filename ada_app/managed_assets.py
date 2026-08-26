"""ADA-owned, content-addressed Library image storage."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.ada_paths import ADA_ROOT, LIBRARY_ASSETS_ROOT, LIBRARY_RECORDS_ROOT


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_key(value: str) -> str:
    key = re.sub(r"[^a-zA-Z0-9._-]+", "_", value).strip("._")
    return key[:180] or "asset"


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ADA_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _replace_exact(value: Any, source: str, destination: str) -> Any:
    if isinstance(value, str):
        return destination if os.path.normcase(value) == os.path.normcase(source) else value
    if isinstance(value, list):
        return [_replace_exact(item, source, destination) for item in value]
    if isinstance(value, dict):
        return {key: _replace_exact(item, source, destination) for key, item in value.items()}
    return value


def adopt_library_record(record: dict[str, Any]) -> dict[str, Any]:
    """Copy one Library image into ADA storage and return its durable record.

    Blobs are addressed by SHA-256, so two records containing identical pixels
    share one physical file. The ComfyUI path remains explicit provenance.
    """
    source_text = str(record.get("full_image_path") or record.get("thumbnail_path") or "").strip()
    source = Path(source_text)
    if not source.is_file():
        raise FileNotFoundError(f"Library source image does not exist: {source_text}")

    digest = _sha256(source)
    extension = source.suffix.lower() or ".bin"
    destination = LIBRARY_ASSETS_ROOT / "sha256" / digest[:2] / f"{digest}{extension}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if _sha256(destination) != digest:
            raise RuntimeError(f"Hash collision or corrupt Library destination: {destination}")
    else:
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        shutil.copy2(source, temporary)
        if _sha256(temporary) != digest:
            temporary.unlink(missing_ok=True)
            raise RuntimeError(f"Library copy verification failed: {source}")
        temporary.replace(destination)

    managed_path = str(destination.resolve())
    migrated = _replace_exact(deepcopy(record), source_text, managed_path)
    prior = record.get("storage_provenance") if isinstance(record.get("storage_provenance"), dict) else {}
    original_source = str(prior.get("original_source_path") or source.resolve())
    provenance = {
        **prior,
        "owner": "ADA",
        "storage_version": "ada_library_v1",
        "sha256": digest,
        "bytes": destination.stat().st_size,
        "managed_path": _relative(destination),
        "original_source_path": original_source,
        "adopted_at": prior.get("adopted_at") or datetime.now(timezone.utc).isoformat(),
        "copy_verified": True,
    }
    migrated["storage_provenance"] = provenance
    migrated["full_image_path"] = managed_path
    migrated["thumbnail_path"] = managed_path

    LIBRARY_RECORDS_ROOT.mkdir(parents=True, exist_ok=True)
    record_path = LIBRARY_RECORDS_ROOT / f"{_safe_key(str(migrated.get('asset_id') or digest))}.json"
    temp_record = record_path.with_suffix(".json.tmp")
    temp_record.write_text(json.dumps(migrated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp_record.replace(record_path)
    return migrated


def verify_managed_record(record: dict[str, Any]) -> bool:
    provenance = record.get("storage_provenance", {})
    if not isinstance(provenance, dict):
        return False
    path = Path(str(record.get("full_image_path") or ""))
    expected = str(provenance.get("sha256") or "")
    return path.is_file() and bool(re.fullmatch(r"[0-9a-f]{64}", expected)) and _sha256(path) == expected
