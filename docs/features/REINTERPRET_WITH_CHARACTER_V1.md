# Reinterpret with Character v1

Library assets can be reused semantically without copying an old renderer prompt.

1. The source asset yields `scene_template_spec_v1`: reusable action, setting,
   composition, expression and visual hook, plus explicit preserve/not-preserve lists.
2. A selected registered character becomes a fresh Character Contract.
3. The combination produces `reinterpreted_render_spec_v1` and a renderer-specific
   prompt artifact.
4. The request is persisted under `data/reinterpretations/` as `READY_FOR_RENDER`.

V1 is **direct reinterpretation** only. It does not submit a render and does not claim
source-image conditioning. Strict, Balanced and Loose choose the intended template
relationship in provenance; actual conditioned modes wait for validated recipes.

Future extensions: Lustify latent img2img, reference/edit with an edit-trained adapter,
style-reference and pose/depth/silhouette structure control. They require source-image
receipt fields and verified local workflows before being selectable.
