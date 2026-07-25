# Decision

## Title

Call plain `python3 scripts/verify.py` from pre-commit and CI

## Date

2026-07-07

## Status

superseded

## Decision

This record is superseded by `.decisions/impact-based-verification-selection.md`. The successor
carries forward plain full verification for pre-commit and manual use while replacing the CI
invocation.

The historical decision was that `.pre-commit-config.yaml` and `.github/workflows/ci.yml` invoke
`python3 scripts/verify.py` with no `--mode` flag, in both the source repository and the published
template.

The `--mode` option stays in `verify.py` as an optional phase filter (`run_pre_commit`, `run_in_ci`,
and related flags in `verification.toml`) for projects that later need to split CI-only or
pre-commit-only phase sets.

This supersedes the incidental `--mode ci` invocation detail recorded in
`.decisions/ci-default-verification.md`; that decision's core (phases ship disabled) is unchanged.

## Context

Issue `#15`: the pre-commit framework decides when pre-commit hooks fire, and GitHub Actions decides
when CI fires. `--mode pre-commit` and `--mode ci` are not trigger mechanisms and do not simulate
those environments; they only filter which phases run. While no phase declares per-mode flags, the
modes select exactly the same phases as the default, so the flags added a misleading suggestion that
the invocation controlled triggering.

## Alternatives

- Keep `--mode ci` / `--mode pre-commit` in the wiring. Rejected: implies trigger semantics that the
  flag does not have, which is the confusion issue `#15` documents.
- Remove the `--mode` feature entirely. Rejected: the phase-filter capability is cheap to keep and
  becomes useful the first time a project needs CI-only verification phases.

## Reason

One documented invocation (`python3 scripts/verify.py`) is what `AGENTS.md` already instructs, keeps
local, pre-commit, and CI runs identical, and leaves trigger ownership where it belongs: the
pre-commit framework and GitHub Actions.

## Consequences

- Pre-commit, CI, and manual runs execute the same phase set.
- Projects that need split phase sets opt in by setting `run_in_ci` / `run_pre_commit` flags in
  `verification.toml` and adding `--mode` back to the specific caller.

## Revisit Conditions

- A project or this repository actually needs different phase sets per environment.
- `verify.py` gains a different mechanism for environment-specific phase selection.

## Related

- [Issue #15](https://github.com/popyson1648/coding-agent-project-template-source/issues/15)
- [Issue #69](https://github.com/popyson1648/coding-agent-project-template-source/issues/69)
- [CI default verification](ci-default-verification.md)
- [Impact-based verification selection](impact-based-verification-selection.md)
