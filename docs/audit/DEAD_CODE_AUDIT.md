# ADA 1.0 Alpha dead-code audit

Static caller searches are evidence for classification, not authorization to delete.

| Path/group | Classification | Evidence / recommendation |
|---|---|---|
| `fix_lib.py`, `fix_tabs.py`, `patch_html.py`, `patch_js.py`, `patch_main.py`, `update_js.py`, `update_ui.py`, `update_ui_resume.py` | LEGACY / DELETE_SAFE candidate | One-off direct source patchers; no callers found; several target superseded UI text. Preserve until owner confirms their historical value, then move to `legacy/maintenance/` or delete in one reviewed commit. |
| `debug.py` | LEGACY | Hard-coded historical character/run debug entrypoint; no caller found. |
| `extract.py` | LEGACY | Refers to a moved/deleted combined workflow path; no caller found. |
| `run_recovery.py` | LEGACY / HIGH RISK | Hard-coded historical mission/run recovery; must not be invoked as a generic recovery tool. |
| `run_smoke.py`, `run_production.py` | UNKNOWN / MANUAL | Standalone manual runners with no import callers. Zero callers alone does not prove dead code. |
| Root `test_*.py` and `tests_ada_*.py` | LEGACY TEST candidate | Ad-hoc tests outside the main `tests/` tree. Classify/migrate only after test ownership is frozen. |
| `with semantic roles` | DELETE_SAFE candidate | Captured terminal pager/help output, not source or documentation. No caller found. Not deleted during this audit. |
| CLI scripts with no import callers | ACTIVE or UNKNOWN | Many product scripts are intended entrypoints; absence of imports is not evidence of disuse. |

No file was removed or moved. The pre-audit branch protects the committed ancestor, but the large uncommitted working set is not yet captured in a Git commit, so cleanup must remain conservative.
