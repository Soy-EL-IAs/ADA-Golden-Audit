# PROPOSAL-UX-002 — Routable tabs and deep links

## Problema

Tabs do not alter the URL. Refresh returns Home and browser Back/Forward cannot restore a previous surface or entity.

## Evidencia

Manual navigation audit across all primary tabs; URL remains `/`.

## Impacto

Medium. It harms recovery, shareable diagnostics and user expectations, but does not block current single-session use.

## Comportamiento actual

Client code toggles classes directly with no route state.

## Comportamiento propuesto

Introduce a minimal URL state contract such as `/#/library`, `/#/characters` and `/#/missions/<id>`, with guarded missing-entity views. Keep backend API ownership unchanged.

## Alternativas

- Query-string state (`/?tab=library`).
- Server-rendered routes per page.

## Riesgos

History loops, stale entity IDs and reloading modal-only states require explicit rules.

## Archivos involucrados

`ada_app/static/app.js`, `ada_app/templates/index.html`, optional FastAPI fallback routes.

## Esfuerzo aproximado

Medium, 1–3 days including navigation tests.

## Recomendación

Use hash routes first; they preserve the current deployment and headless architecture.

