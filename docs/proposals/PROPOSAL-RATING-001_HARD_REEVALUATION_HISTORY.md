# PROPOSAL-RATING-001 — Preserve Hard Re-Evaluation history

## Problema

A new Hard Re-Evaluate replaces `human_review.hard_rating`, so the prior hard result is lost.

## Evidencia

`AssetLibrary.save_hard_rating()` directly assigns the new object. Stage human reviews already use append-only histories, demonstrating a safer precedent.

## Impacto

Repeated reevaluations cannot be audited over time and violate the release requirement to preserve prior evidence.

## Comportamiento actual

Original agent/human ratings remain, but only the latest hard rating survives.

## Comportamiento propuesto

Append immutable entries to `hard_rating_history`, including review ID, timestamp, reviewer/model/runtime version, original score, final score, delta, verdict and `supersedes_review_id`. Keep `hard_rating` as the derived latest entry for compatibility.

## Alternativas

Write separate receipt files and store only their IDs; disallow a second reevaluation; keep current overwrite behavior with an explicit warning.

## Riesgos

Review JSON growth, compatibility code and migration ambiguity for existing latest-only records.

## Archivos involucrados

`ada_app/asset_library.py`, Hard Re-Evaluate API/UI, schema/docs and tests.

## Esfuerzo aproximado

Small-to-medium, but it changes persisted data shape and therefore requires approval.

## Recomendación

Add append-only history with compatibility fallback; never synthesize missing history for old records.
