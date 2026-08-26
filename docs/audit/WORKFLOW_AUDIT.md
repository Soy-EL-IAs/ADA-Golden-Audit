# ADA 1.0 Alpha workflow audit

## Production workflows

| Name | Path | Status | Caller | Model/input | Output |
|---|---|---|---|---|---|
| Illustrious only | `workflows/production/illustrious_only_api.json` | PRODUCTION — split specialist path | `scripts/production_workflows.py` via specialist/headless orchestration | Text prompt; `waiIllustriousSDXL_v160.safetensors` | One Illustrious image at SaveImage node 7 |
| Klein only | `workflows/production/klein_only_api.json` | PRODUCTION — split specialist path | `scripts/production_workflows.py` via specialist/headless orchestration | Approved Illustrious image + Klein prompt; Flux 2 Klein + configured LoRAs | One Klein image at SaveImage node 20 |
| Lustify primary | `workflows/production/lustify_krea2_primary_v1_api.json` | PRODUCTION PRIMARY — app renderer path | `ada_app/renderer_pipeline.py` -> `scripts/production_workflows.py` | Resolved renderer prompt; Lustify Krea2 checkpoint | One direct T2I image |
| Lustify Img2Img | `workflows/production/lustify_krea2_img2img_v1_api.json` | PRODUCTION CONDITIONAL | Character capability route through renderer pipeline | Trusted source image + source-preserving prompt | One latent Img2Img image |
| Miaomiao secondary | `workflows/production/miaomiao_anima16_secondary_v1_api.json` | PRODUCTION OPTIONAL SECONDARY | Explicit Miaomiao/identity route through renderer pipeline | Booru-style prompt; Miaomiao Anima 1.6 | One anime image |

## Reusable graph templates

| Path | Classification | Consumer/status |
|---|---|---|
| `workflows/constructors/illustrious_base.json` | EXPERIMENTAL/REUSABLE | Constructor source; not a directly pinned product submission graph |
| `workflows/constructors/lustify_base.json` | EXPERIMENTAL/REUSABLE | Constructor source |
| `workflows/constructors/miaomiao_anima16_base.json` | EXPERIMENTAL/REUSABLE | Constructor source |
| `workflows/constructors/anima38_base.json` | EXPERIMENTAL | Anima renderer is marked discarded in current pipeline decisions |
| `workflows/finalizers/klein_base.json` | EXPERIMENTAL/REUSABLE | Finalizer source; product submission uses the pinned production graph |

## Legacy quarantine

| Path | Classification | Runtime rule |
|---|---|---|
| `workflows/legacy/generated/chel_001_illustrious_to_krea_chained_api.json` | LEGACY | Never load from production |
| `workflows/legacy/generated/chel_001_illustrious_to_krea_chained_ui.json` | LEGACY | Never load from production |
| `workflows/legacy/illustrious_to_klein_batch_base_ui.json` | LEGACY | Never load from production |
| `workflows/legacy/krea/illustrious_to_krea_fast_chained_README.md` | LEGACY DOCUMENTATION | Historical only |
| `workflows/legacy/README.md` | LEGACY DOCUMENTATION | Explains quarantine |

The old combined runner is already hard-quarantined and an existing test proves it cannot submit. The run index also excludes legacy adapters.

## Root workflows requiring classification

| Path | Current classification | Finding |
|---|---|---|
| `workflows/illustrious_4x_api.json` | DEPRECATED/UNKNOWN | Not referenced by a pinned product loader in the current source audit |
| `workflows/krea_convert_1x_api.json` | DEPRECATED/UNKNOWN | Historical single-stage utility; no current product caller demonstrated |
| `workflows/illustrious_to_krea_fast_chained_api.json` | DEPRECATED | Combined historical graph outside the legacy directory; must not be used by production |
| `workflows/illustrious_to_krea_fast_chained_ui.json` | DEPRECATED | UI form of the historical combined graph |
| `workflows/minimax_f2v_ada_clean_ui.json` | EXPERIMENTAL | MiniMax notes/config exist, but no current product submission caller was demonstrated |

Moving the root deprecated workflows into `workflows/legacy/` is intentionally deferred until Git provenance and all callers are checked. No file was moved or deleted during this audit.

## Loader controls

Implemented controls:

- Product graphs are constant-pinned or selected through `config/pipeline.json`.
- Illustrious and Klein graph validators enforce required node classes, one output, configured models/settings and forbidden cross-stage nodes.
- The old combined runner raises before submission.
- Active-path scanning excludes the quarantined legacy directory and checks incident-specific dangerous defaults.

Control `WF-001` — fixed and manually verified:

`renderer_workflow_path()` now resolves the configured path and rejects every path outside `workflows/production/`, including `workflows/legacy/` and deprecated root graphs. A manual negative check substituted a legacy workflow in the preset and produced the expected `ValueError` before graph loading or submission. No new test file was added during this pass, respecting the temporary test-freeze requested by the owner.
