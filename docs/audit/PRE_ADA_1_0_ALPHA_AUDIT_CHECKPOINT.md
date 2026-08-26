# Pre-ADA 1.0 Alpha audit checkpoint

Captured: 2026-08-25, America/Buenos_Aires.

## Git state

- Current branch at capture: `master`.
- Current commit: `3585055e39b2d4c8bcb08a004eb17704cb46c7a6`.
- Commit date: `2026-08-22T15:36:07-03:00`.
- Commit subject: `replace hardcoded ComfyUI bindings with semantic roles`.
- Protective branch created at that commit: `pre-ada-1.0-alpha-audit`.
- Working tree at capture: **dirty**.
- Porcelain entries: 3,376 total: 3,314 untracked, 58 modified, 4 deleted.
- The protective branch records the committed ancestor only. It does **not** pretend to contain the dirty working tree.

The working files and generated/runtime data remain physically in place. No cleanup, move, reset, stash or deletion was performed during this checkpoint. Before any later destructive cleanup, active source changes must be committed and generated evidence must either remain in place or be explicitly archived.

## Main dirty groups

| Root | Entries seen by Git | Initial interpretation |
|---|---:|---|
| `experimental_runs/` | 2,348 | Generated experiment artifacts |
| `runs/` | 425 | Historical/local run state |
| `data/` | 100 | Active runtime state |
| `character_refs/` | 98 | Active identity data plus failed/staging evidence |
| `full_pipeline_runs/` | 93 | Pipeline evidence/history |
| `scripts/` | 69 | Active and historical code mixed with Python caches |
| `ada_app/` | 48 | Active application source; currently untracked |
| `schemas/` | 35 | Active contracts; currently mostly untracked |
| `tests/` | 28 | Tests plus inaccessible temporary folders |
| `config/` | 26 | Active configuration plus experimental presets |
| `visual_review_runs/` | 21 | Review evidence |
| `workflows/` | 20 | Production, constructors/finalizers and legacy graphs |
| `docs/` | 16 | Current, historical and audit documents |

Git also reported inaccessible temporary directories matching `ada-character-onboarding-*`, `ada-mission-delete-*`, `tests/tmp*` and one subtree under `dummy_tmp/`. They are classified as `TEMPORARY / NEEDS_REVIEW` until their creator and recovery value are confirmed.

## Runtime captured

| Service | Address | State at capture |
|---|---|---|
| ADA API/UI | `127.0.0.1:8000` | Listening |
| ComfyUI | `127.0.0.1:8188` | Listening; queue empty |
| LM Studio | `127.0.0.1:1234` | Listening; no loaded model instance reported |

The immediately preceding interrupted Stock batch completed in background. Recent missions included completed Stock runs for Tifa Lockhart, Nanally NTE and Jill Valentine, followed by two completed three-image scene missions for Tifa and 2B. These are runtime artifacts and were not overwritten.

## Toolchain and dependency snapshot

- Python `3.12.10`.
- Node.js `v25.2.1`.
- FastAPI `0.115.6`.
- Uvicorn `0.35.0`.
- Pydantic `2.13.4`.
- filelock `3.20.0`.
- jsonschema `4.25.1`.
- Pillow `11.0.0`.
- Requests `2.32.5`.
- PyTorch `2.10.0+cu130`.

No root `.gitignore`, dependency lockfile, `requirements.txt` or `pyproject.toml` was present at capture. This is a release-hygiene issue, not evidence that dependencies are absent.

## Active configuration roots

- Agent/VRAM roles: `config/orchestration.json`.
- Renderer/workflow/model settings: `config/pipeline.json`.
- Active product profile: `config/production_profiles.json` (`lustify_primary`).
- Model registry: `config/models_registry.json`.
- Local machine paths: `config/ada.local.json`; must not be treated as a portable release file.
- Character metadata and references: `config/characters.json`, `config/character_refs.json` and `character_refs/`.

## Recovery boundary

The safe recovery points are deliberately explicit:

1. `pre-ada-1.0-alpha-audit` restores the last committed ancestor.
2. The current working tree preserves all pre-audit source and runtime files in place.
3. No generated/history directory may be deleted merely to obtain a clean `git status`.
4. A clean final release requires classification plus ignore/tracking policy, not filesystem erasure.

