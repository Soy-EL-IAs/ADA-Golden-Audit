# PROPOSAL-STATE-001 — Persisted mission reconciliation

## Problema

Mission JSON can remain in an active status after process loss, terminal failure or partial historical migrations. Home then presents work as running indefinitely.

## Evidencia

Five records from 2026-08-23 are counted in progress while ComfyUI is idle. One has a terminal timestamp and failure detail but `status=PRODUCING`; another has `status=CREATED` and five approved assets without a source run.

## Impacto

High. It breaks `queued != running != completed`, misleads users, and weakens restart trust.

## Comportamiento actual

`GET /api/missions` returns persisted JSON without reconciliation. Background thread identity/heartbeat and last-update time are not part of the model.

## Comportamiento propuesto

- Persist `updated_at`, `worker_instance_id` and optional heartbeat while active.
- At startup, inspect non-terminal missions against process ownership, GPU lock, ComfyUI queue and persisted artifacts.
- Never silently mark terminal from age alone.
- Classify stale records as `RECOVERY_REQUIRED`, retaining original status and evidence.
- Offer an explicit Resume or Mark failed action with an audit receipt.

## Alternativas

- UI-only age warning: safer but does not reconcile backend truth.
- Automatically mark all old active records failed: simple but destructive to evidence.

## Riesgos

Incorrect reconciliation can duplicate work or mask a genuinely running external worker.

## Archivos involucrados

`ada_app/mission.py`, `ada_app/mission_runner.py`, `ada_app/main.py`, `ada_app/run_reconciliation.py`, Home/mission UI and mission schemas.

## Esfuerzo aproximado

Medium, 2–4 focused days including crash/restart tests.

## Recomendación

Implement after Alpha baseline as the highest-priority state reliability item.

