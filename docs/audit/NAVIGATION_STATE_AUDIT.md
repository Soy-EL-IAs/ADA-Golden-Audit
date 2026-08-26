# ADA 1.0 Alpha navigation and state audit

## Navigation

| Scenario | Result | Status |
|---|---|---|
| Sidebar navigation across Home, Library, Characters, Create, Runs, Model Lab and Settings | Correct active surface and data load | PASS |
| Refresh on a non-Home tab | Returns to Home because tab state is not in URL | PASS_WITH_KNOWN_ISSUE |
| Browser Back/Forward between tabs | Tabs do not create history entries | NOT_IMPLEMENTED |
| Direct/deep link to a product tab/entity | No route representation exists | NOT_IMPLEMENTED |
| Invalid app URL | HTTP 404 with `Not Found` | PASS |
| Missing mission | HTTP 404 with `Mission not found` | PASS |
| Missing run | HTTP 404 with `Run not found` | PASS |
| Collection card -> Library | Opens All Images with canonical collection selected | PASS |
| Collection count -> Library result | Neverness to Everness: 3 vs 3 visible images | PASS |

## State consistency finding STATE-001

Five mission records are presented as active although their files have not changed since 2026-08-23 and no ComfyUI work is queued/running.

Evidence examples:

- `mission_20260823_190018_437422`: `status=PRODUCING`, `completed_at` populated, detail says `Mission FAILED: 0/2 approved` and `approved_assets=1`.
- `mission_20260823_184706_fe2045`: `status=CREATED`, no source runs, no start timestamp, but `approved_assets=5`.
- `mission_20260823_215733_8ba276`: `status=PRODUCING`, detail says cancellation is pending, last modified two days earlier.

This is persisted data inconsistency, not merely a display bug. Rewriting those JSON files by inspection would destroy evidence. The correct fix requires a startup reconciliation/heartbeat policy and is documented as PROPOSAL-STATE-001.

## Busy/running truth

The mission runner uses additional real states `WAITING_FOR_GPU` and `RUNNING`. The UI and `ProductionMission.STATES` omitted them from the active set even though the runner persists them. The Alpha code now recognizes these states. This does not solve stale historical records.

## Current state model boundaries

- Product Mission: coarse mission state plus `current_stage_detail` and counters.
- M2/pilot candidate: `pipeline_state` and render/review artifacts.
- Specialist run: fine-grained `ada_run.json` stage plus boundary files.
- Library: independent human status and canonical visibility rule.

Certification must compare all four rather than infer completion from an HTTP request or one field.

