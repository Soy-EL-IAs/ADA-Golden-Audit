#!/usr/bin/env python3
"""Canonical loader for ADA character-reference manifests.

Schema-v1 manifests exposed references as ``refs``.  Schema v2 renamed the
field to ``canonical_references``.  All readers normalize once at this
boundary and consume only ``canonical_references`` afterwards.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def normalize_character_reference_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Return a copy with one authoritative ``canonical_references`` list."""
    if not isinstance(manifest, dict):
        raise ValueError("character reference manifest must be an object")
    canonical = manifest.get("canonical_references")
    legacy = manifest.get("refs")
    if isinstance(canonical, list):
        references = canonical
    elif isinstance(legacy, list):
        references = legacy
    else:
        references = []
    normalized = dict(manifest)
    normalized["canonical_references"] = list(references)
    return normalized


def load_character_reference_manifest(path: Path) -> dict[str, Any]:
    """Load and normalize a manifest without mutating its historical file."""
    value = json.loads(path.read_text(encoding="utf-8"))
    return normalize_character_reference_manifest(value)
