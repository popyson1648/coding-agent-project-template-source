# Plan

## Status

in-progress

## Date

2026-07-14

## Issues

- Follow-up to PR #64 and `.plans/pr-dependabot-actions-updates.md`.

## Goal

Replace Dependabot with Renovate on the source repository so that GitHub Actions pin updates cover
all five workflow/scaffold copies in one PR, while template-created projects keep their zero-setup
Dependabot configuration.

## Scope

- Add `renovate.json` covering the default workflow locations plus `.template/ci.yml` copies,
  grouped into one weekly PR, with digest pinning kept.
- Remove `.github/dependabot.yml` from the source root only; the template subtree keeps its copy.
- Update `scripts/verify.py` required paths accordingly.
- Record the decision and supersede `.decisions/github-actions-dependabot.md` for the source side.

## Non-goals

- Do not change the updater shipped to template-created projects.
- Do not self-host Renovate.
- Do not loosen full-SHA pinning.

## Assumptions

- The user installs the Mend Renovate App on the source repository (manual browser step).
- The user disables Dependabot version updates in the mirror repository settings (manual step);
  the shipped `dependabot.yml` file itself stays unchanged.

## Steps

1. Add `renovate.json` at the source root.
2. Remove source-root `.github/dependabot.yml` and update `SOURCE_REQUIRED_PATHS`.
3. Write the decision record and supersede the Dependabot decision.
4. Run `python3 scripts/verify.py` and validate the Renovate config.
5. Open the PR, get it merged, then have the user install the Renovate app.

## Progress

- [x] Step 1: `renovate.json` added.
- [x] Step 2: source-root `dependabot.yml` removed; `scripts/verify.py` updated.
- [x] Step 3: decision records updated.
- [x] Step 4: `python3 scripts/verify.py` passed; `renovate-config-validator` (renovate 43.262.1)
  validated the config.
- [ ] Step 5: PR, merge, app installation.

## Verification

- `python3 scripts/verify.py`
- `npx --yes --package renovate renovate-config-validator` (best effort; Renovate also reports
  config errors on its first run)

## Open Issues

- Manual steps after merge: install the Mend Renovate App on the source repository; turn off
  Dependabot version updates in the mirror repository settings.
