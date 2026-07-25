# Testing

## Test Types

- Source-layout verification
- Publish-workflow contract verification
- GitHub Actions hardening verification
- Public-template subtree verification
- Shared agent-rule file synchronization
- Template scaffold synchronization
- Autonomous-loop policy and plan-state synchronization
- Python syntax compilation for both verification scripts
- Unit tests for shared `scripts/verify.py` behavior
- Impact-selection schema, path matching, dependency propagation, and fallback behavior

## Minimum Checks Before Completion

- Run `python3 scripts/verify.py`. With no event option, this is full verification.

## Checks By Change Type

- Template subtree changes: run `python3 scripts/verify.py --check public-template`.
- Loop-policy or plan-template changes: run
  `python3 scripts/verify.py --check agent-rule-sync --check template-sync --check loop-policy`.
- Publish workflow or source-layout changes: run `python3 scripts/verify.py`.
- Verification script changes: run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` and
  `python3 scripts/verify.py`.
- Input-scope changes: exercise a direct match, a dependency-propagated match, a known unrelated
  path, and an unknown path with repeated `--changed-file` arguments.

## How To Run Verification

- `python3 scripts/verify.py`
- `python3 scripts/verify.py --event full`
- `python3 scripts/verify.py --event changed --base <base-sha> --head <head-sha>`
- `python3 scripts/verify.py --event changed --changed-file <repository-relative-path>`
- `python3 scripts/verify.py --event scheduled --list`
- `python3 scripts/verify.py --event manual --list`
- `python3 scripts/verify.py --check source-layout --check public-template --check publish-workflow --check github-actions --check agent-rule-sync --check template-sync --check loop-policy`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`

## Impact Selection

- Schema version 2 declares path scopes under `[inputs.<name>]`; `depends_on` propagates a changed
  input to its transitive dependents.
- Each phase lists its input names and a `when` list. Use `always` alone, or combine `changed`,
  `scheduled`, and `manual`.
- `[selection].selector_paths` covers files that define selection, while `global_paths` covers
  shared files whose changes require every eligible phase.
- A named input referenced by no phase marks a known unrelated change; a path matching no input is
  unknown and forces full fallback.
- `--event changed` accepts an explicit Git base/head pair or repeated `--changed-file` values.
- Unknown paths, selector or global changes, and unavailable Git comparison data fall back to all
  eligible phases. The fallback is intentional: incomplete metadata must cost time, not coverage.
- `--event full` ignores impact policies but still honors `enabled`, `--mode`, and `--only`.
- CI keeps its workflow and job active and requests changed selection with the push or pull-request
  base/head SHAs. Pre-commit and plain manual invocation remain full verification.
