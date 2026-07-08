# Plan

## Status

done

## Date

2026-07-08

## Issues

#42, #43, #44, #45, #46, #47, #48, #49, #50, #51, #52, #53, #54, #55

## Goal

Resolve the current open maintenance issues for the source repository and public template, then open
a reviewable pull request into `dev`.

## Scope

- Harden GitHub Actions references and permissions.
- Add Dependabot configuration for GitHub Actions.
- Add MPL-2.0 licensing, a baseline `.gitignore`, and README requirement clarifications to the
  public template.
- Update source-side README, project documentation, release recovery notes, and stale plan status.
- Add unit tests and stronger `scripts/verify.py` checks for shared agent rules and template sync.

## Non-goals

- Merging the pull request.
- Changing the publish authentication model.
- Introducing a template generation engine.
- Adding auto-merge or non-GitHub-Actions Dependabot ecosystems.

## Assumptions

- The license choice is MPL-2.0, as specified by the maintainer.
- The PR target branch is `dev`.
- Existing public template users can receive these changes through the existing publish flow after
  this source change is merged.

## Steps

1. Confirm upstream MPL-2.0 text and current GitHub Action tag commit SHAs.
2. Implement workflow hardening, Dependabot, template files, documentation, and release recovery.
3. Add unit tests and verification coverage for verify.py behavior and repository invariants.
4. Run verification, pre-commit, and targeted tests.
5. Commit, push, and open a draft PR into `dev`.

## Progress

- [x] Step 1: confirm upstream MPL-2.0 text and current GitHub Action tag commit SHAs
- [x] Step 2: implement workflow hardening, Dependabot, template files, documentation, and release recovery
- [x] Step 3: add unit tests and verification coverage
- [x] Step 4: run verification, pre-commit, and targeted tests
- [x] Step 5: commit, push, and open a draft PR into `dev`

## Verification

- `python3 scripts/verify.py`
- `python3 scripts/verify.py --check source-layout --check public-template --check publish-workflow --check github-actions --check python-syntax --check agent-rule-sync --check template-sync`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`
- `pre-commit run --all-files`

## Open Issues

None.
