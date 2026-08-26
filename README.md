# ADA 1.0

ADA is a local image-production application. Its current production renderers are Lustify Krea2 direct (primary), Miaomiao Anima16 (anime), and Miaomiao → Lustify latent Img2Img when identity needs a fallback.

Start the application with `START_ADA_APP.cmd`, or run:

```powershell
python ada.py serve
```

Read-only health and path checks:

```powershell
python ada.py paths
python ada.py check
```

## Repository Layout

- `ada_app/` — product application, API, UI, Library and mission logic.
- `config/` — active configuration and machine-local overrides. Productive character metadata is data, not config.
- `data/` — ADA-owned persistent runtime data.
- `docs/` — architecture, decisions, audits, releases and migrations.
- `experimental/` — model labs, prototypes and experimental evidence; never a default production path.
- `legacy/` — historical pipelines, runs, tools, assets and provenance retained read-only.
- `schemas/` — persisted contract and receipt schemas.
- `scripts/` — maintained operators and utilities used by the product.
- `tests/` — automated tests. Their temporary files are constrained to `data/tmp/tests/`.
- `workflows/production/` — only the current Lustify/Miaomiao production workflows.
- `workflows/experimental/` — workflows under evaluation.
- `workflows/legacy/` — Illustrious/Klein and historical workflows; production loaders do not search this tree.
- `ada.py` — canonical CLI/application entry point.
- `START_ADA_APP.cmd` — Windows launcher.

Within `data/`:

- `characters/` — authoritative character catalog, taxonomy and hero/cover selections.
- `missions/` — authoritative mission state.
- `library/` — curated ADA dataset, managed images, per-asset records, index and ratings.
- `runs/` — current mission, renderer, stock and review runs.
- `references/` — authoritative canonical character references and manifests.
- `indexes/` — rebuildable indexes outside the Library-specific index.
- `tmp/` — locks, staging and test sandboxes; never authoritative data.

## Where is my dataset?

ADA dataset:

```text
D:\IA\Ada\data\library
```

`data/library/index.json` is the navigation source of truth. Each image record includes an asset ID, character, renderer, render intent, prompt/spec data, seed and dimensions through its render receipt, Visual Review and machine scores, Human Judgment, Hard Re-Evaluation history through `asset_review.json`, source mission/run, timestamps and provenance.

Images live in content-addressed storage under `data/library/assets/sha256/`. Per-asset snapshots live in `data/library/records/`. The index is rebuildable from current runs, but rebuilds always adopt the resulting pixels into ADA-owned storage before publishing the index.

## Where are raw ComfyUI renders?

ComfyUI output is the raw renderer workspace. ADA Library is the persistent curated dataset.

```text
ComfyUI output
    → ADA processes and reviews the render
    → Library persistence adopts and hash-verifies a physical copy
    → data/library/assets/sha256/...
```

Library records retain the original ComfyUI path as `storage_provenance.original_source_path`; normal display and review use `full_image_path` inside ADA storage. Removing or rotating ComfyUI output therefore does not remove an accepted Library image.

## Storage compatibility

All new writes resolve through `scripts/ada_paths.py`. Environment or `config/ada.local.json` overrides may relocate authoritative roots. Current writers never target `legacy/`. Historical files remain available under `legacy/`, and migration provenance records their former locations.

The completed storage migration is documented in `docs/migrations/ADA_1_0_STORAGE_RESTRUCTURE.md`.
