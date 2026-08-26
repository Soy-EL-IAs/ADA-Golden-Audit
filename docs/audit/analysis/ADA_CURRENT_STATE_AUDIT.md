# ADA Current State Audit
*Date: 2026-08-23*

## 1. Architecture Map

### Product Layer
- **ADA App:** FastAPI backend + Vanilla JS/Bootstrap frontend. Local dashboard interface.
- **Dashboard:** Reads system status (LM Studio, ComfyUI, models).
- **Creative Lab:** Generates concepts via `run_m2.py`.
- **Pilot Gallery:** Tracks active background Pilot runs via `/api/runs/{run_id}/pilot`.
- **Runs:** Exposes all historic and active runs through the Unified Run Index.
- **Library (New):** Presents final approved assets across all runs. Supports Character Collections and Favoriting.

### Creative Layer
- **Creative Expansion (M2):** `qwen3.5-9b-uncensored-hauhaucs-aggressive` generates `ConceptProposal` schemas.
- **Semantic Guard (M1):** Evaluates logical adherence.
- **Diversity / Quality (M3):** Deterministic clustering and quality scoring.
- **Auto Selection (M4):** Filters non-PASS and picks top N candidates deterministically.

### Image Production
- **Specialist Orchestrator:** Manages state transitions for a specific premise.
- **Illustrious:** 1st pass generation (JSON prompt + ComfyUI).
- **Visual Review:** Qwen-VL (8B/30B) evaluates Illustrious outputs.
- **Klein:** 2nd pass refine generation.
- **Final Review:** Qwen-VL final quality check.

### Runtime / Orchestration
- **State:** `manifest.json` for legacy/creative, `pilot_candidates.json` for pilots.
- **Execution:** Heavy tasks run synchronously inside a FastAPI `BackgroundTasks` thread or `threading.Thread`.
- **Models:** LM Studio endpoints for inference. ComfyUI for image generation.

---

## 2. Generate Pilot Validation (m2_2b_20260823_130059)

**Status:** `PARTIAL` (Not fully hardened).

**Metrics:**
- **Concepts Generated:** 12
- **M3/Semantic Validated:** 12
- **M4 Selected:** 3 (`m1_2b_02`, `m1_2b_12`, `m1_2b_05`)
- **Began Illustrious:** 3
- **Completed Illustrious:** 2 (`m1_2b_12` failed due to `LM Studio returned no valid illustrious_output_v1 JSON`)
- **Visual Review:** 2
- **Began Klein:** 2
- **Completed Klein:** 1 (`m1_2b_05` failed due to missing identity elements triggering a schema validation error).
- **Final Review:** 1 (`m1_2b_02` returned `RETRY_ILLUSTRIOUS`).
- **Terminal States:** 
  - `m1_2b_12`: ERROR (JSON parsing).
  - `m1_2b_05`: ERROR (Schema validation).
  - `m1_2b_02`: COMPLETE (despite failing Final Review, the runner lacks a proper retry loop).

**Conclusion:** The happy-path works, but the pipeline lacks bounded retries and fails silently/hard on minor LLM hiccups. It is not fully autonomous yet.

---

## 3. Semantic States

- **M3/M4 Precedence:** Fixed. `semantic FAIL` forces `recommendation = INVALID`, preventing M4 from selecting it.
- **Run vs Candidate state:** UI and Backend states diverge. A candidate completing forces its pipeline state to `COMPLETE`, but if it failed Final Review, it should actually trigger a retry or `FAILED` state. Currently, a `RETRY_ILLUSTRIOUS` verdict is ignored by the runner and falsely pushed to `COMPLETE`.

---

## 4. Library Validation

- **Indexing:** Correctly scans legacy runs (`20260820_*`) and Pilot runs (`m2_*`), extracting provenance safely.
- **Missing Data:** Gracefully handles missing reviews/telemetry (shows `UNKNOWN`).
- **Resilience:** The index can be rebuilt at will without touching raw artifacts.
- **Curations:** `Favorites` persist across rebuilds in an isolated `asset_review.json` file.
- **Validation:** PASS. The Library functions perfectly as a read-only presentation layer.

---

## 5. Technical Debt

### Critical
1. **Missing Orchestration Retry Loops:** `pilot_runner.py` advances linearly regardless of `RETRY_*` verdicts from Visual/Final Reviews.
2. **LLM Fragility:** No robust retry for `JSONDecodeError` or schema violations during agent calls.
3. **Blocking Threads:** ComfyUI submissions block the API background thread via `wait_history()`, freezing status updates.

### High
1. **FileExistsError:** The Orchestrator crashes if restarted on an existing candidate directory without cleanup.
2. **VRAM Clashing:** Uncoordinated loading/unloading between LM Studio and ComfyUI.

### Medium
1. **State Fragmentation:** `manifest.json` vs `pilot_candidates.json` logic creates duplicate parsing paths.

---

## 6. Product Experience

**What can a user do today?**
- Request N concepts for a character.
- Automatically filter and generate the top 3 through a complex visual pipeline.
- View real-time progress.
- Browse a library of final approved images, compare them with base generations, and favorite them.

**What requires knowing internals?**
- Recovering a crashed pipeline.
- Fixing VRAM OOMs manually.
- Forcing a retry on a specific image.

ADA is very close to a usable V1 product. It has transitioned from a collection of scripts to a cohesive web application.
