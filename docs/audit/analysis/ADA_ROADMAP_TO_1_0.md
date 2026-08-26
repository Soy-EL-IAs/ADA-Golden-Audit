# ADA Roadmap to 1.0
*Date: 2026-08-23*

## ADA 1.0 Definition
**ADA 1.0** is a fully local, resilient application that allows a user to request character concepts, automatically produces high-quality images via a multi-stage visual pipeline, autonomously retries defects, and curates successful results into a permanent visual library, without requiring command-line intervention or manual error recovery.

---

## Milestone 1: Autonomous Quality Loop (ADA 0.8)

### Goal
Empower the pipeline to actually fix its mistakes. Currently, Visual Review verdicts (`RETRY_ILLUSTRIOUS`, etc.) are ignored by the runner.

### Why now
The "Generate Pilot" flow is a straight line. It does not leverage the review agents to improve image quality, which defeats the purpose of the multi-agent architecture.

### Scope
- Implement a bounded retry loop (e.g., max 2 retries) inside `pilot_runner.py`.
- If `RETRY_ILLUSTRIOUS` is returned, regenerate the prompt and submit to ComfyUI again.
- Introduce a terminal `FAILED` pipeline state if retries are exhausted.

### Out of scope
- Changing the Visual Review prompt or logic.
- Human-in-the-loop manual corrections.

### Dependencies
- None.

### Acceptance criteria
- A candidate that fails Visual Review automatically triggers a new Illustrious generation.
- A candidate that repeatedly fails reaches a terminal `FAILED` state and does not appear in the Library.

### Risk
Medium (Requires careful state management to avoid infinite loops).

### Estimated effort
Medium.

---

## Milestone 2: Pipeline Reliability & Recovery (ADA 0.9)

### Goal
Prevent catastrophic pipeline crashes caused by minor LLM hallucinations or system hangs.

### Why now
`m1_2b_12` failed completely because the LLM generated invalid JSON. `m1_2b_05` failed because of a schema contract mismatch. These should not crash the background runner.

### Scope
- Wrap LLM agent calls in robust retry blocks (catching `JSONDecodeError` and `ContractError`).
- Fix `FileExistsError` by ensuring the orchestrator cleans up or safely resumes directories.
- Refactor ComfyUI execution in `pilot_runner.py` to use asynchronous polling instead of `wait_history()` thread-blocking, allowing the API to remain responsive.

### Out of scope
- Multi-PC distributed generation.
- Redis/Celery integration (keep it simple and local).

### Dependencies
- Autonomous Quality Loop.

### Acceptance criteria
- The pipeline survives 3 consecutive malformed JSON responses by retrying.
- Restarting a Pilot run over an existing directory cleanly resumes or overwrites without crashing.

### Risk
High (Touching core execution logic).

### Estimated effort
Large.

---

## Milestone 3: Production UX Hardening (ADA 1.0)

### Goal
Provide a seamless, transparent user experience for long-running batches.

### Why now
The UI is functional but lacks deep observability (e.g., why did a candidate fail?) and control (cannot cancel a run).

### Scope
- UI support for terminal `FAILED` states, exposing the exact error or review verdict that killed the candidate.
- A "Cancel Run" button to safely abort background generation.
- Capability to request a "Production Batch" (e.g., Top 10 concepts) now that the pipeline is reliable.

### Out of scope
- User login/Authentication.
- Cloud deployments.

### Dependencies
- Pipeline Reliability & Recovery.

### Acceptance criteria
- Users can view detailed error traces in the Pilot Gallery for failed candidates.
- Users can cancel a running pilot.

### Risk
Low.

### Estimated effort
Small.

---

## Future Horizons (Post 1.0)

### MiniMax / Video Generation
**When to include:** Post ADA 1.0. 
**Reasoning:** Video generation (MiniMax) is extremely expensive and requires a pristine, finalized starting image. ADA 1.0 must first consolidate the Image Production pipeline to guarantee that the starting assets are structurally perfect. Introducing video before stabilizing the image pipeline would amplify upstream errors and waste compute.

### Scheduling & Automation
Cron-based autonomous generation (e.g., "Generate 5 Tifa images every night") belongs in ADA 1.1 once reliability is proven.
