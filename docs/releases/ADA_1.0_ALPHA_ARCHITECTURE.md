# ADA 1.0 Alpha architecture truth

This document describes the repository as implemented on 2026-08-25. Aspirations are not labeled as product behavior.

## Implemented

```text
Browser UI (HTML/CSS/JS)
  -> FastAPI endpoints
  -> persisted Mission / Character / Library state
  -> background mission runner
  -> cross-process GPU lock
  -> renderer pipeline / specialist headless pipeline
  -> LM Studio specialists and ComfyUI
  -> receipts, reviews, indexes and visible Library assets
```

- The UI is a client of the API; it does not own generation or review rules.
- `ada_app/main.py` serves the product and exposes mission, character, library, run, model-lab, settings and reinterpretation endpoints.
- `ada_app/mission.py` persists mission state under `data/missions/`.
- `ada_app/mission_runner.py` runs work in the background and serializes GPU access with a file lock.
- `ada_app/renderer_pipeline.py` resolves render specifications, compiles renderer prompts, renders through ComfyUI, calls grounded Visual Review and persists receipts.
- `ada_app/asset_library.py` builds the active Library index from persisted run artifacts and human review state.
- Headless execution remains available through scripts such as `scripts/run_full_pipeline.py` and the specialist orchestrator.

## Two implemented production surfaces

### Current app renderer pipeline

The active product profile is Lustify primary, with a conditional Lustify Img2Img route and optional Miaomiao secondary route. These graphs are configured in `config/pipeline.json`.

### Split specialist pipeline

The specialist/headless flow uses separate Illustrious and Klein graphs pinned by `scripts/production_workflows.py`. It is the path matching:

```text
Premise -> Illustrious prompt/render -> Visual Review
        -> Klein prompt/render -> Final Review
```

These two surfaces coexist. Treating them as one is a future architectural decision, not a cleanup fix.

## Partial

- Restart recovery exists through persisted mission/run artifacts, but boundary-by-boundary recovery still requires certification.
- UI state reflects mission state, but queued/running/completed and failure UX require systematic product inspection.
- Library provenance and human review are implemented; complete delete-safety and broken-artifact behavior require audit.
- Character onboarding, references, covers and Stock generation are implemented; duplicate/delete/reference failure paths require certification.
- Model Lab and capability routing exist, with only some characters formally evaluated.

## Experimental

- `experimental/` and most of `experimental_runs/`.
- Constructor/finalizer graph composition outside the pinned production loaders.
- Model/renderer adapter candidates and parts of the alternative-generation surface.
- MiniMax integration notes and workflow, unless a live caller is demonstrated during audit.

## Legacy

- Combined Illustrious-to-Klein/Krea graphs under `workflows/legacy/`.
- Historical run shapes supported by compatibility code in Library and run indexing.
- Root historical render workflows not referenced by pinned production loaders.

## Planned or not yet certified

- A single authoritative product pipeline designation.
- Full Playwright product-inspector coverage.
- Golden E2E evidence pack for `ada_alpha_golden_001`.
- Complete restart certification at each persisted pipeline boundary.
- Formal delete-safety matrix across characters, assets, missions, runs and datasets.
- Portable dependency lock and clean Git/runtime separation.

## Architecture invariants for Alpha

1. UI controls and represents ADA; business rules stay behind the API.
2. A queued request is not running and a running request is not complete.
3. UI completion must come from persisted mission/run state, never only HTTP completion.
4. LM Studio and ComfyUI handoffs must obey explicit VRAM arbitration.
5. Production loaders must never resolve a workflow under `workflows/legacy/`.
6. Historical provenance and original reviews must not be overwritten by reevaluation.
7. New audit runs require unique IDs and must not overwrite prior artifacts.

