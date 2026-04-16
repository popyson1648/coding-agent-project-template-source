# Plan

## Goal

Fix the failing `Publish Public Template` GitHub Actions workflow so the public template publish job can create an app token successfully.

## Scope

- Update the publish workflow input to match the current `actions/create-github-app-token@v2` contract.
- Update repository verification logic that validates the publish workflow.
- Update project documentation if it still describes the outdated variable or workflow contract.

## Non-goals

- Changing the publish repository target.
- Reworking the general CI workflow, which is already passing on the latest commit.
- Investigating third-party CI providers.

## Assumptions

- The GitHub Actions variable `APP_ID` stores the GitHub App numeric app ID.
- The failure is caused by the workflow using `client-id` where the action now requires `app-id`.

## Steps

1. Update `.github/workflows/publish-template.yml` to use the correct action input name.
2. Update `scripts/verify.py` so the `publish-workflow` check validates the corrected workflow contract.
3. Update any `.project/` documentation that still refers to the outdated workflow input semantics.
4. Run `python3 scripts/verify.py` and any targeted checks needed to confirm the fix.

## Verification

- `python3 scripts/verify.py`
- If needed, targeted verification for the publish workflow structure via `python3 scripts/verify.py --check publish-workflow`

## Open Issues

- If `APP_ID` is not the GitHub App numeric app ID, the workflow will still fail and the repository variable value will need to be corrected in GitHub settings.
