# Decision

## Title

Follow template updates via git merges from the public repository, identified by a published version stamp

## Date

2026-07-07

## Status

Accepted

## Decision

The standard way for an adopted project to follow template updates is to add the public template
repository as a git remote and merge it: the first sync uses `--allow-unrelated-histories`, every
later sync is an ordinary three-way merge whose base git tracks itself. Template merges are never
squashed, and `python3 scripts/verify.py` is the acceptance check after conflict resolution.

The publish workflow stamps `.template-version` (source commit SHA and publish date) into the
public repository whenever synced content changed. The stamp is excluded from the delete-aware
rsync so unchanged publishes stay no-ops, lives only in the public repository, and is never edited
by hand. It gives every project — including snapshot adopters — a machine-readable template version
and enables a documented no-remote alternative: locate the base publish commit from the stamp,
apply the template's old-to-new diff with `git apply --reject`, and resolve `.rej` files manually.

## Context

Issue `#38`: neither adoption path (GitHub "Use this template", or the `#7` snapshot copy) had a
way to take in later template changes; `cp -n` cannot update existing files, and no version
identity existed. Publish commits already carry `Publish template from source <sha>`, which the
stamp keys into.

## Alternatives

- Copier or cruft. Rejected: both require converting the template into a templating-engine project
  (Jinja/cookiecutter) with its own release tagging — the parameterization issue `#38` explicitly
  excludes. Their core ideas are kept: recorded version identity (cruft's `.cruft.json` → the
  stamp) and old→new diff application instead of blind overwrite.
- actions-template-sync as the default. Rejected as default: needs a PAT or GitHub App plus a
  scheduled workflow in every adopting project; referenced in the README as an opt-in automation.
- Semantic versioning with git tags. Rejected for now: the template has no compatibility contract
  or migrations that semver would express; commit-based identity is automatic and sufficient.
- No version stamp (merge path only). Rejected: snapshot adopters would have no way to state which
  template they carry, and the no-remote diff path would be impossible.

## Reason

The merge path is the community-documented pattern for template repositories, uses git's own
three-way merge so project customizations survive and conflicts surface exactly where both sides
changed, works for both adoption paths, and requires zero new tooling. The stamp adds version
identity at the cost of two workflow lines.

## Consequences

- `publish-template.yml` writes the stamp conditionally; the publish-workflow contract check in
  `scripts/verify.py` enforces the rsync exclusion and the stamp write.
- The published `README.md` documents both update paths and the no-squash rule.
- Projects created from the public repository automatically carry `.template-version`.
- The source subtree intentionally has no `.template-version`; it exists only as publish output.

## Revisit Conditions

- The template gains breaking changes or migrations that need semantic versions and upgrade steps.
- Adopters ask for maintained update automation (revisit actions-template-sync or a dedicated tool).

## Related

- Issues: #38
- Decisions: template-adoption-path.md, template-publication-model.md
