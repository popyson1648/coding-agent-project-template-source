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

## Minimum Checks Before Completion

- Run `python3 scripts/verify.py`.

## Checks By Change Type

- Template subtree changes: run `python3 scripts/verify.py --check public-template`.
- Loop-policy or plan-template changes: run
  `python3 scripts/verify.py --check agent-rule-sync --check template-sync --check loop-policy`.
- Publish workflow or source-layout changes: run `python3 scripts/verify.py`.
- Verification script changes: run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` and
  `python3 scripts/verify.py`.

## How To Run Verification

- `python3 scripts/verify.py`
- `python3 scripts/verify.py --check source-layout --check public-template --check publish-workflow --check github-actions --check agent-rule-sync --check template-sync --check loop-policy`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`
