# Decision

## Title

Ship a dedicated `secrets` verification phase with gitleaks as the recommended scanner

## Date

2026-07-07

## Status

Accepted

## Decision

`verification.toml` ships a dedicated `[phases.secrets]` phase, ordered before all other phases in
`scripts/verify.py`. The phase starts disabled with a reason, matching the existing
first-CI-run-passes default. gitleaks is the recommended tool, documented in the shipped
`.project/testing.md`. Projects run the phase through `python3 scripts/verify.py`, which pre-commit
and CI both call, so no separate secrets wiring is needed. The template does not ship a
`.gitleaks.toml`; projects create one only when they need custom rules or allowlists.

## Context

Issue `#18` asks for a secrets-scan candidate in the verification workflow. gitleaks is MIT-licensed,
language- and framework-independent, and integrates with both pre-commit and CI. Research notes:
`.tmp/web-research/gitleaks.md`.

## Alternatives

- Fold secret scanning into the `lint` phase. Rejected: lint is about code quality; a leaked
  credential is a security event with different urgency and different suppression rules.
- Use the official gitleaks pre-commit hook plus `gitleaks/gitleaks-action` in CI. Rejected as the
  default: it wires the tool twice outside `verification.toml`, and `gitleaks-action` requires a
  license key for organization-owned repositories, while running the CLI through `verify.py` does not.
- Ship a `.gitleaks.toml` in the template. Rejected: the default rules are sensible and an empty
  config file invites drift.

## Reason

A dedicated phase keeps secret scanning visible in the standard phase list, runs it first so leaked
credentials fail fast, and reuses the single `verify.py` entry point for local, pre-commit, and CI
execution.

## Consequences

- Both `scripts/verify.py` copies list `secrets` first in `DEFAULT_ORDER`.
- All shipped `verification.toml` files contain a disabled `[phases.secrets]` with an enabling hint.
- The source repository keeps its own phase disabled until gitleaks is installed in its environment.

## Revisit Conditions

- gitleaks's successor project becomes the maintained standard.
- The template starts shipping a default toolchain that includes an installed secret scanner.
