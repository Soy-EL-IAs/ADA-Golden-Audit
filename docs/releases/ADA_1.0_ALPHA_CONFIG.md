# ADA 1.0 Alpha effective configuration

Captured from the live configuration on 2026-08-25. Machine-specific roots and secrets are intentionally omitted.

## Agent roles

| Role | Model | Context | TTL | Status |
|---|---|---:|---:|---|
| Master / Smart | `qwen3.8-27b-uncensored` | 16,384 | 900 s | Configured; orchestration disabled by default |
| Vision Worker | `qwen/qwen3-vl-8b` | 8,192 | 300 s | Configured |
| Premise specialist | `qwen3.5-9b-uncensored-hauhaucs-aggressive` | 16,384 | 300 s | Configured |
| Illustrious specialist | same 9B model | 8,192 | 300 s | Configured |
| Klein specialist | same 9B model | 8,192 | 300 s | Configured |
| MiniMax specialist | same 9B model | 12,288 | 300 s | Configured |
| Visual Review specialist | `qwen/qwen3-vl-8b` | 8,192 | 300 s | Configured |

Shared settings: one parallel request, flash attention enabled, GPU KV cache enabled. The Master also configures a 512-token reasoning budget and MTP speculative draft.

## VRAM policy

- Release/unload timeout: 90 seconds.
- Poll interval: 2 seconds.
- Minimum free ratio before ComfyUI handoff: 0.75.
- Runtime jobs also serialize GPU work with `data/gpu_execution.lock`.

## Active product renderer profile

`config/production_profiles.json` selects `lustify_primary`.

### Lustify Krea2 primary

- Workflow: `workflows/production/lustify_krea2_primary_v1_api.json`.
- Checkpoint: `lustifyNSFWCheckpoint_v10Krea2.safetensors`.
- Text encoder: `qwen3vl_4b_fp8_scaled.safetensors` (`krea2`).
- VAE: `qwen_image_vae.safetensors`.
- Size: 1152 × 1536; batch 1.
- Steps: 8; CFG 1.0; sampler `euler`; scheduler `simple`; denoise 1.0.
- Direct T2I supported; latent Img2Img delegated to the conditional Lustify preset.

### Lustify identity fallback

- Workflow: `workflows/production/lustify_krea2_img2img_v1_api.json`.
- Size: 1024 × 1536; steps 8; CFG 1.0; `euler/simple`; denoise 0.55.
- Status: production conditional.

### Miaomiao optional secondary

- Workflow: `workflows/production/miaomiao_anima16_secondary_v1_api.json`.
- Checkpoint: `miaomiaoHarem_anima16.safetensors`.
- Text encoder: `qwen_3_06b_base.safetensors`.
- VAE: `qwen_image_vae.safetensors`.
- Size: 832 × 1216; batch 1.
- Steps: 25; CFG 4.0; sampler `euler`; scheduler `normal`; denoise 1.0.
- Status: optional secondary; anime-only direct T2I.

## Split specialist pipeline

The headless/specialist path remains configured and uses separated workflows:

- Illustrious: `workflows/production/illustrious_only_api.json`.
  - `waiIllustriousSDXL_v160.safetensors`, 768 × 1376, 14 steps, CFG 4.5, `euler_ancestral/normal`.
- Klein: `workflows/production/klein_only_api.json`.
  - `flux-2-klein-9b-fp8.safetensors`.
  - Encoder `qwen_3_8b_fp8mixed.safetensors`; VAE `flux2-vae.safetensors`.
  - 1024 × 1024, 6 steps, guidance 4.0, CFG 1.0, `euler/flux2`.
  - LoRAs: `anime2real-semi` at 0.5 and `klein_snofs_v1_3` at 0.3.
  - Timeout 1,200 seconds.

## Historical configuration still present

`config/pipeline.json` explicitly labels Illustrious and Klein as deprecated for the current primary renderer pipeline while retaining them for specialized/source-preserving use. This is intentional coexistence, not a single unified pipeline.

## Portability boundary

`config/ada.local.json` contains machine-specific roots and is not a portable release snapshot. A committed example file exists. The release must add an explicit ignore/tracking policy before certification.

