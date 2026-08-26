# Klein semi-realistic provisional baseline

This is ADA's current provisional baseline for illustration/anime to semi-realistic, photo-like finalization with limited identity drift.

## Manual best-result prompt

> Create a realistic photo version of the source image. Strictly preserve exact facial identity, facial proportions, expression, pose, framing, hairstyle, outfit, tan skin, purple hair and vivid golden-yellow eyes. Improve realism through skin texture, hair strands, realistic fabric and lighting only. Do not redesign the face or change the expression.

The production compiler uses the same short structure but injects the active character's identity anchors from the Stage Render Plan instead of hardcoding the example traits. This prevents the Yoruichi-specific colors from contaminating other characters.

## Effective LoRA chain

Application order is significant:

1. `flux/anime2real-semi.safetensors`, strength `0.50`
2. `flux/klein_snofs_v1_3.safetensors`, strength `0.30`

The production workflow keeps its single normal output node. No manual test-only save node is included.

Status: provisional baseline, intended to remain simple and reversible until broader manual evaluation replaces it.
