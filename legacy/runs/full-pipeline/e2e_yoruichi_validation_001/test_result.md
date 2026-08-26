# ADA E2E Manual Test Result

## Test ID

`E2E_YORUICHI_MISSION_001`

## Date

2026-08-24

## Objective

Validate the complete ADA production path:

Character Request → Character Bootstrap → Character Reference Resolution → Creative Expansion M1 → Concept Selection → Illustrious Generation → Klein Refinement → Machine Review → Library Asset Creation → Human Review.

## Input

- Requested character: Shihouin Yoruichi
- Franchise: Bleach
- Requested output: multiple creative concepts and final approved assets

## Overall Result

**PARTIAL SUCCESS** — the E2E reached Library asset generation. Technical execution completed; creative quality and traceability observations remain for a later Creative Intelligence iteration.

## Stage Results

### 1. Character Bootstrap — SUCCESS

The onboarding resolved `Shihouin Yoruichi`. The historical fallback from an unregistered character to `2B` was not reproduced.

Observation: the profile resolved copyright and appearance/outfit tags, but the available structured profile is still thinner than the desired explicit identity/outfit representation. This increases reliance on model inference.

### 2. Creative Expansion M1 — SUCCESS WITH QUALITY ISSUES

- Model: `qwen3.5-9b-uncensored-hauhaucs-aggressive`
- Selected concept: `m1_shihouin_yoruichi_12`
- Recorded selection scores: Quality 88; Diversity 88

The selected concept used an extreme macro close-up with identity cues (yellow eyes, purple hair), finger gesture, intimate framing and steam. Creative Expansion worked, but selection favored immediate visual hook more strongly than character fidelity.

### 3. Illustrious Generation — SUCCESS

- Workflow: `illustrious_only_api.json`
- Checkpoint: `waiIllustriousSDXL_v160`
- Parameters: 768×1376, 14 steps, CFG 4.5, Euler ancestral, normal

When the prompt included `Shihouin Yoruichi from Bleach`, the image preserved recognizable skin tone, purple hair, yellow eyes and personality. Runs that rely on generic appearance tags risk producing a generic character. The desired contract is character name + franchise + identity anchors + scene description.

### 4. Klein Refinement — SUCCESS

- Workflow: `klein_only_api.json`
- Model: `flux-2-klein-9b-fp8`
- LoRA: `flux/A2R_Klein_Standard.safetensors`, strength 0.50

Klein preserved face, broad identity, composition and general pose. The review identified outfit drift: missing thighhighs/leotard and incomplete outfit preservation. A later prompt-quality iteration should keep explicit outfit anchors alongside identity and scene preservation.

### 5. Machine Review — SUCCESS

- Illustrious Review: PASS
- Final Review: MINOR_DEFECT

The review layer detected outfit drift, missing steam and minor composition changes.

### 6. Library Integration — PARTIAL

The asset was created with mission, source-run, prompt, seed, workflow and review provenance. The manual test recorded that a direct Illustrious-versus-Klein comparison view was unavailable; this is a documented observation only, not an instruction to alter the currently isolated production workflow surface.

## Evaluation

- Technical score: 8.5 / 10
- Creative score: 5 / 10

The architecture is operational. The next optimization area is the Creative Intelligence Layer rather than infrastructure or workflow/runtime separation.

## Follow-up Priorities

1. Character profile completeness.
2. Explicit character identity in Illustrious prompts.
3. Outfit anchors in Klein preservation.
4. Mission/Library visual traceability.

See `findings.json` for machine-readable findings and `run_metadata.json` for the recorded execution context.
