# Decision

## Title

Pin GitHub Actions and grant read-only workflow tokens by default

## Date

2026-07-08

## Status

Accepted

## Decision

Source and public-template workflows pin third-party actions to full 40-character commit SHAs and
declare `permissions: contents: read` for CI-style workflows that only need repository checkout.

The publish workflow keeps repository-level `GITHUB_TOKEN` permissions read-only and uses a scoped
GitHub App installation token only for the public-template repository write operations.

## Context

GitHub's secure-use guidance says full-length commit SHA pinning is the immutable way to reference
third-party actions:

- https://docs.github.com/en/actions/reference/security/secure-use

GitHub's token guidance recommends granting only the minimum `GITHUB_TOKEN` permissions needed by a
workflow:

- https://docs.github.com/actions/reference/authentication-in-a-workflow

GitHub also documents policies that can require full-length SHA pinning for Actions:

- https://docs.github.com/en/rest/actions/permissions

## Alternatives

- Keep major-version action tags such as `actions/checkout@v4`: rejected because mutable tags are
  weaker supply-chain controls.
- Rely only on repository default token permissions: rejected because workflow-local permissions are
  explicit, reviewable, and portable across repositories.
- Give publish workflow write permissions through `GITHUB_TOKEN`: rejected because writes target the
  separate public template repository and should remain scoped to the GitHub App installation token.

## Reason

Full SHA pinning and least-privilege tokens are established GitHub Actions hardening practices. They
fit this repository because CI only needs read access, while publish requires a separate, narrower
write credential for one generated-output repository.

## Consequences

- Action references are less readable, so the matching major version is kept as an inline comment.
- Dependabot version updates are needed to keep pinned SHAs current.
- `scripts/verify.py` enforces full SHA pins and read-only workflow permissions.

## Revisit Conditions

- GitHub introduces immutable action releases that are easier to maintain than SHA pins.
- The workflow gains steps that need additional `GITHUB_TOKEN` permissions.

## Related

- Issues #42 and #43
- `.decisions/github-actions-dependabot.md`
