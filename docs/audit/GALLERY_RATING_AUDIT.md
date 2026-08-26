# ADA 1.0 Alpha Gallery and rating audit

## Gallery

Verified manually at desktop and tablet widths:

- Character and All Images grids load visible Library assets only.
- Canonical collection filters and character display names render correctly.
- Empty search/filter state is explicit.
- Asset detail opens the correct image and exposes renderer, status, agent score, human score, actions and technical provenance.
- Selection mode wires soft removal and Hard Re-Evaluate to explicit selected IDs.
- Rejected assets are excluded from normal views and remain available in the dedicated Rejected view.

Broken-image and missing-metadata behavior were inspected through code/fallbacks but not injected into live runtime data.

## Rating layers

The active record keeps automatic review fields, human review/rating and `hard_rating` as separate fields. Stage review and stage preference changes append history with supersession IDs, preserving their prior events.

Hard Re-Evaluate calculates and persists:

- current `final_score`/verdict/explanation returned by the hard reviewer;
- `original_score` derived from human rating when present, otherwise the agent rating;
- `delta` between hard and original score.

## Finding RATING-001

`save_hard_rating()` assigns `review["hard_rating"]` directly. A second Hard Re-Evaluate therefore replaces the previous hard result without a hard-review history, even though original automatic/human review remains separate. This violates the stronger Alpha requirement that reevaluation evidence never be silently overwritten.

No storage migration was applied during the audit. See `PROPOSAL-RATING-001_HARD_REEVALUATION_HISTORY.md`.

Status: Gallery `PASS_WITH_KNOWN_ISSUE`; Rating/Hard Re-Evaluate `PASS_WITH_KNOWN_ISSUE` for current display, but not fully certifiable until RATING-001 is resolved and a live failure path is evidenced.
