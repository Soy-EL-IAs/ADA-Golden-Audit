# PROPOSAL-ARCH-001 — Explicit product pipeline authority

## Problema

ADA has two implemented production surfaces: the app renderer path (Lustify/Miaomiao) and the split specialist path (Illustrious/Klein). Documentation and UI can describe one while runtime uses the other.

## Evidencia

`config/production_profiles.json` selects `lustify_primary`; `scripts/production_workflows.py` simultaneously pins the split Illustrious/Klein graphs. Both have real persisted receipts.

## Impacto

High architectural ambiguity, especially for the Golden E2E definition.

## Comportamiento actual

Scene/Stock missions in the app use the renderer pipeline. Specialist/headless runs can use Premise → Illustrious → Review → Klein → Final Review.

## Comportamiento propuesto

Define a versioned pipeline profile as the explicit mission input and persist it on every mission/run. UI should show the chosen profile without owning its rules. Alpha may certify both profiles separately, but only one should be the default Golden E2E.

## Alternativas

- Deprecate the specialist split path.
- Revert app production to the specialist split path.
- Keep both indefinitely without profile identity (not recommended).

## Riesgos

Changing defaults can invalidate benchmarks, character capability routes and recovery behavior.

## Archivos involucrados

Configuration, mission contract, renderer/specialist orchestrators, UI status, receipts and docs.

## Esfuerzo aproximado

Large, 1–2 weeks with migration and E2E evidence.

## Recomendación

Do not unify during the Alpha checkpoint. Certify truthfully, then make the profile contract the first architecture item after release.

