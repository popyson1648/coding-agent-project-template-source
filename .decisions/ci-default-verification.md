# Decision

## Title

Ship the template with verification phases disabled so the first CI run passes

## Date

2026-06-27

## Status

Accepted

## Decision

The default `verification.toml` shipped by the template starts every phase with `enabled = false` and a `reason`.
A project generated from the template runs `python3 scripts/verify.py --mode ci` in CI, selects no phases, and reports success.
Each phase is enabled and given a command when the matching tool is actually added.

## Context

The previous default enabled `format`, `lint`, `typecheck`, `build`, and `test_unit` with empty commands and no reason.
`scripts/verify.py` treats an enabled phase that has an empty command and no reason as a failure (exit 2).
Every project created from the template therefore failed CI on its first push before any tooling existed.

## Alternatives

- Keep the phases enabled with empty commands and a reason so `verify.py` skips them. Rejected: an enabled phase with no command is contradictory and misleading.
- Give each phase a placeholder command. Rejected: placeholder commands hide that no real check is configured.
- Remove the CI workflow from the template. Rejected: issue `#12` requires CI to run `verify.py` by default.

## Reason

Disabling phases with a reason matches the source repository's own pattern for not-yet-configured checks.
It keeps `verify.py` running in CI by default while letting a fresh project stay green until its owner configures real checks.

## Consequences

- `.template/verification.toml`, `coding-agent-project-template/.template/verification.toml`, and `coding-agent-project-template/.project/verification.toml` ship phases disabled with reasons.
- Project owners must enable a phase and set its command when they add the matching tool.
- The source repository's own `.project/verification.toml` keeps its real commands and is not affected.

## Revisit Conditions

- The template starts shipping a default toolchain that should run in CI out of the box.
- `verify.py` changes how it treats enabled phases with empty commands.
