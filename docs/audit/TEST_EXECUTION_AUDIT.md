# ADA 1.0 Alpha test execution audit

Captured 2026-08-25. No test files or dependencies were added during this pass.

## Existing unittest suite

Command scope: 14 existing modules covering production workflow isolation, VRAM/resource handoff, grounded review, run state, mission deletion, character catalog/onboarding/profile safety, Stock mode, tag resolution, Klein prompt compilation, mission character versions and split orchestration.

Result after rerunning outside the restricted Windows sandbox:

- 58 tests executed.
- 56 passed.
- 2 failed.
- 0 environmental permission errors remained.

The first sandboxed run also produced 13 `PermissionError` results while creating temporary folders. They were demonstrated to be environment-only because the same cases passed outside the sandbox.

## Open failures

`tests/test_klein_prompt_compiler.py` contains two exact-text assertions expecting standalone sentences such as `Preserve 2B's ...`. The current deterministic compiler includes the same identity traits inside its stricter source-preservation sentence. This is a contract/test mismatch, not evidence that identity tags are missing.

Disposition: open. Do not rewrite either the current compiler or the test expectation during a freeze while both files contain concurrent work. Decide and freeze the intended prompt contract first.

## Additional read-only/manual checks

- Three existing pytest-style Library visibility functions were invoked directly: 3 passed.
- Live API cross-check: collection totals summed to 89 and the visible Library endpoint returned 89 assets; zero visible assets carried rejected/hidden/soft-deleted/removed markers.
- A legacy path was substituted into the production renderer preset: the loader raised `ValueError` before loading/submitting it.
- `node --check` passed for `ada_app/static/app.js`.
- Python compilation passed for `ada_app/asset_library.py`, `ada_app/mission.py` and `scripts/production_workflows.py`.

## Not executed

- No Playwright package was installed and no repository Playwright suite was created.
- No destructive error injection, live VRAM unload, character deletion, dataset generation or Golden render was started.
- No large dataset was executed.

These omissions are represented as `NOT_IMPLEMENTED` or known issues in the certification matrix, never as passes.
