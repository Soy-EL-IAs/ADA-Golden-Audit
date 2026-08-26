# Direct Generator Benchmark v1

## Scope

This benchmark asks one narrow question: which tested model and explicit recipe is the strongest direct anime generator for ADA?

It is isolated under `experimental_runs/model_lab/`. It does not alter production Illustrious, Klein, Missions, Character Contracts, routing, prompts, models, or workflows. A benchmark result is evidence only; there is no automatic promotion into production.

## Role

`direct_anime_generator` means that a model receives a Character Contract snapshot plus a scene prompt and produces the final anime/illustration image directly. Capability remains `unknown` until a run receipt has a human evaluation. `benchmark_ready` only means that the loader, dependencies, workflow snapshot, bindings, and settings are reproducible.

Qwen 3.5 and `Anima-3.8B-expanded_adapter` are auxiliary components of the Anima recipe. They are not ranked as generators.

## Versioned recipes

Every recipe manifest lives in `experimental_runs/model_lab/recipes/` and declares:

- exact model and loader;
- immutable API workflow snapshot and its manual source evidence;
- prompt style (`descriptive`, `booru_tags`, or `hybrid`);
- width, height, and `batch_size: 1`;
- sampler, scheduler, steps, CFG, denoise, and negative prompt;
- all checkpoint, text-encoder, adapter, and VAE dependencies;
- explicit prompt, seed, and output bindings.

Initial recipes:

| Recipe | Model | Prompt style | Resolution | Sampling |
|---|---|---|---|---|
| `lustify_krea2_direct_v1` | Lustify Krea2 | descriptive | 1152×1536 | Euler/simple, 8 steps, CFG 1 |
| `miaomiao_anima16_direct_v1` | Miaomiao Anima16 | booru tags | 832×1216 | Euler/normal, 25 steps, CFG 4 |
| `anima_3_8b_direct_v1` | Anima 3.8B | hybrid | 832×1216, then 1.25× latent upscale | res_multistep/beta, 40-step first pass and 14-step refinement |

The snapshots were derived from successful manual ComfyUI executions. UI-only preview nodes were replaced with one experimental `SaveImage` output; an empty Lustify Power Lora node was omitted because it applied no adapter.

## Benchmark manifest

`direct_generator_benchmark_001` starts with three hard cases:

1. Yoruichi on a neon rooftop after rain with a black cat;
2. Yoruichi in a shower/mirror scene with wet canonical outfit;
3. Ghislaine in an action pose stressing anatomy, beast traits, tattoo, and outfit.

Each case stores a lab-local Character Contract snapshot, neutral scene intent, seed, recipe-specific effective prompt, eligible models/recipes, and evaluation dimensions.

## Execution contract

The Model Lab UI requires a test case and an explicit model/recipe selection. One click submits exactly one image (`batch_size: 1`). It never creates a Mission and never enters production routing.

Each execution writes:

- `effective_workflow.json` with the actual prompt, seed, and output prefix;
- `model_test_receipt.json` with model/version, checkpoint, adapters, recipe/version, prompt, negative prompt, seed, workflow, dependencies, resolution, sampler settings, total duration, ComfyUI inference duration, VRAM snapshots, output, and errors.

Human evaluation uses a 1–10 scale for identity, face, hairstyle, eye color, outfit, pose/anatomy, composition, environment, prompt adherence, visual appeal, and overall quality.

## Rankings

Rankings are produced only from human evaluation receipts:

- model ranking for the `direct_anime_generator` role;
- recipe ranking;
- speed-versus-quality table using human overall score and measured inference time (falling back to total duration only when ComfyUI timing is unavailable).

Different recipes for the same model remain distinct. Untested combinations are never inferred or promoted.
