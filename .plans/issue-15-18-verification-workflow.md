# Plan

## Status

done

## Date

2026-07-07

## Issues

#15, #18

## Goal

Align the pre-commit and CI wiring with the agreed verification workflow (issue #15) and add a
secrets-scanning phase with gitleaks as the recommended tool (issue #18).

## Scope

- Call plain `python3 scripts/verify.py` from `.pre-commit-config.yaml` and `.github/workflows/ci.yml`
  in both the source repository and the published template, keeping `--mode` available as an optional
  phase filter for projects that later need CI-only or pre-commit-only phase sets.
- Add a `secrets` phase to the verification phase order in both `scripts/verify.py` copies.
- Add a disabled `[phases.secrets]` entry with a gitleaks-oriented reason to every shipped
  `verification.toml`.
- Document secrets scanning setup (gitleaks install, pre-commit/CI placement, config files) briefly in
  the testing docs shipped with the template.
- Record both choices in `.decisions/`.

## Non-goals

- Removing the `--mode` feature from `verify.py`.
- Shipping a `.gitleaks.toml` in the template; projects create one only when they need custom rules.
- Enabling the secrets phase in this source repository (gitleaks is not installed here yet).

## Assumptions

- `verify.py` treats a disabled phase as skipped and an unknown phase name as appended after
  `DEFAULT_ORDER`, so adding `secrets` to `DEFAULT_ORDER` in both copies keeps ordering deterministic.
- gitleaks official pre-commit hook and `gitleaks git`/`gitleaks dir` commands per
  `.tmp/web-research/gitleaks.md`.

## Steps

1. Update pre-commit and CI files (source root, source `.template/`, template live and `.template/`
   copies) to run `python3 scripts/verify.py`.
2. Update source `.project/testing.md` and `.project/release.md` to the plain invocation.
3. Add `secrets` to `DEFAULT_ORDER` in `scripts/verify.py` and
   `coding-agent-project-template/scripts/verify.py`.
4. Add `[phases.secrets]` to the four `verification.toml` files.
5. Add a short "Secrets Scanning" section to the shipped testing docs.
6. Add decision records; run verification.

## Verification

- `python3 scripts/verify.py`
- `python3 scripts/verify.py --list` and `--mode pre-commit --list` still work.
- `python3 coding-agent-project-template/scripts/verify.py --config coding-agent-project-template/.project/verification.toml` reports no enabled phases (template default stays green).

## Open Issues

- None.
