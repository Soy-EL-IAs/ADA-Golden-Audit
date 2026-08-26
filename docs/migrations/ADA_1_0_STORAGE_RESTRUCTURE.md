# ADA 1.0 Storage Restructure

Date: 2026-08-25/26  
Repository: `D:\IA\Ada`  
Golden E2E: intentionally not executed

## Status

Code, storage, Library ownership, current runs, references, workflows, tests and documentation were migrated. No productive source image was deleted. After explicit authorization, inherited ACLs were restored only on the identified test residues; their contents were inspected again and all 47 confirmed temporary directories were removed. The final root contains 11 directories (including `.git`) and 4 files.

## Root Before

The root contained 97 top-level elements: 63 directories and 34 files. Product code competed with 12 dispersed run/validation roots, 29 leaked test sandboxes, caches, scratch/dummy content, generated snapshots, loose patch scripts, raw renderer history and ambiguous data locations.

### Automatic inventory classification

| Original root element | Classification | Evidence / dependency | Disposition |
|---|---|---|---|
| `ada_app/` | ACTIVE_SOURCE | FastAPI, UI, mission and Library implementation | retained |
| `scripts/` | ACTIVE_SOURCE / ONE_SHOT_TOOL | imported by `ada_app` and operators | retained; loose root tools classified separately |
| `config/` | ACTIVE_CONFIG | runtime loaders and model/pipeline config | retained; historical Klein configs moved |
| `schemas/` | ACTIVE_CONFIG | contract validation | retained |
| `tests/` | TEST_SOURCE / TEST_ARTIFACT | unittest sources plus three old temp dirs | retained; legacy root tests separated and temp residues removed |
| `workflows/` | ACTIVE_CONFIG / EXPERIMENTAL / LEGACY | explicit loader paths and workflow tests | split into production/experimental/legacy |
| `data/` | ACTIVE_RUNTIME_DATA / ACTIVE_DATASET | missions, character DB, old Library index, reinterpretations | normalized under authoritative subroots |
| `character_refs/` | ACTIVE_DATASET | catalog manifests, Visual Review and fallback loaders | `data/references/` |
| `experimental_runs/` | ACTIVE_RUNTIME_DATA / EXPERIMENTAL | current M2 mission adapter plus Model Lab and prototypes | split between `data/runs/missions/` and `experimental/` |
| `runs/` | LEGACY | old Illustrious/Krea pipeline manifests and assets | `legacy/runs/pre-ada-root-runs/` |
| `full_pipeline_runs/` | LEGACY | deprecated specialist pipeline | `legacy/runs/full-pipeline/` |
| `visual_review_runs/` | AUDIT_EVIDENCE / LEGACY | historical review benchmarks | `legacy/runs/visual-review/` |
| `e2e_runs/` | LEGACY | historical specialist E2E evidence | `legacy/runs/e2e/` |
| `evolution_runs/` | LEGACY | historical evolution cycles | `legacy/runs/evolution/` |
| `render_only_runs/` | LEGACY | historical renderer assets/manifests | `legacy/runs/render-only/` |
| `balanced_default_validations/` | AUDIT_EVIDENCE / LEGACY | historical validation set | `legacy/runs/balanced-default-validations/` |
| `klein_ab_tests/` | LEGACY | deprecated Klein experiment | `legacy/runs/klein/ab-tests/` |
| `klein_batch_runs/` | LEGACY | deprecated Klein batch artifacts | `legacy/runs/klein/batch/` |
| `klein_comparisons/` | LEGACY | deprecated Klein comparison evidence | `legacy/runs/klein/comparisons/` |
| `character_dataset_staging/` | LEGACY | historical staging manifests | `legacy/datasets/character-dataset-staging/`; new staging uses `data/tmp/` |
| `premises/`, `prompts/` | LEGACY | inputs for old pipeline tooling | `legacy/artifacts/` |
| `migration/` | AUDIT_EVIDENCE / ONE_SHOT_TOOL | prior migration evidence and scripts | `legacy/migrations/pre-ada-1-storage/` |
| `analysis/` | DOCUMENTATION | audits/roadmap/capability reports | `docs/audit/analysis/` |
| `audit_evidence/` | AUDIT_EVIDENCE | UI screenshots | `docs/audit/evidence/` |
| `assets/` | LEGACY | old generated asset placeholder | `legacy/assets/` |
| `search/` | ACTIVE_CONFIG | SearXNG service config | `config/services/search/` |
| `scratch/` | TEMPORARY / UNKNOWN | diagnostic fragments preserved by doubt | `legacy/scratch/` |
| `dummy_tmp/` | TEST_ARTIFACT / TEMPORARY | 14-byte deliberately corrupt fixture plus empty test directories | inspected and removed |
| `.obsidian/` | ACTIVE_CONFIG | local editor state | `config/editor/obsidian/` |
| `__pycache__/`, `*.pyc` | CACHE | Python bytecode | removed where accessible |
| 23 `ada-character-onboarding-*` directories | TEST_ARTIFACT | exact test prefix; verified 0 files/0 bytes | removed after scoped ACL repair |
| 6 `ada-mission-delete-*` directories | TEST_ARTIFACT | exact test prefix; verified 0 files/0 bytes | removed after scoped ACL repair |
| `ada.py`, `START_ADA_APP.cmd` | ACTIVE_SOURCE | application launchers | retained/replaced with ADA 1.0 entry point |
| `README.md` | DOCUMENTATION | repository onboarding | archived and rewritten |
| `.gitignore` | ACTIVE_CONFIG | workspace hygiene | rewritten |
| `run_production.py`, `run_recovery.py`, `run_smoke.py` | ONE_SHOT_TOOL / maintained launcher | manual operators | `scripts/launchers/` |
| `debug.py`, `extract.py`, `fix_*.py`, `patch_*.py`, `update_*.py` | ONE_SHOT_TOOL | historical patch/debug scripts, no product imports | `legacy/tools/root-patches/` |
| root `test_*.py`, `tests_*.py` | TEST_SOURCE / LEGACY | mixed current and old manual tests | current tests under `tests/`; stale/live scripts under `legacy/tests/` |
| `lmstudio_mcp_*.json` | ACTIVE_CONFIG | local MCP launch config | `config/lmstudio/` |
| `comfy_history.json` | AUDIT_EVIDENCE | renderer history/provenance | `legacy/provenance/` |
| `tree.txt` | CACHE | generated filesystem snapshot | deleted |
| `HANDOFF_TO_LUNA.md`, `README_ADA.md`, `LOCAL_OPERATOR_README.md` | DOCUMENTATION | historical/operations docs | `docs/archive/` and `docs/operations/` |
| `with semantic roles…` | UNKNOWN | ambiguous fragment | preserved under `legacy/fragments/` |

