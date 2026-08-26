# ADA 1.0 Alpha known issues

| ID | Severity | Component | Description | Reproduction / evidence | Workaround | Recommended fix |
|---|---|---|---|---|---|---|
| STATE-001 | High | Missions/Home | Five persisted missions appear active despite old timestamps, failed details or populated completion fields; ComfyUI was idle. | Open Home; see `home__loaded__after.png` and `docs/audit/NAVIGATION_STATE_AUDIT.md`. | Inspect mission detail/files; do not trust aggregate “in progress” alone. | Implement deterministic mission reconciliation per proposal. |
| ARCH-001 | Blocker for release tag | Pipeline | The UI product pipeline and the split Premise→Illustrious→Review→Klein→Final path are separate implemented surfaces. The requested UI Golden E2E does not exist as one route. | Architecture and workflow audits. | Use each surface only for its documented purpose. | Decide authority/integration via PROPOSAL-ARCH-001. |
| TEST-001 | High | Tests | Existing suite: 56/58 pass; two Klein prompt tests assert an older exact sentence shape. | `docs/audit/TEST_EXECUTION_AUDIT.md`. | Review prompt output semantically; do not treat the two assertions as passing. | Freeze prompt contract, then align compiler and tests. |
| TEST-002 | Medium | Product inspection | No repository Playwright dependency/suite or lockfile. | No Node manifest found; manual evidence only. | Use `audit_evidence/` and manual browser audit. | Approve PROPOSAL-TEST-001. |
| UX-001 | High | Mobile | Fixed sidebar leaves only ~170 px at 390 px viewport; core content clips. | `gallery__mobile__baseline.png`. | Desktop/tablet usage. | Responsive navigation proposal. |
| UX-002 | Medium | Navigation | Tabs do not change URL/history; refresh/back/forward/deep link cannot restore current screen. | Navigation audit. | Navigate through sidebar after refresh. | Routable navigation proposal. |
| UX-003 | Low | Model Lab | Long model/test IDs wrap excessively. | `model-lab__baseline.png`. | Wider viewport. | Clamp/ellipsis with disclosure. |
| VRAM-001 | Medium | Resource handoff | Mocked transitions pass, but no live busy-render arbitration was destructively injected during concurrent work. | VRAM audit. | Observe queue and avoid manual unload while busy. | Capture full transition receipts in controlled Golden run. |
| DEL-001 | Medium | Deletion | Character/run/dataset deletion is not implemented; Library removal has no audited restore UI. | Delete safety audit. | Preserve manually; rejected assets remain on disk. | Design explicit restore/delete lifecycle. |
| ERR-001 | Low | Hard reevaluation | Per-asset failures are server-logged but not summarized clearly in the UI response. | Endpoint/code audit. | Check server log and evaluated count. | Return structured per-asset errors. |
| RATING-001 | High | Hard reevaluation | A second hard reevaluation overwrites the previous `hard_rating` object instead of preserving an append-only history. | `docs/audit/GALLERY_RATING_AUDIT.md`. | Do not rerun Hard Re-Evaluate when the previous receipt must be preserved externally. | PROPOSAL-RATING-001. |

No known issue was silently converted into a pass.
