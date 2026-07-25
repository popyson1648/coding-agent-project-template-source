# Decision

## Title

Select verification phases from declared change impact with conservative full fallbacks

## Date

2026-07-25

## Status

Accepted

## Decision

Use verification schema version 2 to describe change impact independently of language, framework,
or build tool:

- `[inputs.<name>]` declares repository-relative path patterns and transitive `depends_on`
  relationships.
- Each phase declares input names and a `when` list. `always` is used alone; otherwise `changed`,
  `scheduled`, and `manual` can be combined.
- `[selection].selector_paths` identifies files that define selection behavior, while
  `global_paths` identifies shared files whose changes affect every eligible phase.

`--event changed` selects phases from directly matched inputs and their transitive dependents. It
accepts either an explicit Git base/head pair or repeated `--changed-file` values. Unknown paths,
selector or global changes, invalid changed-path metadata, and unavailable Git comparison data fall
back to all eligible phases.

A named input referenced by no phase explicitly marks a known unrelated change. This is distinct
from an unknown path, which always forces the conservative full fallback.

Plain `python3 scripts/verify.py` remains full verification. `--event full` expresses the same event
explicitly and ignores impact policies while still honoring `enabled`, `--mode`, and `--only`.

GitHub Actions keeps the CI workflow and verification job active for every configured push and pull
request. Checkout fetches complete history, and CI invokes `verify.py --mode ci --event changed`
with the event's base/head SHAs. Selection happens inside the job rather than through workflow path
filters.

The source repository uses granular named inputs because its complete layout is known. The
published template starts with a single `**` repository input, so every known change affects every
enabled phase until a project owner declares narrower scopes.

## Context

Issue `#69` asks for faster feedback by running only verification affected by a change without
coupling the template to a language-specific task runner.

Nx documents the established model: Git identifies changed files, a project graph identifies their
owners, and reverse dependencies expand the affected set. It also defaults dependency-file changes
to all projects as a fail-safe:

- https://nx.dev/docs/features/ci-features/affected

Git documents three-dot or merge-base comparison for branch changes. Its `--name-status -z` output
is machine-readable without ambiguous quoting, and `--no-renames` permits a move to be treated
conservatively as deletion plus addition:

- https://git-scm.com/docs/git-diff
- https://git-scm.com/docs/git-merge-base

The checkout action fetches only one commit by default and documents `fetch-depth: 0` for complete
history:

- https://github.com/actions/checkout

GitHub documents that a workflow skipped by path filtering can leave a required check pending and
block merging. Therefore the required workflow and job cannot be the unit of impact selection:

- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs

GitHub's event and webhook documentation identifies pull-request base/head revisions and the push
payload's `before` revision:

- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://docs.github.com/en/webhooks/webhook-events-and-payloads#push

## Alternatives

- Run every phase for every change. Rejected as the only mode because it preserves coverage but
  cannot improve feedback time as the phase set grows.
- Filter the GitHub Actions workflow or job by path. Rejected because a skipped required workflow
  can remain pending, and the workflow filter cannot express transitive input dependencies.
- Adopt Nx, Bazel, Gradle, or another build graph as a template dependency. Rejected because the
  public template is intentionally language- and framework-independent.
- Skip unknown paths. Rejected because an incomplete input map would silently omit verification.
- Infer dependencies from commands or language manifests. Rejected because inference is
  tool-specific and can miss non-code inputs such as generated config or policy files.

## Reason

Explicit named inputs make the selection contract reviewable and portable. Reverse dependency
closure captures indirect impact without turning the dependency graph into command ordering.
Conservative fallbacks ensure incomplete or unavailable evidence increases verification cost
instead of reducing coverage.

Keeping selection inside the always-run CI job preserves a stable required check while still
reducing executed work. A broad published default avoids assuming path ownership that only the
adopting project can define.

## Consequences

- Projects can shorten changed-event feedback after accurately describing path ownership and input
  dependencies.
- Projects must maintain input patterns when repository structure or dependency relationships
  change.
- Selector, global, unknown, or indeterminate changes intentionally lose the speed optimization and
  run every otherwise eligible phase.
- CI needs complete Git history and event-specific base/head SHAs.
- `scheduled` and `manual` are phase-selection policies; external workflow triggers remain separate.
- Pre-commit and plain manual invocation continue to run full verification.

## Revisit Conditions

- Selection metadata becomes difficult to keep correct as the repository grows.
- A language-independent standard emerges that can replace this schema without reducing
  conservative fallback coverage.
- CI can provide an authoritative changed-file set without full Git history.
- Required-check behavior changes so skipping the workflow is safe and observable.

## Related

- [Issue #69](https://github.com/popyson1648/coding-agent-project-template-source/issues/69)
- [Plain verify invocation](plain-verify-invocation.md)
- [CI default verification](ci-default-verification.md)
- [Evidence-based web research](evidence-based-web-research.md)
