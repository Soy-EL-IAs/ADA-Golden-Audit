# Ada Viral Guide Evolution Summary

- Updated: 2026-08-22T11:31:53.653174+00:00
- Local LM Studio URL: `http://127.0.0.1:1234`
- Model: `qwen3.8-27b-uncensored`
- Runs recorded: 39
- Completed: 28
- Failed: 9
- OpenAI / Work / ComfyUI / Worker used: no

Best completed run by unweighted diagnostic mean: `run_027` (7.83/10).

## Runs

| Run | Status | Overall | Identity | Appeal | Diversity | Repetition | Micro-story | Animation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 001 | failed | — | — | — | — | — | — | — |
| 002 | failed | — | — | — | — | — | — | — |
| 003 | failed | — | — | — | — | — | — | — |
| 004 | failed | — | — | — | — | — | — | — |
| 005 | failed | — | — | — | — | — | — | — |
| 006 | failed | — | — | — | — | — | — | — |
| 007 | failed | — | — | — | — | — | — | — |
| 008 | failed | — | — | — | — | — | — | — |
| 009 | interrupted | — | — | — | — | — | — | — |
| 010 | completed | 6.83 | 8.50 | 7.00 | 6.00 | 5.50 | 6.50 | 7.50 |
| 011 | completed | 6.83 | 8.50 | 7.50 | 6.00 | 5.50 | 7.00 | 6.50 |
| 012 | completed | 7.68 | 9.20 | 8.40 | 7.50 | 6.50 | 7.20 | 7.30 |
| 013 | completed | 6.58 | 8.50 | 7.50 | 6.00 | 5.00 | 6.50 | 6.00 |
| 014 | completed | 6.93 | 8.20 | 7.60 | 6.50 | 5.80 | 6.40 | 7.10 |
| 015 | completed | 7.50 | 9.00 | 8.00 | 7.00 | 6.00 | 7.00 | 8.00 |
| 016 | completed | 7.48 | 8.50 | 8.20 | 7.00 | 6.50 | 7.50 | 7.20 |
| 017 | completed | 7.83 | 8.50 | 8.20 | 7.50 | 6.50 | 8.00 | 8.30 |
| 018 | completed | 7.33 | 9.00 | 8.00 | 7.00 | 6.00 | 7.00 | 7.00 |
| 019 | completed | 6.92 | 8.50 | 7.20 | 6.50 | 6.00 | 6.50 | 6.80 |
| 020 | completed | 7.00 | 9.00 | 8.00 | 6.00 | 5.00 | 7.00 | 7.00 |
| 021 | completed | 7.33 | 9.00 | 8.00 | 7.00 | 6.00 | 7.00 | 7.00 |
| 022 | completed | 7.00 | 9.00 | 8.00 | 6.00 | 5.00 | 7.00 | 7.00 |
| 023 | completed | 7.08 | 8.50 | 7.80 | 6.50 | 6.00 | 6.50 | 7.20 |
| 024 | failed | — | — | — | — | — | — | — |
| 025 | completed | 7.35 | 9.20 | 7.50 | 6.00 | 5.50 | 7.80 | 8.10 |
| 026 | completed | 7.00 | 9.00 | 8.00 | 6.00 | 5.00 | 7.00 | 7.00 |
| 027 | completed | 7.83 | 9.00 | 8.50 | 7.00 | 6.00 | 8.00 | 8.50 |
| 028 | completed | 7.05 | 9.50 | 7.20 | 6.50 | 5.80 | 6.80 | 6.50 |
| 029 | completed | 6.42 | 8.00 | 7.50 | 6.00 | 5.00 | 6.00 | 6.00 |
| 030 | completed | 7.00 | 8.50 | 7.50 | 6.00 | 5.50 | 7.00 | 7.50 |
| 031 | completed | 6.83 | 9.00 | 8.00 | 6.00 | 5.00 | 7.00 | 6.00 |
| 032 | completed | 7.17 | 9.00 | 8.00 | 6.00 | 5.00 | 7.00 | 8.00 |
| 033 | completed | 6.67 | 9.00 | 8.00 | 5.00 | 4.00 | 7.00 | 7.00 |
| 034 | completed | 6.08 | 9.00 | 7.50 | 4.00 | 3.00 | 6.50 | 6.50 |
| 035 | completed | 7.17 | 8.50 | 7.50 | 6.00 | 5.50 | 7.50 | 8.00 |
| 036 | completed | 7.50 | 9.00 | 8.00 | 7.00 | 6.00 | 7.00 | 8.00 |
| 037 | completed | 6.83 | 9.00 | 8.00 | 6.00 | 4.00 | 7.00 | 7.00 |
| 038 | completed | 7.75 | 9.50 | 8.00 | 7.50 | 6.50 | 7.50 | 7.50 |
| 039 | interrupted | — | — | — | — | — | — | — |

## Failures

- `run_001`: see `run_001/error.json`.
- `run_002`: see `run_002/error.json`.
- `run_003`: see `run_003/error.json`.
- `run_004`: see `run_004/error.json`.
- `run_005`: see `run_005/error.json`.
- `run_006`: see `run_006/error.json`.
- `run_007`: see `run_007/error.json`.
- `run_008`: see `run_008/error.json`.
- `run_024`: see `run_024/error.json`.

## Interpretation

Each completed cycle's `cycle_report.md` is the evidence supplied to the next cycle. Scores are local-model diagnostics, not ground truth; inspect the winning guide and premises before promoting anything to production.

No candidate is automatically copied into `config/prompt_guides`. Promotion remains a manual decision.
