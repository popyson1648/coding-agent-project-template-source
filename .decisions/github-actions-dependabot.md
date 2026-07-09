# Decision

## Title

Use weekly Dependabot version updates for GitHub Actions

## Date

2026-07-08

## Status

Accepted

## Decision

Both the source repository and the public template include `.github/dependabot.yml` for the
`github-actions` package ecosystem, scheduled weekly from the repository root.

## Context

The workflows use third-party GitHub Actions and pin them to full commit SHAs. Pinning reduces
mutable-tag risk, but it also creates an update process that needs automation.

Dependabot version updates for the `github-actions` ecosystem provide freshness PRs for workflow
action references. This is separate from Dependabot alerts and Dependabot security updates.

## Alternatives

- No Dependabot version updates: rejected because pinned action SHAs would become stale without a
  default update mechanism.
- Auto-merge Dependabot PRs: rejected for now because this repository has no accepted auto-merge
  policy.
- Other ecosystems: rejected because the repository has no npm, pip, or similar dependency manifest.

## Reason

Weekly checks are frequent enough for GitHub Action freshness without creating daily maintenance
noise. The public template receives the same default so projects created from the template start
with GitHub Actions update PRs enabled.

## Consequences

- Source and public template repositories contain `.github/dependabot.yml`.
- Dependabot PRs still require normal review and verification.
- SHA-pinned action references in scaffold files outside `.github/workflows/` may need manual sync
  when Dependabot updates the executable workflow copies.

## Revisit Conditions

- The project adopts auto-merge for Dependabot PRs.
- Other dependency manifests are added.
- Dependabot gains broader support for scaffolded workflow files outside `.github/workflows/`.

## Related

- Issue #44
