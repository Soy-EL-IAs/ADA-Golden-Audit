# Audit Context

## High-Level Overview
ADA is an AI-driven image generation, curation, and character persistence pipeline. It acts as an orchestrator that manages complex workflows for creative expansion, character grounding, rendering using local and external models, and visual quality review.

## Golden State
This snapshot represents the "ADA Current Post-Golden Audit Snapshot". There is evidence of a validated Golden E2E run, meaning the primary pipeline has been demonstrated to reach a functional end-to-end state. However, subsequent development and research are included here, so this directory contains both the Golden implementation and post-Golden contextual work.

## Primary Components
- **Frontend / ADA App:** da_app/ - The user interface and web application.
- **Orchestration & Logic:** scripts/ - Contains the pipeline logic, orchestrators, specialist agents, and routing logic (e.g., specialist_orchestrator.py, un_full_pipeline.py).
- **Persistence & Library:** data/ (especially data/library, data/characters, data/missions) - Storage of generated assets, characters, and runtime state.
- **Contracts & Schemas:** schemas/ - JSON schemas defining the data contracts for agents and workflows.
- **Workflows:** workflows/ - ComfyUI and API workflows used to interface with generative models.
- **Tests:** 	ests/ - The test suite validating isolation, pipeline steps, and utilities.

## Entrypoints
- da.py / START_ADA_APP.cmd: Main application entrypoints.
- scripts/run_full_pipeline.py: Example pipeline runner.

## External Components
ADA relies conceptually on several external systems:
- **LM Studio** for local LLM and VLM inference.
- **ComfyUI** for local stable diffusion / image generation.
- **SearXNG** for local search capabilities (optional).

> **IMPORTANT**: Some documents under docs/research describe proposed or VNEXT ideas. They are contextual material only. The auditor must verify actual implementation against source code and must not assume research documents represent current behavior.
