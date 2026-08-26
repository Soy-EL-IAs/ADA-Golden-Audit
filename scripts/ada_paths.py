#!/usr/bin/env python3
"""Central path and endpoint resolution for ADA.

Precedence is environment, machine-local config, then project-derived or
existing portable defaults.  Importing this module performs no I/O outside
small JSON config reads and creates no directories.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


_PHYSICAL_ROOT = Path(__file__).resolve().parents[1]


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError, json.JSONDecodeError):
        return {}


def _env_path(name: str) -> Path | None:
    value = os.environ.get(name, "").strip()
    return Path(value).expanduser().resolve() if value else None


ADA_ROOT = _env_path("ADA_ROOT") or _PHYSICAL_ROOT
CONFIG_ROOT = ADA_ROOT / "config"
_LOCAL = _read_json(CONFIG_ROOT / "ada.local.json")
_PIPELINE = _read_json(CONFIG_ROOT / "pipeline.json")
_ORCHESTRATION = _read_json(CONFIG_ROOT / "orchestration.json")

def _storage_path(env_name: str, local_name: str, default: Path) -> Path:
    """Resolve one writable storage root without scattering machine paths."""
    configured = _env_path(env_name)
    if configured is not None:
        return configured
    local_value = _LOCAL.get(local_name)
    if isinstance(local_value, str) and local_value.strip():
        candidate = Path(local_value).expanduser()
        return (candidate if candidate.is_absolute() else ADA_ROOT / candidate).resolve()
    return default.resolve()


DATA_ROOT = _storage_path("ADA_DATA_ROOT", "data_root", ADA_ROOT / "data")
CHARACTERS_ROOT = _storage_path("ADA_CHARACTERS_ROOT", "characters_root", DATA_ROOT / "characters")
MISSIONS_ROOT = _storage_path("ADA_MISSIONS_ROOT", "missions_root", DATA_ROOT / "missions")
LIBRARY_ROOT = _storage_path("ADA_LIBRARY_ROOT", "library_root", DATA_ROOT / "library")
LIBRARY_ASSETS_ROOT = LIBRARY_ROOT / "assets"
LIBRARY_RECORDS_ROOT = LIBRARY_ROOT / "records"
RUNS_ROOT = _storage_path("ADA_RUNS_ROOT", "runs_root", DATA_ROOT / "runs")
MISSION_RUNS_ROOT = RUNS_ROOT / "missions"
RENDERER_RUNS_ROOT = RUNS_ROOT / "renderer"
STOCK_RUNS_ROOT = RUNS_ROOT / "stock"
REVIEW_RUNS_ROOT = RUNS_ROOT / "reviews"
REFERENCES_ROOT = _storage_path("ADA_REFERENCES_ROOT", "references_root", DATA_ROOT / "references")
INDEXES_ROOT = _storage_path("ADA_INDEXES_ROOT", "indexes_root", DATA_ROOT / "indexes")
TMP_ROOT = _storage_path("ADA_TMP_ROOT", "tmp_root", DATA_ROOT / "tmp")
LOCKS_ROOT = TMP_ROOT / "locks"
WORKFLOWS_ROOT = ADA_ROOT / "workflows"
EXPERIMENTAL_ROOT = ADA_ROOT / "experimental"
LEGACY_ROOT = ADA_ROOT / "legacy"

# Current product aliases retained for callers that predate the ADA 1.0 names.
CHARACTER_REFS_ROOT = REFERENCES_ROOT
CHARACTER_DATASET_STAGING_ROOT = TMP_ROOT / "character_dataset_staging"
CHARACTER_DB_ROOT = CHARACTERS_ROOT
GENERATED_ASSETS_ROOT = LIBRARY_ASSETS_ROOT

# Read-only historical locations. New production code must never write here.
LEGACY_RUNS_ROOT = LEGACY_ROOT / "runs"
PROMPTS_ROOT = LEGACY_ROOT / "artifacts" / "prompts"
PREMISES_ROOT = LEGACY_ROOT / "artifacts" / "premises"
ASSETS_ROOT = LEGACY_ROOT / "assets"
KLEIN_BATCH_RUNS_ROOT = LEGACY_RUNS_ROOT / "klein" / "batch"
VISUAL_REVIEW_RUNS_ROOT = LEGACY_RUNS_ROOT / "visual-review"
RENDER_ONLY_RUNS_ROOT = LEGACY_RUNS_ROOT / "render-only"
KLEIN_AB_TESTS_ROOT = LEGACY_RUNS_ROOT / "klein" / "ab-tests"

_comfy_default = _LOCAL.get("comfyui_root") or _PIPELINE.get("comfy_root")
COMFYUI_ROOT = _env_path("ADA_COMFYUI_ROOT") or (Path(_comfy_default).resolve() if _comfy_default else None)
LMSTUDIO_BASE_URL = os.environ.get(
    "ADA_LMSTUDIO_URL",
    os.environ.get("LM_STUDIO_URL", _LOCAL.get("lmstudio_base_url") or _ORCHESTRATION.get("lm_studio_url") or
                   "http://127.0.0.1:1234"),
).rstrip("/")
COMFYUI_BASE_URL = os.environ.get(
    "ADA_COMFYUI_URL", _LOCAL.get("comfyui_base_url") or _PIPELINE.get("server_url") or
    "http://127.0.0.1:8188",
).rstrip("/")

_legacy_root = _LOCAL.get("legacy_project_root")
LEGACY_PROJECT_ROOT = Path(_legacy_root).resolve() if _legacy_root else None


def project_path(*parts: str) -> Path:
    return ADA_ROOT.joinpath(*parts)


def resolve_legacy_path(value: str | Path) -> Path:
    """Map copied historical project paths to Ada without rewriting history."""
    path = Path(value)
    if not path.is_absolute():
        return (ADA_ROOT / path).resolve()
    if LEGACY_PROJECT_ROOT is not None:
        try:
            relative = path.resolve().relative_to(LEGACY_PROJECT_ROOT)
        except ValueError:
            pass
        else:
            candidate = (ADA_ROOT / relative).resolve()
            if candidate.exists():
                return candidate
    return path.resolve()


def path_summary() -> dict[str, str | None]:
    return {
        "ada_root": str(ADA_ROOT), "data_root": str(DATA_ROOT),
        "characters_root": str(CHARACTERS_ROOT), "missions_root": str(MISSIONS_ROOT),
        "library_root": str(LIBRARY_ROOT), "library_assets_root": str(LIBRARY_ASSETS_ROOT),
        "runs_root": str(RUNS_ROOT), "mission_runs_root": str(MISSION_RUNS_ROOT),
        "references_root": str(REFERENCES_ROOT), "indexes_root": str(INDEXES_ROOT),
        "tmp_root": str(TMP_ROOT), "workflows_root": str(WORKFLOWS_ROOT),
        "legacy_root": str(LEGACY_ROOT), "experimental_root": str(EXPERIMENTAL_ROOT),
        "assets_root": str(ASSETS_ROOT), "prompts_root": str(PROMPTS_ROOT),
        "character_refs_root": str(CHARACTER_REFS_ROOT),
        "character_dataset_staging_root": str(CHARACTER_DATASET_STAGING_ROOT),
        "klein_batch_runs_root": str(KLEIN_BATCH_RUNS_ROOT),
        "visual_review_runs_root": str(VISUAL_REVIEW_RUNS_ROOT),
        "character_db_root": str(CHARACTER_DB_ROOT),
        "generated_assets_root": str(GENERATED_ASSETS_ROOT),
        "comfyui_root": str(COMFYUI_ROOT) if COMFYUI_ROOT else None,
        "lmstudio_base_url": LMSTUDIO_BASE_URL, "comfyui_base_url": COMFYUI_BASE_URL,
    }
