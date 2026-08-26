# ADA 1.0 Alpha functional catalog

Status values: `IMPLEMENTED`, `PARTIAL`, `LEGACY`, `NOT_IMPLEMENTED`, `AUDIT_PENDING`.

| ID | Screen / feature | UI action | Backend / persistence | Expected result | Current state | Test/evidence |
|---|---|---|---|---|---|---|
| HOME-001 | Home dashboard | Open Home | missions, Library assets, collections APIs | Current work, visible recent assets and canonical collection counts | IMPLEMENTED | Product inspection pending |
| CMD-001 | Command bar | Enter instruction, Go | `POST /api/command` | Parsed navigation/action or understandable feedback | IMPLEMENTED | Button audit pending |
| CHAR-001 | Character catalog | Open Characters | `GET /api/characters/catalog` | Added/suggested grid, counts, covers, capabilities | IMPLEMENTED | Browser baseline pending |
| CHAR-002 | Add character | `+ Add character` / `+ Add` | `POST /api/characters/bootstrap` | Persist character metadata/references and refresh dropdown/catalog | IMPLEMENTED | Existing onboarding tests; E2E pending |
| CHAR-003 | Duplicate character | Add an existing identity | bootstrap validation | Explicit rejection or canonical resolution | PARTIAL/AUDIT_PENDING | Existing onboarding tests require mapping |
| CHAR-004 | Delete character | No product control | No delete endpoint | Confirm impact, preserve historical runs, refresh UI | NOT_IMPLEMENTED | Backlog/proposal required |
| CHAR-005 | Revalidate references | Onboarding/revalidation path | `POST /api/characters/revalidate` | Rebuild/validate canonical identity evidence | IMPLEMENTED API; UI audit pending | Existing character tests |
| CHAR-006 | Character hero | Set as hero from asset | `POST /api/characters/{name}/hero`; `data/character_db/heroes.json` | Only a visible Library image becomes cover | IMPLEMENTED | Catalog tests/manual audit |
| CREATE-001 | Scene creation | Select character, action, setting, count, Generate | `POST /api/missions/create`; `data/missions/` | Persist queued mission and show real state | IMPLEMENTED | Mission tests/E2E pending |
| CREATE-002 | Dataset/auto concepts | Dataset submode | same mission API / creative pipeline | Generate configured small dataset | PARTIAL | Must avoid large run during Alpha audit |
| CREATE-003 | Stock generation | Switch Stock, optional outfit, Generate | mission API -> direct renderer pipeline | One-character studio image, review, Library promotion, cover | IMPLEMENTED | Recent multi-character run; certification pending |
| MISSION-001 | Mission status | Open active/recent mission | `GET /api/missions/{id}` | Persisted queued/running/terminal state and stage detail | IMPLEMENTED | Busy/state audit pending |
| MISSION-002 | Mission funnel | Open mission detail | `GET /api/missions/{id}/funnel` | Inspect stage boundary artifacts | IMPLEMENTED | Manual audit pending |
| MISSION-003 | Cancel mission | Cancel | `POST /api/missions/{id}/cancel` | Cancellation persists and incompatible actions disable | IMPLEMENTED | Safety audit pending |
| MISSION-004 | Resume mission | Resume | `POST /api/missions/{id}/resume` | Resume from safe persisted state | PARTIAL | Restart/boundary certification pending |
| MISSION-005 | Delete mission | Delete terminal mission | `DELETE /api/missions/{id}` | Explicit impact; no unexpected output cascade | IMPLEMENTED | Existing delete tests; manual provenance audit pending |
| LIB-001 | Library character grid | Open Library | `GET /api/library/assets` | Only visible active assets grouped by character | IMPLEMENTED | Visibility tests/manual count audit |
| LIB-002 | Library all/favorites/rejected | Change view | client filter over Library data | Consistent visible/rejected semantics | IMPLEMENTED | Product inspection pending |
| LIB-003 | Search/filter/sort | Use controls | client controls + collection metadata | Stable combined filtering and sort | IMPLEMENTED | Product inspection pending |
| LIB-004 | Character workspace | Open character | filtered Library data | Gallery for selected identity; no duplicate Character/Compare tabs | IMPLEMENTED | Baseline pending |
| LIB-005 | Asset detail | Open card | Library metadata | Image, provenance, rating, review, renderer and technical details | IMPLEMENTED | Gallery audit pending |
| LIB-006 | Favorite/rating/review | Use detail controls | `POST /api/library/review/{asset_id}` | Persist human evidence without overwriting agent evidence | IMPLEMENTED | Rating audit pending |
| LIB-007 | Remove from Library | Remove one/many | `POST /api/library/remove-selected` | Soft-reject/hide; files and provenance remain | IMPLEMENTED | Delete-safety audit pending |
| LIB-008 | Hard Re-Evaluate | Select assets | `POST /api/library/hard-reevaluate` | New evidence stored separately; visible status and delta | IMPLEMENTED | Full audit pending |
| LIB-009 | Compare render outputs | Compare in asset detail | receipt metadata/client modal | Compare real sibling outputs and preferences | IMPLEMENTED | Button audit pending |
| LIB-010 | Reinterpret/alternative | Asset actions | reinterpretation endpoints | New uniquely identified request and persisted result | IMPLEMENTED | E2E pending |
| RUN-001 | Run history | Open Runs | `GET /api/runs` and detail endpoints | Run list, status, concepts, telemetry | IMPLEMENTED | Navigation/state audit pending |
| RUN-002 | Concept human review | Review concept | `POST /api/runs/{run}/concepts/{concept}/review` | Persist keep/reject decision | IMPLEMENTED | Manual audit pending |
| PILOT-001 | Pilot generation/resume | Creative Lab controls | pilot endpoints | Generate/resume experimental pilot | EXPERIMENTAL | Excluded from core certification |
| MODEL-001 | Model Lab scan | Scan Models | Model Lab endpoints | Discover without changing production routing | IMPLEMENTED TOOL | Existing model receipts; UI pending |
| MODEL-002 | Controlled one-image test | Run one image | `POST /api/model-lab/run` | Persist isolated model test | IMPLEMENTED TOOL | Manual audit pending |
| MODEL-003 | Benchmarks | Initialize/run/evaluate | benchmark endpoints | Persist comparable test/evaluation receipts | IMPLEMENTED TOOL | Evidence exists; not core Golden E2E |
| SET-001 | Settings/system status | Open Settings | `GET /api/system` | Accurate live service status and current capabilities | PARTIAL | Stale hardcoded rows found; small fix candidate |
| ROAD-001 | Roadmap | Open Roadmap | `GET /api/roadmap` | Read current roadmap | IMPLEMENTED | Documentation-only audit |
| VIDEO-001 | Videos | Open legacy placeholder | none | Clearly marked unavailable | LEGACY/NOT_IMPLEMENTED | Current UI says “Coming next” |

## State model in the current app

Mission persistence currently uses coarse states such as `CREATED`, `WAITING_FOR_GPU`, `RUNNING`, `PRODUCING`, `COMPLETE`, `PARTIAL`, `FAILED` and `CANCELLED`, plus `current_stage_detail` and per-run artifacts. The specialist/headless pipeline also persists finer stage boundaries such as premise, Illustrious render/review and Klein render/review.

The Alpha audit must not claim that every fine-grained state is a first-class `ProductionMission.status` value. Certification will map persisted boundary artifacts to the UI funnel instead.

## Immediate product-truth findings

- Character deletion is not implemented and must be `NOT_IMPLEMENTED`, not `FAIL`.
- Videos are a legacy placeholder, not a working feature.
- Settings contains hardcoded “Online” badges in addition to live system status; those rows can display false state.
- Settings labels latent Img2Img as “Not integrated” although the current production configuration and renderer code implement a conditional Lustify latent Img2Img route.

