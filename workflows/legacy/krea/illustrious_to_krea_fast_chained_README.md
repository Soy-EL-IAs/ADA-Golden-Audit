# Illustrious FAST → Krea, one Queue

`illustrious_to_krea_fast_chained_api.json` is one ComfyUI API workflow. Its node path is:

`INPUT / JSON record → ILLUSTRIOUS FAST → decode → unload cached models → KREA → Illustrious/Krea/compare outputs`.

The Illustrious image is wired directly from `VAEDecode` into Krea's `ImageScale`; no file upload or second Queue is used. `FL_UnloadAllModels` sits between stages so ComfyUI can free the Illustrious checkpoint before it loads Krea when VRAM is constrained.

## FAST defaults

- Illustrious: `512×768`, `7` steps, CFG `4.5`, `euler_ancestral`.
- Krea: `768×1152`, `8` steps, CFG `1.0`, `euler` / `beta57`.
- Comparison: `easy imageConcat`, horizontal, no text.

Edit node `4` and node `5` for Illustrious A/B tests; edit nodes `13`, `14`, and `18` for Krea tests.

## JSONL adapter

ComfyUI currently has `Read JSON file [Crystools]`, but no installed JSONL record iterator. That means the workflow is intentionally one record per Queue; the generic adapter materializes a chosen JSONL line into this same one-queue graph:

```powershell
python scripts/export_chained_workflow.py --premises premises/sol_100.jsonl --premise-id chel_001 --output workflows/generated/chel_001_illustrious_to_krea_chained_api.json
```

The generated file contains the record-derived Illustrious prompt, negative, Krea preservation prompt, both seeds, and output names. Import it in ComfyUI using **Load (API workflow)**, then Queue once.

## Metrics

No timing node was added: node timing should be read from ComfyUI's `/history/{prompt_id}` response after the single Queue completes. It provides actual node execution durations and avoids a custom metadata/timer dependency. The generated workflow stores record id and both seeds under `_meta.record`.

## Validation performed

The Chel generated workflow has 21 nodes. All node class names and input names were checked against the current local `/object_info`; no generation was submitted during validation.
