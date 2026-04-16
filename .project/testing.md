# Testing

## Test Types

- Source-layout verification
- Publish-workflow contract verification
- Public-template subtree verification
- Python syntax compilation for both verification scripts

## Minimum Checks Before Completion

- Run `python3 scripts/verify.py --mode all`.

## Checks By Change Type

- Template subtree changes: run `python3 scripts/verify.py --check public-template`.
- Publish workflow or source-layout changes: run `python3 scripts/verify.py --mode all`.

## How To Run Verification

- `python3 scripts/verify.py --mode all`
- `python3 scripts/verify.py --check source-layout --check public-template --check publish-workflow`
