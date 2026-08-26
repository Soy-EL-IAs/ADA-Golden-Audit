# ADA Capability Matrix
*Date: 2026-08-23*

| Capability | Status | Evidence | Risk | Next Action |
|---|---|---|---|---|
| **ADA App Core (UI/API)** | DONE BUT NEEDS HARDENING | Runs on port 8000. `app.js` handles tabs, Dashboard reads system states. | Low | Add Cancel controls and detailed error logs. |
| **Creative Expansion (M2)** | DONE & VALIDATED | Generates diverse concepts via `qwen3.5-9b`. Artifacts stored in `proposal_records.json`. | Low | None. |
| **Semantic Guard / M3 / M4** | DONE & VALIDATED | Deterministically filters INVALID and selects Top N based on Quality/Diversity clustering. | Low | None. |
| **Generate Pilot Flow (M5)** | PARTIAL | `m1_2b_02` completed successfully, but `12` and `05` crashed due to unhandled exceptions. | High | Implement retry loops for LLM parsing and schema validation. |
| **Visual Quality Loop** | PARTIAL | Agents return `RETRY_ILLUSTRIOUS`, but the orchestrator runner ignores it and proceeds. | High | Wire up bounded retry logic in `pilot_runner.py`. |
| **Asset Library (M6)** | DONE & VALIDATED | `index.html` Library tab accurately reflects final assets. Favorites persist in `asset_review.json`. | Low | None. |
| **Unified Run Index** | DONE & VALIDATED | `ada_app/run_index.py` correctly parses both legacy `20260820_*` runs and modern `m2_*` pilot runs. | Low | None. |
| **Resilience & Recovery** | NOT STARTED | Crashes require manual intervention. Background tasks lock threads. | High | Refactor to async polling and graceful error trapping. |
| **MiniMax / Video** | EXPERIMENTAL | Code hints exist, but intentionally deferred. | Medium | Defer until ADA 1.1. |
