# Plan

## Status

in-progress

## Date

2026-07-09

## Issues

- PR #60: Bump `actions/create-github-app-token` from 2.2.2 to 3.2.0
- PR #62: Bump `actions/checkout` from 4.3.1 to 7.0.0
- Related passing PR: #61, bump `actions/setup-python` from 5.6.0 to 6.3.0

## Goal

Allow Dependabot GitHub Actions pin updates to pass repository verification while keeping the
security requirement that workflow actions are pinned to full commit SHAs.

## Scope

- Update the publish workflow verification so it checks required behavior and action names without
  requiring specific old commit SHAs.
- Keep the separate `github-actions` check responsible for enforcing full-SHA action pins.
- Add or update focused unit tests for the verification behavior.
- Keep source/template verification files synchronized where the repository requires it.
- Apply the action version bumps from PR #60, #61, and #62 directly, including the template
  `ci.yml` copies that Dependabot does not scan, so the Dependabot PRs auto-close as superseded.
- Migrate the publish workflow from the deprecated `app-id` input to `client-id`.

## Non-goals

- Do not merge Dependabot PRs automatically.
- Do not loosen the full-SHA pinning requirement.
- Do not change unrelated workflow behavior.

## Assumptions

- PR #60 and PR #62 fail because `check_publish_workflow()` requires exact old action SHAs.
- PR #61 already passes and should not need code changes.
- After this fix lands on `main`, the Dependabot PR checks should be rerun or rebased against the
  updated base branch.

## Steps

1. Replace exact old action-SHA snippets in the publish workflow check with structured validation
   that requires the expected action names and relies on the existing SHA-pin check for refs.
2. Add tests proving the publish workflow check accepts updated full-SHA pins and rejects missing
   required publish behavior.
3. Mirror required script/test/template changes into the public template subtree if verification
   reports sync mismatches.
4. Run `python3 scripts/verify.py`.
5. Recheck PR #60, #61, and #62 status and report remaining manual actions, such as rerunning CI or
   merging.

## Progress

- [x] Investigated current branch PR #63 and confirmed it is merged with no unresolved review
  threads.
- [x] Identified open PRs #60, #61, and #62.
- [x] Read failing CI logs for #60 and #62.
- [x] Step 1: Update publish workflow verification.
- [x] Step 2: Add focused tests.
- [x] Step 3: Keep generated/template copies synchronized (no change needed: the public template
  `scripts/verify.py` has no repository checks).
- [x] Step 4: Run repository verification.
- [x] Step 5 (revised): Superseded the Dependabot PRs by applying the bumps in this branch:
  `actions/checkout` v7.0.0, `actions/setup-python` v6.3.0, `actions/create-github-app-token`
  v3.2.0, across `.github/workflows/` and all template `ci.yml` copies.
- [x] Migrated `app-id` to `client-id` in the publish workflow. The action reads both inputs into
  the same parameter, so the existing numeric `APP_ID` variable keeps working unchanged.
- [~] Merge to `main`, then confirm Dependabot closes #60, #61, and #62 as no longer needed.

## Verification

- `python3 scripts/verify.py`
- If needed, targeted unit test run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`

## Open Issues

- Needs merge to `main` (user approval). After merge, confirm Dependabot closes #60, #61, and #62
  automatically; close them manually if it does not.
- Future Dependabot bumps to `ci.yml` still require the same manual sync of template copies; that
  trade-off stays recorded in `.decisions/github-actions-dependabot.md`.
