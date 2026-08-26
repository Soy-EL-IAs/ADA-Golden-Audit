# ADA 1.0 Alpha project inventory

Status: initial evidence-backed classification. `safe_to_delete` remains `NO` unless a consumer audit proves otherwise.

| Path | Purpose | Classification | Active | Generated | Git policy candidate | Safe to delete | Needs review |
|---|---|---|---:|---:|---|---:|---:|
| `ada_app/` | FastAPI application, UI, Library and mission pipeline | ACTIVE | Yes | No | Track | No | No |
| `config/` | Runtime roles, renderers, models, characters and presets | ACTIVE + EXPERIMENTAL | Yes | No | Track portable config; exclude local paths | No | Yes |
| `scripts/` | Headless orchestration, specialists, review, tools and experiments | ACTIVE + LEGACY | Yes | No | Track classified source; ignore caches | No | Yes |
| `schemas/` | Persisted contracts and API/agent boundaries | ACTIVE | Yes | No | Track | No | No |
| `workflows/production/` | Split and renderer-specific ComfyUI graphs | ACTIVE | Yes | No | Track | No | Yes |
| `workflows/constructors/` | Reusable constructor graphs | EXPERIMENTAL/ACTIVE | Conditional | No | Track | No | Yes |
| `workflows/finalizers/` | Reusable finalizer graphs | EXPERIMENTAL/ACTIVE | Conditional | No | Track | No | Yes |
| `workflows/legacy/` | Quarantined combined historical workflows | LEGACY | No | No | Track as historical compatibility | No | No |
| root legacy workflow JSONs | Historical chained/single-purpose graphs outside quarantine | DEPRECATED/UNKNOWN | Unknown | No | Move proposal only | No | Yes |
| `character_refs/` | Canonical identity references and manifests | ACTIVE DATA | Yes | Mixed | Track curated refs/manifests; exclude failed cache | No | Yes |
| `data/asset_library/` | Active Library index and human review state | ACTIVE RUNTIME | Yes | Yes | Preserve locally; release policy required | No | Yes |
| `data/character_db/` | Character cover/hero state | ACTIVE RUNTIME | Yes | Yes | Preserve locally; seed policy required | No | Yes |
| `data/missions/` | Mission persistence and recovery state | ACTIVE RUNTIME | Yes | Yes | Ignore runtime; keep selected golden evidence | No | Yes |
| `data/reinterpretations/` | Alternative-generation persistence | ACTIVE RUNTIME | Yes | Yes | Ignore runtime; keep selected evidence | No | Yes |
| `premises/` | Historical/generated premise datasets | TEST EVIDENCE | No | Yes | Keep curated fixtures only | No | Yes |
| `prompts/` | Historical/generated prompt datasets | TEST EVIDENCE | No | Yes | Keep curated fixtures only | No | Yes |
| `character_dataset_staging/` | Dataset preparation outputs | GENERATED | No | Yes | Ignore | No | Yes |
| `experimental/` | Experimental pipeline source | EXPERIMENTAL | No | No | Track with explicit status | No | Yes |
| `experimental_runs/` | Experiment outputs and Model Lab evidence | TEST EVIDENCE + GENERATED | No | Yes | Ignore bulk; curate receipts | No | Yes |
| `evolution_runs/` | Historical evolution-loop outputs | TEST EVIDENCE | No | Yes | Ignore bulk; curate summary | No | Yes |
| `full_pipeline_runs/` | Specialist pipeline results | TEST EVIDENCE | No | Yes | Ignore bulk; curate golden run | No | Yes |
| `klein_batch_runs/` | Historical Klein batch outputs | TEST EVIDENCE | No | Yes | Ignore bulk; curate fixtures | No | Yes |
| `klein_ab_tests/` | Klein comparison evidence | TEST EVIDENCE | No | Yes | Ignore bulk; curate decisions | No | Yes |
| `klein_comparisons/` | Klein visual comparison images | TEST EVIDENCE | No | Yes | Ignore bulk | No | Yes |
| `render_only_runs/` | Old render-only outputs; largest runtime group (~468 MiB) | GENERATED/LEGACY | No | Yes | Ignore; archive proposal | No | Yes |
| `runs/` | Historical/headless run outputs | GENERATED/LEGACY | Conditional | Yes | Ignore bulk; preserve provenance | No | Yes |
| `e2e_runs/` | Prior end-to-end evidence | TEST EVIDENCE | No | Yes | Curate golden evidence | No | Yes |
| `visual_review_runs/` | Visual review diagnostics and benchmarks | TEST EVIDENCE | No | Yes | Ignore bulk; curate failure fixtures | No | Yes |
| `balanced_default_validations/` | Renderer validation evidence | TEST EVIDENCE | No | Yes | Curate summary/receipts | No | Yes |
| `migration/` | Migration artifacts and historical compatibility | LEGACY | No | Mixed | Track docs/tools only | No | Yes |
| `assets/generated/` | Generated UI/static assets | GENERATED | Conditional | Yes | Ignore if reproducible | No | Yes |
| `analysis/` | Prior audits and roadmaps | DOCUMENTATION | No | No | Track after truth audit | No | Yes |
| `docs/` | Product, architecture, operation and release documentation | ACTIVE + LEGACY | Yes | No | Track and label currency | No | Yes |
| `tests/` | Automated tests plus leaked temporary directories | ACTIVE + TEMPORARY | Yes | Mixed | Track tests; ignore caches/temp dirs | No | Yes |
| `__pycache__/`, `*/__pycache__/` | Python bytecode caches | TEMPORARY | No | Yes | Ignore; untrack without deleting source | Yes after checkpoint | No |
| `dummy_tmp/` | Temporary/debug outputs | TEMPORARY | No | Yes | Ignore | No | Yes |
| `ada-character-onboarding-*` | Leaked onboarding test sandboxes; inaccessible | TEMPORARY | No | Yes | Ignore; removal requires permission review | No | Yes |
| `ada-mission-delete-*` | Leaked mission-delete test sandboxes; inaccessible | TEMPORARY | No | Yes | Ignore; removal requires permission review | No | Yes |
| `.obsidian/` | Local editor workspace | LOCAL CONFIG | No | Yes | Ignore | Yes after checkpoint | No |
| `.git/` | Git object database (~601 MiB) | VCS INTERNAL | Yes | Yes | Never alter manually | No | No |

## Root-file findings

- `START_ADA_APP.cmd`, `ada.py` and `run_production.py` are launch surfaces and require startup certification.
- `patch_*.py`, `fix_*.py`, `update_*.py`, `debug.py` and ad-hoc `test_*.py` files at repository root are historical maintenance helpers. They are `UNKNOWN` until caller and provenance checks complete.
- `comfy_history.json`, `tree.txt`, `orihime_debug.zip` and the malformed-looking file `with semantic roles…` are local/debug artifacts. None is approved for deletion yet.
- Absence of `.gitignore` explains most of the 3,314 untracked entries and the tracked bytecode drift.

## Workflow truth discovered so far

The repository currently has two active production surfaces:

1. The current ADA app renderer pipeline reads `config/pipeline.json` and uses `workflows/production/lustify_krea2_primary_v1_api.json`, conditional Img2Img and optional Miaomiao.
2. The specialist/headless split pipeline uses `scripts/production_workflows.py` and pins `workflows/production/illustrious_only_api.json` plus `workflows/production/klein_only_api.json`.

Combined historical workflows are under `workflows/legacy/`. This isolation is correct. The coexistence of two product pipelines must be documented as architecture truth; collapsing them is a large architectural change and is outside automatic cleanup.

