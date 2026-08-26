# ADA 1.0 Alpha error UX audit

## Safely observed

| Case | Result | Status |
|---|---|---|
| Invalid application URL | FastAPI returns structured 404 JSON; the existing shell does not enter an inconsistent partial screen. | PASS_WITH_KNOWN_ISSUE |
| Missing mission | API returns a clear 404 error. | PASS |
| Missing run / reinterpretation | API returns a clear not-found response. | PASS |
| Delete active mission | API returns 409 with allowed terminal states; UI shows feedback. | PASS |
| Invalid Library selection payload | API returns 400. | PASS |
| Hero asset missing, wrong character or hidden | API returns 404/409 with a specific reason. | PASS |
| Invalid target character for reinterpretation | API returns 400/409 without queuing work. | PASS |

## Not destructively injected

ComfyUI offline, LM Studio offline, missing model, missing production workflow, active VRAM contention, filesystem write denial, render timeout, invalid image and truncated live Visual Review were not forced against the owner's active environment. Existing tests cover several boundaries, but live UI evidence is still required.

Known UX weakness: background hard reevaluation logs per-asset exceptions to the server and returns the number successfully evaluated; the response does not provide a per-asset failure summary to the UI. This requires a small API/UX design pass after the freeze.