## Authoritative Layout

```text
data/
├── characters/       # catalog.json, taxonomy, heroes
├── missions/         # mission state
├── library/          # authoritative ADA dataset
├── references/       # canonical character references
├── runs/             # current product runs
│   ├── missions/
│   ├── renderer/
│   ├── stock/
│   └── reviews/
├── indexes/
└── tmp/
```

All production roots resolve through `scripts/ada_paths.py`, with environment and `config/ada.local.json` overrides. New product writers do not target `legacy/`.

## Library Migration and Image Ownership

Pre-migration Library state was 116 derived index records plus 3 explicitly registered reinterpretations: 119 logical assets. Every source image existed.

The migration adopted each image into content-addressed storage:

```text
data/library/assets/sha256/<hash-prefix>/<sha256>.<extension>
```

Each record now contains `storage_provenance` with owner, storage version, SHA-256, byte size, managed path, original ComfyUI path, adoption timestamp and copy-verification result. `data/library/records/` contains one durable metadata snapshot per asset. `index.json` now contains all 119 records; `explicit_images.json` remains as a compatibility source for the three historical explicit registrations.

Results from `data/library/migration_manifest.json`:

- assets before: 119
- assets after: 119
- source images found: 119
- source images missing: 0
- hashes verified: 119
- unique managed blobs: 119
- failures: 0
- originals deleted: 0
- review state SHA-256 before/after: identical (`520b90bff3c35634d5f7fb20816f2947672f91b1a38c39fc907507f38da8fe76`)

Future index rebuilds and reinterpretation registrations call `ada_app.managed_assets.adopt_library_record` before publishing records. Identical pixels share one SHA-256 blob.

## Moved

| Old path | New path |
|---|---|
| `data/asset_library/` | `data/library/` |
| `data/character_db/` | `data/characters/` |
| `config/characters.json` | `data/characters/catalog.json` |
| `character_refs/` | `data/references/` |
| `data/reinterpretations/` | `data/runs/renderer/reinterpretations/` |
| `experimental_runs/m2_fast_creative_expansion/` | `data/runs/missions/` |
| `experimental_runs/model_lab/` | `experimental/model_lab/` |
| remaining `experimental_runs/*` | `experimental/runs/` |
| `runs/` | `legacy/runs/pre-ada-root-runs/` |
| `full_pipeline_runs/` | `legacy/runs/full-pipeline/` |
| `e2e_runs/` | `legacy/runs/e2e/` |
| `evolution_runs/` | `legacy/runs/evolution/` |
| `render_only_runs/` | `legacy/runs/render-only/` |
| `visual_review_runs/` | `legacy/runs/visual-review/` |
| `balanced_default_validations/` | `legacy/runs/balanced-default-validations/` |
| `klein_ab_tests/` | `legacy/runs/klein/ab-tests/` |
| `klein_batch_runs/` | `legacy/runs/klein/batch/` |
| `klein_comparisons/` | `legacy/runs/klein/comparisons/` |
| `character_dataset_staging/` | `legacy/datasets/character-dataset-staging/` |
| `premises/`, `prompts/` | `legacy/artifacts/` |
| `migration/` | `legacy/migrations/pre-ada-1-storage/` |
| `analysis/` | `docs/audit/analysis/` |
| `audit_evidence/` | `docs/audit/evidence/` |
| `docs/audits/` | `docs/audit/historical/` |
| `search/` | `config/services/search/` |
| `.obsidian/` | `config/editor/obsidian/` |
| root patch/debug scripts | `legacy/tools/root-patches/` |
| root maintained run scripts | `scripts/launchers/` |
| old root test scripts | `legacy/tests/root-scripts/` |
| `assets/`, `scratch/`, raw history/fragments | corresponding `legacy/` categories |

