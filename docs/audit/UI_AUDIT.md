# ADA 1.0 Alpha visual UI audit

Baseline viewport: 1280 × 720 unless noted. Evidence is under `audit_evidence/`.

| ID | Severity | Screen | Finding | Evidence | Disposition |
|---|---|---|---|---|---|
| UI-001 | High | Home / Missions | Home reports five missions “in progress” although all files are from 2026-08-23, ComfyUI is idle and one persisted record says `Mission FAILED` while `status=PRODUCING`. | `home__loaded__baseline_viewport.png`; mission JSON audit | OPEN; requires reconciliation design (PROPOSAL-STATE-001) |
| UI-002 | High | Home / Collections | Every asset previously collapsed into `Unknown`, showing `11 characters / 89 images` instead of canonical collections. Literal historical `franchise: Unknown` blocked registry fallback. | `home__loaded__baseline_viewport.png` | FIXED; registry metadata enriches active read model |
| UI-003 | Medium | Library | Character cards exposed internal IDs such as `hyuuga_hinata`, `chun-li` and `nanally de NTE`; singular grammar was also wrong. | `gallery__grid__baseline.png`; `gallery__asset-detail__after.png` | FIXED; cards and asset-detail title use canonical display names and correct pluralization. Stable IDs remain internal. |
| UI-004 | Medium | Settings | Duplicate hardcoded Online badges could contradict live service state. Latent Img2Img was labeled “Not integrated” although a conditional production route exists. | `settings__baseline.png` | FIXED; duplicate static status removed and capability corrected |
| UI-005 | High | Global / mobile | At 390 × 844, fixed 220 px sidebar leaves 170 px for the app. Controls become a single narrow column and Library cards are clipped. | `gallery__mobile__baseline.png` | OPEN; responsive navigation proposal (PROPOSAL-UX-001) |
| UI-006 | Medium | Runs | Long run IDs/model names force horizontal overflow; raw `COMPLETE_TEXT_ONLY` is product-hostile and Date/Action move off screen. | `runs__history__baseline.png`; `runs__history__after.png` | FIXED; constrained columns, ellipsis and human status labels. Verified at 1280 px with no page overflow. |
| UI-007 | Low | Model Lab | Long uppercase filenames wrap across many short lines and dominate cards. | `model-lab__baseline.png` | OPEN polish candidate |
| UI-008 | Medium | Navigation | Tab clicks do not change URL/history. Refresh always returns Home; deep links, Back and Forward cannot restore product state. | Manual browser audit | OPEN; PROPOSAL-UX-002 |
| UI-009 | Low | Create Scene | Native radio controls have weak visual association and considerable empty horizontal space, but remain usable. | `create__scene__baseline.png` | OPEN polish candidate |
| UI-010 | Pass | Empty states | Character “Needs cover” and unmatched Library search show clear empty messages. | Manual DOM audit | PASS |
| UI-011 | Pass | Asset detail | Primary image, status, agent rating, human rating, actions and technical disclosure have clear hierarchy. | `gallery__asset-detail__baseline.png` | PASS_WITH_KNOWN_ISSUE (delete semantics require audit) |
| UI-012 | Pass | Characters | Summary, search, filters, identity capability, cover state and recommendations are visually coherent at desktop width. | `characters__list__baseline.png` | PASS |

## Before/after evidence

### Collections

- Before: `home__loaded__baseline_viewport.png` (`Unknown`).
- After: `home__collections__after.png` (11 canonical collections, compact counts).
- Count verification: `Neverness to Everness` reports one character / three images and opens exactly three visible Library cards.

### Library character names

- Before: `gallery__grid__baseline.png`.
- After: `gallery__grid__after.png`.
- Internal stable IDs remain in provenance and requests; the UI uses `character_display_name`.

### Settings

- Before: `settings__baseline.png`.
- After: `settings__after.png`.

### Runs

- Before: `runs__history__baseline.png` (raw status and horizontal overflow).
- After: `runs__history__after.png` (`Concepts ready`, constrained columns, Date and Action visible).

## Responsive result

- Desktop 1280 px: usable, four-column Library cards at the captured density.
- Tablet 768 px: usable with two-column cards, though dense.
- Mobile 390 px: fail for core product usage because navigation consumes more than half the viewport.

No global navigation redesign was applied during the Alpha audit.
