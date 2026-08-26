# ADA Model Registry and Model Lab v1

Model Lab is isolated from production workflows and Missions. Its artifacts live under `experimental_runs/model_lab/`.

## Discovery

`scripts/model_scanner.py` reads safetensors headers only. It records file size, embedded metadata, tensor count, dtypes, principal tensor keys, probable architecture, component type, classification evidence, and a header hash. It does not infer visual capabilities from filenames.

The primary discovery location is `D:\IA\Ada\downloads`. The local fallback is the current user's `Downloads` directory because the five initial files were physically found there. The registry always records the resolved source path.

Physical metadata is stored in `config/models_registry.json`. Capability claims are separate files under `config/model_capabilities/`. Unknown visual behavior remains `unknown` until a controlled test exists.

## Test safety

A discovered model is not automatically runnable. Model Lab requires an explicit confirmed test recipe. Unknown adapter or loader wiring is blocked rather than guessed.

Every run persists `model_test_receipt_v1` with model, configuration, prompt, seed, input, output, elapsed time, VRAM snapshots, result fields, and any error.

## Current production promotion

The controlled benchmark promoted `lustify_krea2_primary_v1` as the direct primary
renderer and `miaomiao_anima16_secondary_v1` as an opt-in secondary renderer. The
frozen settings are in `config/pipeline.json`; production workflow snapshots live in
`workflows/production/`. The decision and evidence boundary are recorded in
`docs/decisions/RENDERER_BASELINE_20260824.md`.

## Historical production reference

Klein remains the production reference and is not modified by Model Lab. The initial comparison recipe uses:

- `flux/anime2real-semi.safetensors` at `0.50`
- `flux/klein_snofs_v1_3.safetensors` at `0.30`

Reference prompt:

> Make it hyper-realistic while preserving the exact facial identity, facial proportions, expression, pose, framing, hairstyle and outfit of the source image.
>
> Keep her vivid golden-yellow eyes, tan skin and purple hair unchanged.
>
> Improve natural skin texture, facial detail, individual hair strands, realistic fabric and lighting.
>
> Do not soften or change her expression.

This prompt is a fixed Model Lab reference for the Yoruichi comparison. It is not a global character default.

## Benchmark Runner v1

Official benchmarks live under `experimental_runs/model_lab/benchmarks/<benchmark_id>/`. The layers are deliberately separate and append-only:

1. `model_test_case_v1` defines character, source, task, role, one or more eligible models, fixed prompt/seed and evaluation dimensions.
2. `model_test_receipt_v1` records one technical execution. Each execution runs exactly one model and records checkpoint, adapters, workflow, timing, VRAM, input and output.
3. `model_evaluation_receipt_v1` records a human evaluation using eight 1–10 dimensions.
4. Capability profiles aggregate human receipts by model and role. One evaluated sample produces `tested`, not `confirmed`; existing production evidence is never downgraded.

Initial roles are `identity_constructor`, `anime_to_real_converter`, `photorealistic_generator`, and `style_preserver`. Models remain `unknown` for a role until evidence exists. Rankings use the mean human `overall` score and display sample counts.

`identity_realism_benchmark_001` describes the intended Yoruichi, Ghislaine and 2B matrix, but its active first slice is limited to one character, one source image and one model execution. The initial Yoruichi/Klein receipt adopts the already completed controlled Model Lab sanity run, so initialization does not render a duplicate image.
