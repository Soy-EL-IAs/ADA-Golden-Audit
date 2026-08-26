# PROPOSAL-UX-001 — Responsive product navigation

## Problema

The fixed 220 px sidebar leaves only 170 px of content at a 390 px viewport. Core Library controls and cards are clipped.

## Evidencia

`audit_evidence/gallery__mobile__baseline.png` and the measured layout (`sidebar=220`, `content=170`).

## Impacto

High for phone-sized windows; desktop and tablet remain usable.

## Comportamiento actual

Sidebar is always fixed and fully expanded. Product controls wrap inside the remaining width.

## Comportamiento propuesto

Below a documented breakpoint, replace the fixed sidebar with a compact top bar and an explicit navigation drawer. Preserve the same information architecture and tab semantics.

## Alternativas

- Collapse to icon-only 64 px rail.
- Declare a minimum supported width of 768 px for Alpha.

## Riesgos

Keyboard focus, screen-reader labeling and drawer state can regress if treated as CSS-only decoration.

## Archivos involucrados

`ada_app/templates/index.html`, `ada_app/static/style.css`, `ada_app/static/app.js`.

## Esfuerzo aproximado

Medium, 1–2 days with responsive/browser coverage.

## Recomendación

For Alpha, document 768 px as the supported minimum. Implement a drawer in ADA 1.1.

