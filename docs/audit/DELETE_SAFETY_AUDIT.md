# ADA 1.0 Alpha delete safety audit

| Surface | Implemented behavior | Provenance outcome | Recovery | Status |
|---|---|---|---|---|
| Library asset | “Remove from Library” sets `REJECTED`; confirmation explicitly says files and lineage remain. | Physical image and historical record remain; shared visible filter excludes it from Home/Library counts and recents. | Can be recovered by changing review/library status; no UI restore action audited. | PASS_WITH_KNOWN_ISSUE |
| Mission | Only `FAILED`, `COMPLETE` or `CANCELLED` can be deleted; active states return 409. UI confirms that only persisted mission state is removed. | Library assets and shared character references remain. | Git/backups only for deleted mission JSON; no trash layer. | PASS_WITH_KNOWN_ISSUE |
| Character | No delete endpoint or UI action was found. | Nothing is deleted. | N/A | NOT_IMPLEMENTED |
| Run | No delete endpoint or UI action was found. | Nothing is deleted. | N/A | NOT_IMPLEMENTED |
| Dataset | No product delete endpoint or UI action was found. | Nothing is deleted. | N/A | NOT_IMPLEMENTED |

Existing mission-delete tests passed for terminal-only deletion, active-state blocking and UI confirmation wiring. Existing Library visibility checks passed and verify that removal changes the active read model without modifying the supplied historical records.

No real asset, mission, character, run, dataset or physical image was deleted during this audit.
