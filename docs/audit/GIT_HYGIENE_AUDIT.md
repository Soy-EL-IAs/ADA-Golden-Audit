# ADA 1.0 Alpha Git hygiene audit

## Recovery checkpoint

- Current branch: `master`.
- Pre-audit committed ancestor: `3585055e39b2d4c8bcb08a004eb17704cb46c7a6`.
- Recovery branch created: `pre-ada-1.0-alpha-audit`.
- Important boundary: that branch preserves the committed ancestor only; it does not pretend to capture the large uncommitted owner worktree.

## Worktree

At audit start, porcelain status contained 3,376 entries: 3,314 untracked, 58 modified and 4 deleted. After adding a conservative `.gitignore`, status contains 187 entries: 125 untracked, 58 modified and 4 deleted.

No tracked or untracked source/data was reset, checked out, stashed, moved or physically deleted. The four deletions and most source modifications predate this audit and remain untouched as owner work.

## Ignore policy added

- Python/editor caches and machine-local config.
- Runtime `data/`, generated run trees, temporary test sandboxes and logs.
- Bulk experiment/render outputs and failed reference cache.
- Generated workflow exports, while keeping curated `workflows/legacy/` trackable.

Release documentation, source, schemas, production workflows, curated character references and `audit_evidence/` remain trackable.

## Open hygiene work

- Several bytecode files are already tracked and modified; a later reviewed commit should remove them from the Git index without deleting local source.
- Root maintenance/debug scripts require the dead-code decision before move/delete.
- No dependency manifest/lockfile exists.
- A release baseline cannot be honestly created until the mixed source state is reviewed and all intended files are staged together.

Status: `FAIL` for clean-release criteria. No `ADA-1.0-alpha` tag exists or was created.
