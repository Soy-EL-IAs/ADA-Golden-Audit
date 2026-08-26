# ADA Base Migration v1 — Inventory

Generated: `2026-08-21T17:26:45.826068-03:00`

Source: `C:\Users\ELIAS\Documents\Codex\2026-08-20\referenced-chatgpt-conversation-this-is-an\outputs\luna_pipeline`

Files: **1190**
Total bytes: **588912653**

## Top-level inventory

| Path | Files | Bytes |
|---|---:|---:|
| `HANDOFF_TO_LUNA.md` | 1 | 4525 |
| `LOCAL_OPERATOR_README.md` | 1 | 1449 |
| `README.md` | 1 | 12769 |
| `START_LOCAL_OPERATOR.cmd` | 1 | 163 |
| `character_dataset_staging` | 5 | 18603 |
| `character_refs` | 11 | 54039 |
| `config` | 13 | 16628 |
| `data` | 3 | 8830873 |
| `docs` | 8 | 20415 |
| `experimental` | 4 | 75944 |
| `experimental_runs` | 64 | 30524739 |
| `klein_ab_tests` | 13 | 17816145 |
| `klein_batch_runs` | 11 | 127179 |
| `lmstudio_mcp_entry.json` | 1 | 526 |
| `lmstudio_mcp_full.json` | 1 | 786 |
| `lmstudio_mcp_searxng.json` | 1 | 526 |
| `premises` | 4 | 184886 |
| `prompts` | 7 | 160858 |
| `render_only_runs` | 892 | 490994839 |
| `runs` | 61 | 39088924 |
| `schemas` | 1 | 392 |
| `scripts` | 44 | 616203 |
| `search` | 2 | 826 |
| `visual_review_runs` | 32 | 255561 |
| `workflows` | 8 | 104855 |

## Path classification

- `configuration`: 44 hits
- `documentation`: 61 hits
- `historical_metadata`: 1351 hits
- `runtime_active`: 86 hits

## Migration decisions

- Runtime/configuration paths are patched only after copying to Ada.
- Historical paths remain unchanged and use legacy compatibility resolution when needed.
- ComfyUI and LM Studio remain external; models/checkpoints/LoRAs are not duplicated.
- Generated asset junction is deferred until the real ComfyUI output folder is measured and copied safely.

## Detailed path hits

The machine-readable inventory contains every hit with file, line, classification, pattern and excerpt.
