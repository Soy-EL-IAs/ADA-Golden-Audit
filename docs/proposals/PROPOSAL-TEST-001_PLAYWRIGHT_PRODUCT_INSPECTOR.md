# PROPOSAL-TEST-001 — Playwright Product Inspector

## Problema

ADA has browser evidence but no repository-owned Playwright inspector, package manifest or lockfile. Installing a new dependency is outside small-fix authority and the owner temporarily requested no new tests.

## Evidencia

The audit navigated the live product through the in-app browser and captured stable before/after screenshots, but those actions are not reproducible by CI from this repository.

## Impacto

Navigation, screenshot contracts, responsive regressions and busy/running UX remain manual certification items.

## Comportamiento actual

Manual browser inspection plus Python unit tests.

## Comportamiento propuesto

Add a minimal pinned Node project under `tests/product-inspector/`, a Playwright config targeting an externally started local ADA server, deterministic read-only smoke cases, unique IDs for mutating tests and screenshot output under `audit_evidence/` or disposable test artifacts.

## Alternativas

Keep manual inspection; use Python browser tooling; run a centrally managed external inspector.

## Riesgos

New dependency/toolchain, browser downloads, accidental writes to production runtime data and screenshot instability.

## Archivos involucrados

`package.json`, lockfile, `tests/product-inspector/`, CI/startup documentation and isolated test-data configuration.

## Esfuerzo aproximado

Medium: one focused implementation plus environment-isolation review.

## Recomendación

Approve only after a test-data root and server lifecycle contract are defined. Start with read-only Home/Library/Characters/Settings/404 inspections, then add isolated mutation flows.
