# ADA 1.0 Alpha certification matrix

Audit date: 2026-08-25. This is an evidence-backed release candidate assessment, not a completed release certification.

| Area | Status | Automated | Manual | Evidence / reason |
|---|---|---:|---:|---|
| Startup / service discovery | PASS | No | Yes | Local ADA returned 200 after restart; ComfyUI queue and LM Studio endpoint were reachable. |
| Repository inventory | PASS_WITH_KNOWN_ISSUE | No | Yes | `docs/audit/PROJECT_INVENTORY.md`; unknown/legacy candidates intentionally preserved. |
| Production workflow isolation | PASS | Yes | Yes | 12 workflow tests passed; manual legacy-path guard rejected before load. |
| Configuration freeze | PASS | No | Yes | `ADA_1.0_ALPHA_CONFIG.md`. |
| Architecture truth | PASS_WITH_KNOWN_ISSUE | No | Yes | Two production surfaces are documented; authority unresolved. |
| Characters / onboarding / covers | PASS_WITH_KNOWN_ISSUE | Yes | Yes | Existing catalog/onboarding/profile/Stock tests pass; character delete is not implemented. |
| Missions | PASS_WITH_KNOWN_ISSUE | Yes | Yes | Create/version/delete tests pass; stale persisted “active” missions remain (STATE-001). |
| Premise agent | PASS_WITH_KNOWN_ISSUE | Partial | No live Alpha run | Existing specialist boundary tests pass; no new frozen one-premise live test was run. |
| Illustrious prompt/render | PASS_WITH_KNOWN_ISSUE | Partial | No live Alpha run | Isolated graph and state tests pass; no new UI evidence of running/completion. |
| Visual Review boundary | PASS_WITH_KNOWN_ISSUE | Yes | No live Alpha failure injection | Five grounded-review tests pass; no live truncated/failure receipt in this audit. |
| Klein prompt/render | FAIL | Yes | No live Alpha run | Graph isolation passes, but 2 current prompt compiler assertions fail. |
| Final Review | PASS_WITH_KNOWN_ISSUE | Partial | Existing assets inspected | Persisted evidence is visible; no new end-to-end Alpha final review executed. |
| Gallery / Collections | PASS | Partial | Yes | Visibility checks 3/3; canonical counts verified against Neverness collection; screenshots captured. |
| Rating / Hard Reevaluate | PASS_WITH_KNOWN_ISSUE | Partial | Yes | Original/hard fields are distinct, but repeated hard reviews overwrite the prior hard result (RATING-001); live failure feedback is incomplete. |
| Delete safety | PASS_WITH_KNOWN_ISSUE | Yes | Yes | Mission tests pass; Library removal is soft; other delete surfaces not implemented. |
| Navigation / responsive | PASS_WITH_KNOWN_ISSUE | No | Yes | Desktop/tablet usable; mobile and history/deep-link issues documented. |
| Persistence / restart | PASS_WITH_KNOWN_ISSUE | Partial | Partial | Server restart preserved Library/missions; three pipeline frontier restarts not executed. |
| VRAM arbitration | PASS_WITH_KNOWN_ISSUE | Yes | Read-only live preflight | Four resource-handoff tests pass; live busy transition not injected. |
| Existing test suite | FAIL | Yes | N/A | 56/58 pass after removing sandbox permission noise. |
| Playwright Product Inspector | NOT_IMPLEMENTED | No | Manual substitute | PROPOSAL-TEST-001; screenshots exist but no repository suite. |
| Golden E2E `ada_alpha_golden_001` | NOT_IMPLEMENTED | No | No | Exact UI→split specialist path is not currently integrated; no fake run was claimed. |
| Git hygiene / clean release tree | FAIL | No | Yes | Large pre-existing mixed working tree remains; no destructive cleanup performed. |
| Release commit / `ADA-1.0-alpha` tag | NOT_IMPLEMENTED | No | No | Blocked by Golden E2E, two failing tests and dirty working tree. |

## Certification decision

`ADA 1.0 Alpha` is **not yet certifiable or taggable** under the supplied Definition of Done. The audit baseline, fixes, evidence and proposals are usable, but creating the release commit/tag now would violate the explicit no-fake-completion rule.

Exit criteria for a later certification pass:

1. Resolve pipeline authority and execute the exact one-character Golden E2E with unique ID/evidence.
2. Resolve the two Klein prompt contract failures and rerun the suite green.
3. Run the approved product inspector or explicitly revise the DoD.
4. Review and commit the mixed working set so `git status` is clean without discarding owner work.
