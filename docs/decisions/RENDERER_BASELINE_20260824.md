# Renderer baseline — 2026-08-24

## Decision

ADA production now renders directly with `lustify_krea2_primary_v1`. A Create request
selects exactly one renderer. `miaomiao_anima16_secondary_v1` is the explicit anime
alternative, not an additional output generated alongside Lustify.
Both consume the same Character Contract and Resolved Render Spec, then create their
own plan, prompt artifact, receipt, review observation, and output lineage.

## Evidence and scope

The decision is based on `experimental_runs/model_lab/manual_controlled_benchmark_20260824`
and the prior Model Lab receipts. Lustify was selected as the general direct renderer
because it covered anime, illustrated, semi-realistic and photo-like targets while
handling complex scenes well. Miaomiao is retained as the faster anime-oriented
renderer; it is not an automatic peer output.

## 2026-08-25 amendment

The general baseline remains unchanged, but direct capability is now allowed to vary
by character. When an explicitly selected Lustify route is marked unreliable for the
registered character, ADA may internally use Miaomiao as a trusted identity source and
then execute the verified Lustify latent Img2Img preset. This is a conditional fallback,
not dual generation and not a claim that Lustify direct is unreliable for every character.

See `CHARACTER_AWARE_LUSTIFY_FALLBACK_20260825.md`.

## Historical compatibility

Illustrious, Klein and Anima 3.8B are marked deprecated/discarded for the default
pipeline, not deleted. Old missions, receipts, final decisions, comparisons and
Library cards remain readable through the legacy lineage adapter. Klein remains a
historical specialized anime-to-semi-real source-preserving tool.

## Reversibility

`config/pipeline.json` is the single production renderer selection point. Restoring a
previous selection changes future missions only; it never rewrites completed run
artifacts or benchmark evidence.
