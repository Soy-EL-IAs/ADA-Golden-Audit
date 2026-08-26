# Library source inventory — 2026-08-24

Static inspection only; no index rebuild, test, render, benchmark or E2E was run.

## Pilot lineage eligible for automatic Library indexing

| Origin | Mission-linked | Historical/no Mission | Total existing outputs |
|---|---:|---:|---:|
| Illustrious | 16 | 3 | 19 |
| Klein | 14 | 3 | 17 |
| Lustify | 1 | 0 | 1 |
| Miaomiao | 0 | 0 | 0 |
| **Total** | **31** | **6** | **37** |

The persisted pre-refactor index contains 18 generation-level records: Yoruichi 4,
Ghislaine 1 and 2B 13. The UI count of 17 was therefore already stale relative to the
index file. Those records collapse sibling renderer outputs. The v2 builder instead
produces one Library Image per existing output, so the same eligible lineage resolves
to 37 image records on the next index build.

Expected Character Card counts after that build are: 2B 28, Ghislaine Dedoldia 2,
and Shihouin Yoruichi 7.

## Deliberately outside automatic Library indexing

| Source | Receipts/requests | Existing unique outputs | Policy |
|---|---:|---:|---|
| Standalone Model Lab | 1 | 1 | promotion required |
| Official benchmark tree | 4 | 4 | promotion required |
| Manual controlled benchmark | 28 | 28 | promotion required |
| Reinterpretation | 1 request | 0 | not an image; `READY_FOR_RENDER` |
| Workflow-separation smoke | — | 2 | excluded: run name is outside the active `m2_*` RunIndex adapter |
| `render_only_runs/` | — | 291 physical images | historical/ungoverned; no automatic import |
| legacy `runs/` image folders | — | 24 physical images | historical/ungoverned; no automatic import |

The physical-folder counts are not treated as approved assets because those roots do
not provide the current Mission → Candidate → Renderer receipt contract. Future Model
Lab promotion must be explicit and create normal Library lineage; directory scanning
must never silently promote experiments.
