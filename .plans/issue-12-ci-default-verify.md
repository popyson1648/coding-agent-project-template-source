# Plan

## Goal

Fix issue `#12` so a project generated from the template passes CI on its first push while still running `verify.py` by default.

## Scope

- Set the default verification phases to `enabled = false` with a `reason` in the shipped `verification.toml` files.
- Keep the CI workflow running `python3 scripts/verify.py --mode ci`.

## Non-goals

- Changing the source repository's own `.project/verification.toml`, which has real commands.
- Reworking `scripts/verify.py` behavior or the published template's source-specific checks.

## Assumptions

- An enabled phase with an empty command and no reason fails `verify.py` (exit 2); a disabled phase is skipped.

## Steps

1. Update `.template/verification.toml` so `format`, `lint`, `typecheck`, `build`, and `test_unit` are disabled with reasons, and add a header comment.
2. Mirror the same content into `coding-agent-project-template/.template/verification.toml` and `coding-agent-project-template/.project/verification.toml`.
3. Record the rationale in `.decisions/ci-default-verification.md`.

## Verification

- `cd coding-agent-project-template && python3 scripts/verify.py --mode ci` exits 0 with "no verification phases selected" (was exit 2).
- `python3 scripts/verify.py --mode all` passes at the source root.

## Open Issues

- The published template's `verify.py` still contains source-repository checks; out of scope for `#12`.
