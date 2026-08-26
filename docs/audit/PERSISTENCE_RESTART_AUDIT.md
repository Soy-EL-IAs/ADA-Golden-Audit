# ADA 1.0 Alpha persistence and restart audit

The ADA web process was stopped and started once after code changes while ComfyUI was idle. After restart:

- Home loaded 84 persisted missions and the same active/stale aggregate.
- Library rebuilt/read 108 indexed records and exposed 89 visible assets.
- Collection totals remained 89 and character/hero data remained available.
- Rejected records remained excluded without physical deletion.
- Runs and Settings endpoints returned 200.

This proves coarse application restart persistence for the current Library, mission and run indexes. It does **not** certify automatic recovery at the fine-grained specialist frontiers `ILLUSTRIOUS_RENDERED`, `ILLUSTRIOUS_REVIEWED` and `KLEIN_RENDERED`; no live generation was interrupted during concurrent owner work.

Status: `PASS_WITH_KNOWN_ISSUE`.
