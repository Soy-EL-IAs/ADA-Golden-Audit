# ADA 1.0 Alpha VRAM arbitration audit

## Implemented boundary

The runtime serializes GPU work with `data/gpu_execution.lock`. Resource handoff code unloads/releases LM Studio before a ComfyUI submission and unloads/frees ComfyUI before loading the visual worker. The configured free-VRAM threshold is 0.75, with a 90-second release timeout and 2-second polling.

## Evidence

Four existing mocked transition tests passed:

1. LM unload/release precedes ComfyUI submit.
2. ComfyUI unload/release precedes LM visual-worker load.
3. The configured free-memory threshold is used.
4. The app pilot uses the same bidirectional handoffs.

Live preflight during the audit found ComfyUI idle with an empty running and pending queue. LM Studio responded on its configured endpoint and exposed no loaded model instance in the captured inventory.

## Safety decision

No live unload/free call was issued. A destructive unload was unnecessary for this audit and could interfere with concurrent owner work. Busy-state safety is therefore covered by code/tests but not live-certified against an active render.

Status: `PASS_WITH_KNOWN_ISSUE` until one controlled Golden run records the full live transition sequence and free-memory receipts.
