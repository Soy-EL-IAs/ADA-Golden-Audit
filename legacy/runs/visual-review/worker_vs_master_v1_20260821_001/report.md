# Worker 8B vs Master 27B

- Cases: 6
- Worker: `qwen/qwen3-vl-8b` — 2.37 s/image
- Master: `qwen3.8-27b-uncensored` — None s/image

| Case | Worker | Master |
|---|---|---|
| 2b_closeup_blindfold_ok | REJECT (id 8, an 7) | ERROR |
| 2b_blindfold_eye_visible | REJECT (id 10, an 9) | ERROR |
| 2b_duplicate_pair | REJECT (id 5, an 5) | ERROR |
| tifa_v26_closeup | REVIEW (id 9, an 8) | ERROR |
| tifa_v26_dynamic | REJECT (id 9, an 7) | ERROR |
| tifa_camera_and_back_drift | PASS (id 10, an 10) | ERROR |