File-count checks matched every material moved tree. The prior migration tree reports 13 files instead of 15 because its two `__pycache__` files were intentionally removed.

## Workflows

`workflows/production/` contains exactly three current product graphs:

- `lustify_krea2_primary_v1_api.json`
- `lustify_krea2_img2img_v1_api.json`
- `miaomiao_anima16_secondary_v1_api.json`

Illustrious/Klein graphs are under `workflows/legacy/specialist/`. Reusable/unvalidated graphs and MiniMax F2V are under `workflows/experimental/`. `renderer_workflow_path` rejects any production preset resolving outside `workflows/production/`.

## Compatibility

- New writes use authoritative roots only.
- Current run readers use `data/runs/missions/`.
- Historical tools resolve the corresponding `legacy/` roots through compatibility constants.
- Library records retain raw ComfyUI paths as provenance but display/review the managed ADA copy.
- Source run roots in Library metadata were rewritten to current locations while `layout_provenance.legacy_source_artifact_root` preserves the former path.
- Reference manifests and character contracts were rewritten to `data/references/`.
- 36 absolute active configuration/data paths were checked; 0 were broken.

## Test Temp Leak

Current onboarding, mission-delete, profile-safety, managed-storage and hard-rating tests create UUID sandboxes under `data/tmp/tests/` using inherited directory permissions and register recursive cleanup. They no longer create temp directories in the repository root or use `tempfile.mkdtemp`, which produced malformed ACLs on this Windows environment.

The prior malformed-ACL residues were repaired only after explicit authorization, re-inspected, and removed. A post-validation scan found zero root leaks, zero `tests/tmp*` directories and zero leaked sandboxes under `data/tmp/tests/`.

## Deleted

Only demonstrably regenerable content was removed:

- accessible `__pycache__/` directories and `.pyc` files;
- `tree.txt` generated filesystem snapshot;
- empty `experimental_runs/` container after all children were moved;
- two cached bytecode files inside the prior migration tree;
- 46 empty test-residue directories: 29 in the root, 14 under `data/tmp/tests/`, and 3 under `tests/`;
- `dummy_tmp/`, containing only a deliberately corrupt 14-byte test fixture and empty test subtrees;
- 5 `__pycache__/` directories regenerated by final compilation validation.

No source image, rating, review, reference, mission, manifest, receipt, provenance record or historical run was deleted.

## Validation

- `python ada.py paths` — passed.
- `python ada.py check` — passed; 119 Library assets and 88 missions loaded.
- `python -m unittest discover -s tests -p "test_*.py" -q` — 68 tests passed; no GPU renders.
- `python -m compileall -q ada.py ada_app scripts tests` — passed; generated bytecode caches were removed afterward.
- `python scripts/validate_storage.py` — passed:
  - 119/119 Library hashes verified;
  - 119/119 images opened with Pillow;
  - 88/88 missions parsed;
  - 12 characters loaded;
  - 8 active reference manifests and 18 referenced images verified;
  - 12 registered characters resolve a cover;
  - 0 broken Library/source paths.
- Post-validation hygiene scan — 0 root test leaks, 0 `tests/tmp*` leaks, 0 `data/tmp/tests` leaks, 0 `__pycache__`, 0 `.pyc`.

Two stored hero IDs point to non-visible assets. This historical state is preserved; the catalog safely ignores them and resolves working fallback covers.

## Remaining Issues / Preserved by Doubt

- Historical absolute paths inside `legacy/` are intentionally preserved as evidence and may describe machines/locations that no longer exist.
- Hard Re-Evaluation history count is currently zero; the persistence behavior is covered by a passing unit test and no history was invented.
- Two historical hero IDs refer to assets that are no longer visible. They were preserved rather than rewritten; the catalog safely ignores them and resolves valid fallback covers.

## Data Integrity Decision

The productive dataset and metadata pass integrity checks: 119 before, 119 after, 119 hashes verified, 0 failed, ratings unchanged, originals preserved. The root-cleanliness acceptance criterion is met. The repository is ready for the ADA 1.0 Alpha Golden E2E; that run was intentionally not executed as part of this migration.

## Root After

```text
.git/
.gitignore
ada_app/
ada.py
config/
data/
docs/
experimental/
legacy/
README.md
schemas/
scripts/
START_ADA_APP.cmd
tests/
workflows/
```
