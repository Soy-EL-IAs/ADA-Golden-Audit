# ADA MiniMax F2V integration notes

Source workflow:
`MiniMax H3 T2V-I2V-FL2V EMA Turbo - RTX 5070 Ti (1).json`

The uploaded workflow already contains the required MiniMax H3 first-frame path. fileciteturn13file0

## Clean workflow created

`minimax_f2v_ada_clean_ui.json`

This is still a **ComfyUI UI-format workflow**, not an API-format export. I deliberately did not fabricate an API graph because the source contains a ComfyUI subgraph/custom-node definition and a reliable API export should be produced by ComfyUI itself.

## Production parameter map

| Purpose | Node ID | Current node |
|---|---:|---|
| First frame | 191 | `LoadImage` |
| MiniMax prompt | 138 | `PrimitiveStringMultiline` |
| Duration | 229 | `PrimitiveFloat` |
| Resolution | 228 | `AcademiaSD_ResolutionCalc` |
| Seed | 193 | `AcademiaSD_Noise` |
| Steps | 239 | `Int` |
| Main MiniMax process | 160 | `ADA F2V — MiniMax H3 EMA Turbo` |
| Video output | 238 | `VHS_VideoCombine` |
| Optional sensual motion LoRA | 231 | `AcademiaSD_MultiLora` |

## Removed from the ADA F2V production path

- last-frame loader / FL2V input
- LM Studio JIT prompt generation
- manual IDEA helper
- prompt preview
- MiniMaxDirectorEasy
- Google Translate helper
- UI notes
- frame/performance group bypasser helpers

## Preserved intentionally

- MiniMax H3 model / text encoder / VAEs
- EMA Turbo LoRA
- current memory/performance patches
- current low-VRAM nodes
- `AcademiaSD_MultiLora`, including the currently active `breastplayjiggle_h3_v1.safetensors`
- VHS MP4 output
- current duration / resolution / steps / seed controls

## Important next step

Open `minimax_f2v_ada_clean_ui.json` in the user's local ComfyUI and export it using **Save (API Format)**.  
That exported file should become:

`D:\IA\Ada\workflows\minimax_f2v_api.json`

After that, ADA can safely implement `minimax_render()` around a real ComfyUI API graph instead of guessing how the frontend subgraph expands.

## Intended ADA runtime contract

ADA only needs to inject:

1. approved final still as first frame,
2. compiled MiniMax temporal hook prompt,
3. seed,
4. duration,
5. resolution,
6. steps,
7. output filename prefix.

Expected result:

`approved Klein image -> MiniMax F2V -> MP4 + metadata`
