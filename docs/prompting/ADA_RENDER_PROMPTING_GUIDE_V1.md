# ADA Render Prompting Guide v1

**Status:** current prompting baseline. **Historical note:** Illustrious/Klein and
Krea-era prompt documents remain evidence only; they are not the default for new work.

## Semantic chain

`Character Contract + Hook Premise v2 → Resolved Render Spec v2 → renderer compiler`

The hook is a structured visual moment, not prompt text. It records hook type,
snapshot, action, object interaction, setting, composition, expression and render
intent. The spec is shared semantic truth; each renderer creates its own prompt.

## Render intent

`anime`, `semi_realistic`, and `photorealistic` are real compiler inputs. Lustify
uses natural descriptive language and changes its medium/material clauses accordingly.
Miaomiao uses compact hybrid tags and is an optional fast anime path, not the primary
photorealistic route.

## Lustify

`lustify_prompt_compiler_v4` uses subject/identity, outfit, visible action and object
interaction, setting, composition, expression, then material and lighting detail. It
does not use SDXL weighting syntax or copied negative-token lists. The validated
baseline uses zeroed negative conditioning.

`DIRECT_T2I` is the general path. `LATENT_IMG2IMG` is integrated only through the
verified conditional preset `lustify_krea2_img2img_v1`; it receives a validated source
image and adds strict source-preservation language before the resolved scene prompt.
`REFERENCE_EDIT`, `STYLE_REFERENCE`, and `STRUCTURE_CONTROL` remain declared but are
not production-supported without a separately verified local recipe.

## Miaomiao

`miaomiao_prompt_compiler_v1` generates a concise sequence: quality, named character,
identity anchors, outfit, action, setting, expression and framing. It never receives
the Lustify prose string.

## Anti-patterns

- Attribute lists without a known character name.
- Contradictory media directions.
- Repeating realism synonyms.
- Exact-source preservation instructions in direct T2I.
- Adding LoRAs by popularity rather than a named capability and measured evidence.

Baseline Lustify has no optional adapters. Style/reference, detail, realism and
pose/depth/silhouette adapters are candidates only; every future use must be explicit
in its recipe and receipt.

Candidate metadata lives in `config/renderer_adapter_candidates.json`; it is not a
pipeline configuration and none of those adapters is loaded by default.
