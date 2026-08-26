# ADA 1.0 Alpha button audit

`PASS_MANUAL` means clicked without creating/deleting data. `PASS_WIRED` means the handler and endpoint were inspected but the mutating or expensive action was not executed in the UI baseline pass.

| ID | Screen | Button/control | Visible/enabled rule | Action / feedback | Result |
|---|---|---|---|---|---|
| BTN-001 | Sidebar | Home | Always | Opens Home and reloads summaries | PASS_MANUAL |
| BTN-002 | Sidebar | Library | Always | Loads Library | PASS_MANUAL |
| BTN-003 | Sidebar | Characters | Always | Loads catalog | PASS_MANUAL |
| BTN-004 | Sidebar | Create | Always | Loads characters and form | PASS_MANUAL |
| BTN-005 | Sidebar | Runs | Always | Loads run history | PASS_MANUAL |
| BTN-006 | Sidebar | Model Lab | Always | Loads registry/benchmarks | PASS_MANUAL |
| BTN-007 | Sidebar | Settings | Always | Loads live system state | PASS_MANUAL |
| BTN-008 | Home | Go | Always; input may be empty | `POST /api/command`; feedback container | PASS_WIRED |
| BTN-009 | Characters | Add character | Always | Opens Create/onboarding | PASS_MANUAL navigation |
| BTN-010 | Characters | All/Added/Suggested/Needs cover | Always | Client catalog filter | PASS_MANUAL |
| BTN-011 | Character card | Open Library | Added only | Opens character workspace | PASS_WIRED |
| BTN-012 | Character card | Generate Stock | Disabled when route red | Preselects Stock generation | PASS_WIRED |
| BTN-013 | Suggested card | Add character | Suggested only | Opens onboarding with name | PASS_WIRED |
| BTN-014 | Library | Characters/All/Favorites/Rejected | Always | Client view/filter | PASS_MANUAL |
| BTN-015 | Library | Select images / Cancel | Hidden where selection is irrelevant | Toggles non-destructive selection | PASS_WIRED |
| BTN-016 | Library | Remove | Only after selection | Soft-rejects selected assets; confirmation and no file deletion | PASS_WIRED; destructive UI action not repeated during audit |
| BTN-017 | Library | Hard Re-Evaluate | Only after selection | Starts separate reevaluation evidence | PASS_WIRED; expensive action pending certification |
| BTN-018 | Character workspace | Back / Generate images | Workspace only | Returns to Library / opens Create | PASS_WIRED |
| BTN-019 | Workspace | All/Lustify/Miaomiao/Legacy/Rejected | Workspace only | Client filter | PASS_WIRED |
| BTN-020 | Asset detail | Close | Modal only | Closes modal | PASS_MANUAL |
| BTN-021 | Asset detail | Generate alternative | Visible asset | Opens prefilled Create context | PASS_WIRED |
| BTN-022 | Asset detail | Reinterpret | Visible asset | Opens/executes reinterpretation request | PASS_WIRED; generation not repeated |
| BTN-023 | Asset detail | Compare | Only meaningful when sibling outputs exist | Displays real receipt outputs | PASS_WIRED |
| BTN-024 | Asset detail | Set as hero | Visible Library asset only | Persists cover and refreshes catalog | PASS_WIRED |
| BTN-025 | Asset detail | Favorite/rating | Modal only | Persists human review evidence | PASS_WIRED |
| BTN-026 | Asset detail | Remove from Library | Modal only | Soft reject; file preserved | PASS_WIRED; not repeated |
| BTN-027 | Create | Scene / Stock | Always | Switches form and defaults | PASS_MANUAL |
| BTN-028 | Create | Add | Requires new name | Character bootstrap with visible status | PASS_WIRED; creation E2E pending |
| BTN-029 | Create | Generate / Generate Stock | Requires valid character/fields; disabled while request sends | Creates persisted mission then opens detail | PASS_WIRED; Golden E2E pending |
| BTN-030 | Mission | Cancel / Resume / Delete | State-dependent | Corresponding mission endpoints | PASS_WIRED; safety tests pending |
| BTN-031 | Runs | View / Close | Row/detail dependent | Loads and closes run detail | PASS_WIRED |
| BTN-032 | Model Lab | Scan Models | Always | Safetensors header scan; status feedback | PASS_WIRED; not repeated |
| BTN-033 | Model Lab | Run one image | Only compatible recipe should be selectable | Isolated one-image job with status | PASS_WIRED; expensive action pending |
| BTN-034 | Model Lab | Initialize benchmarks | Always in current UI | Creates benchmark fixtures | PASS_WIRED; should gain existing-state/disabled audit |
| BTN-035 | Creative Lab | Generate Concepts/Pilot | Advanced surface | Experimental endpoints and status | LEGACY/EXPERIMENTAL; outside core Alpha certification |

No clearly dead visible core-product button was found in the first pass. The old Character/Compare workspace tabs are absent. The asset-detail Compare action remains, where it has the required context.

