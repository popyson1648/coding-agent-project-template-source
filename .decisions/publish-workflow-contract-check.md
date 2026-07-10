# Decision

## Title

Check publish workflow actions by name, not by pinned SHA

## Date

2026-07-10

## Status

Accepted

## Decision

`check_publish_workflow` in source `scripts/verify.py` asserts that the publish workflow uses the
required actions by name (`actions/checkout`, `actions/create-github-app-token`) and keeps the
required behavior snippets. It no longer asserts specific commit SHAs.

The `github-actions` check remains the single place that enforces full 40-character SHA pins.

## Context

The publish-workflow check embedded the exact pinned SHAs of `actions/checkout` and
`actions/create-github-app-token`. Every Dependabot version update for those actions therefore
failed verification until the check was edited by hand, even though the update was correct and still
fully pinned.

## Alternatives

- Update the expected SHAs in the check on every Dependabot PR: rejected because it duplicates the
  pin in two places and makes every routine update a code change.
- Drop the publish-workflow check entirely: rejected because the workflow contract, such as the
  release steps and the template-version stamp, still needs verification.
- Allow unpinned action refs in the publish workflow: rejected because SHA pinning is a security
  requirement.

## Reason

Each check should own one concern. Action identity and publish behavior belong to the publish
workflow contract; pin freshness belongs to the pin check. Splitting them keeps the security
guarantee while letting Dependabot updates pass without source edits.

## Consequences

- Dependabot GitHub Actions updates pass verification when the new refs are full SHAs.
- Removing or renaming a required action in the publish workflow still fails verification.
- `scripts/verify.py` exposes `collect_action_names` and the publish-workflow contract constants.

## Revisit Conditions

- The publish workflow needs to require a minimum action version rather than only an action name.
- Dependabot PRs start to change publish workflow behavior instead of only action refs.

## Related

- PRs #60 and #62
- `.decisions/github-actions-hardening.md`
- `.decisions/github-actions-dependabot.md`
