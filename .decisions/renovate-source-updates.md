# Decision

## Title

Use Renovate for source repository GitHub Actions updates

## Date

2026-07-14

## Status

Accepted

## Decision

The source repository uses Renovate (hosted Mend Renovate App) instead of Dependabot for GitHub
Actions version updates. `renovate.json` extends the github-actions manager to also cover the
scaffold copies (`.template/ci.yml` in the source root and in the public template subtree), groups
all action updates into one weekly PR, and keeps digest pinning.

The public template keeps shipping `.github/dependabot.yml` so projects created from it get
zero-setup update PRs. Dependabot version updates are disabled in the mirror repository settings
because the mirror is generated output and direct patches get overwritten by the publish sync.

## Context

The pinned action SHAs exist in five files: two executable workflows plus three scaffold copies.
Dependabot only scans the repository-root `.github/workflows/` directory, so every update left the
scaffold copies stale and required manual sync. The same shipped `dependabot.yml` also activated on
the mirror repository, where its PRs were meaningless because the mirror is generated output.

## Alternatives

- Keep Dependabot and sync scaffold copies by hand: rejected because it is a recurring manual step
  that fails silently when forgotten.
- Keep Dependabot and add a CI equality check between the executable and scaffold `ci.yml`:
  rejected because every Dependabot PR would then fail CI until someone pushes a sync commit.
- Switch the template's shipped updater to Renovate too: rejected because Dependabot works in
  template-created projects with zero setup, while Renovate requires each user to install an app.
- Self-hosted Renovate on GitHub Actions: rejected for now to avoid maintaining a runner workflow
  and its credentials; revisit if handing the hosted app write access becomes unacceptable.

## Reason

Renovate's github-actions manager matches `.github/workflows/` at any depth by default and accepts
additional file patterns, so one PR updates all five files atomically and the template copies can
never drift from the executable workflows.

## Consequences

- `renovate.json` lives at the source repository root and is a required path in `scripts/verify.py`;
  `.github/dependabot.yml` is removed from the source root but stays in the template subtree.
- The Mend Renovate App must be installed on the source repository for updates to run.
- Renovate maintains a Dependency Dashboard issue in the source repository.
- Renovate PRs still require normal review and verification; full-SHA pinning stays enforced by the
  `github-actions` check.

## Revisit Conditions

- Dependabot gains support for scanning workflow files outside `.github/workflows/`.
- The hosted Renovate App's repository access becomes a concern; switch to self-hosted Renovate.
- The template adds ecosystems that Renovate and Dependabot handle differently.

## Related

- Supersedes `.decisions/github-actions-dependabot.md`
- `.decisions/github-actions-hardening.md`
- `.decisions/publish-workflow-contract-check.md`
- PR #64
