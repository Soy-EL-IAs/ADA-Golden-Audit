# Character-aware Lustify fallback — 2026-08-25

## Decision

ADA may route an explicit Lustify request through:

`Miaomiao same-concept identity source → Lustify true latent Img2Img`

only when the registered character capability says `Lustify.direct = unreliable`.
The production recipe is `lustify_krea2_img2img_v1`, using the normal Lustify model,
Qwen3-VL FP8 encoder, Qwen image VAE, AuraFlow sampling and `denoise 0.55`.

## Reason

The controlled Ghislaine Dedoldia experiment showed that Lustify direct had strong
image quality but weak character identity. Miaomiao direct produced a recognizable
Ghislaine. Recipe B encoded that trusted source into the initial latent and produced
the best balance of identity, composition and increased realism.

Recipe A, reference conditioning without the source latent, produced severe artifacts.
Recipe C, reference conditioning plus Img2Img, preserved identity but remained too close
to anime. Neither is promoted to production.

## Guardrails

- Capability is stored per character; no unsupported global inference is made.
- The Miaomiao source must pass identity review before Lustify is submitted.
- The intermediate is recorded as `identity_reference` and excluded from normal Library.
- The final receipt records the source asset, recipe, mode and effective renderer.
- Missing or failed identity evidence stops the route; ADA does not fall back to direct
  Lustify silently.
- Model Lab outputs are evidence only and are not imported into Library automatically.

## Evidence

- Experiment: `experimental_runs/model_lab/lustify_identity_reference_ghislaine_001/`
- Accepted receipt: `recipes/B_latent_img2img/model_test_receipt.json`
- Production configuration: `config/pipeline.json`
- Character capability: `config/characters.json`

## Known debt

The current fallback creates a same-concept Miaomiao source when needed. A reusable,
human-approved Character Reference registry remains future work; it must not select an
arbitrary historical image by latest-file semantics.

## Reversibility

Remove the character's fallback capability or change its explicit recipe to stop future
conditional routing. Existing receipts and Library lineage remain immutable.

