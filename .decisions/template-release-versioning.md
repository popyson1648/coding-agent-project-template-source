# Decision

## Title

Cut a CalVer GitHub Release on the public template for every content-changing publish

## Date

2026-07-07

## Status

Accepted

## Decision

The publish workflow, after pushing synced content to the public template repository, creates a
GitHub Release there tagged `vYYYY.MM.DD` (UTC, from the same publish event that already stamps
`.template-version`). Same-day republishes get a `.2`, `.3`, ... suffix, checked by probing
`gh release view` before creating. Release notes are generated with `gh release create
--generate-notes`; no hand-written changelog file. The resolved tag is also written into
`.template-version` as a `release:` line, so the machine-readable stamp and the human-visible
release always agree. The public template's README links the release badge and Releases page as the
human-readable way to check version, alongside the existing `.template-version` file.

## Context

Users asked to see the template's version by looking at the repository, ideally through real GitHub
Releases. `.decisions/template-update-mechanism.md` (issue #38) already stamps `.template-version`
but is not human-visible without opening a file, and that decision explicitly found the template has
no compatibility contract, so SemVer would assert a guarantee that does not exist. No `LICENSE` file
exists in the public repository (confirmed via `gh repo view`), so a license badge was not added;
the user chose to skip it rather than add a license now.

## Alternatives

- SemVer tags. Rejected: reopens the compatibility-contract question `template-update-mechanism.md`
  already closed; nothing in this template distinguishes a "breaking" change from any other.
- A hand-maintained `CHANGELOG.md`. Rejected: `--generate-notes` already produces PR/commit-based
  notes from GitHub's own data with no file to keep in sync.
- release-please or semantic-release. Rejected: both are built around conventional commits driving
  SemVer bumps, which begs the same question as plain SemVer tags; unnecessary tooling for a
  date-based scheme.
- Release only on a manual trigger. Rejected: would need a second, separately-remembered step;
  tying it to the existing "content changed" gate keeps one publish event fully self-describing.

## Reason

CalVer states only when a version shipped, matching the earlier finding that this template makes no
compatibility promises. Reusing the publish workflow's existing change-detection gate and GitHub's
own release-notes generation keeps the mechanism to a few workflow lines with nothing new to
maintain. The GitHub REST API's "Create a release" endpoint is covered by the `Contents: write`
permission the workflow's GitHub App token already holds, so no new permission was requested.

## Consequences

- `publish-template.yml` gains a tag-computation/de-dup step and a `Create GitHub Release` step.
- `.template-version` gains a third `release:` line.
- `check_publish_workflow` in source `scripts/verify.py` asserts the new snippets are present.
- The public README's release badge shows "no releases found" until the first release lands after
  this change reaches `main`.

## Revisit Conditions

- The template adopts a compatibility contract or migration notes, at which point SemVer becomes
  meaningful and this decision should be revisited.

## Related

- Issues: none (not filed as an issue; direct user request)
- Decisions: template-update-mechanism.md
