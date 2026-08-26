# ADA 1.0 Alpha documentation audit

| Document/group | Classification | Finding |
|---|---|---|
| `README.md` | CURRENT WITH ALPHA WARNING | Describes the current Lustify app surface and historical split path; now links the Alpha truth/certification documents and explicitly states the Golden limitation. |
| `README_ADA.md` | NEEDS REVIEW | Separate overview modified in the current worktree; do not overwrite until its intended audience is resolved. |
| `docs/releases/ADA_1.0_ALPHA_*` | CURRENT | Frozen configuration, architecture, issues, backlog and certification truth. |
| `docs/audit/*` | CURRENT AUDIT EVIDENCE | Inventory, workflows, UI, buttons, navigation/state, tests and safety findings. |
| `docs/CHANGELOG.md`, `docs/decisions/*`, `docs/features/*` | CURRENT / PROVENANCE | Active decision and feature history; do not collapse into the README. |
| `docs/prompting/*`, current runtime instructions | CURRENT SPECIALIST REFERENCE | Used by active compilers/agents where caller links exist. |
| `HANDOFF_TO_LUNA.md` | LEGACY | Refers to an external historical package and older Illustrious/Krea/Klein operating procedure. Preserve for provenance, not startup. |
| old Klein HTML review / A-B documents | LEGACY | Historical calibration evidence, not current app operation. |
| MiniMax notes/workflow docs | EXPERIMENTAL | Keep explicitly experimental until a current product caller is demonstrated. |

Documentation truth rule: “implemented”, “experimental”, “planned” and “legacy” are kept separate. The README does not claim that the UI currently drives the split Golden E2E.
