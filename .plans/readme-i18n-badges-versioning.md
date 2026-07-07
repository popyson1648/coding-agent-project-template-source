# Plan

## Status

done

## Date

2026-07-07

## Issues

None

## Goal

Add a Japanese README, badges where they can legitimately be shown, and CalVer GitHub Releases so
users can see the public template's version.

## Scope

- `coding-agent-project-template/README.ja.md`: full Japanese translation of `README.md`.
- Language-switcher line and CI + latest-release badges in both README files.
- `.github/workflows/publish-template.yml`: cut a `vYYYY.MM.DD` GitHub Release (with same-day
  de-dup) on the public repository whenever a publish changes synced content; add the resolved tag
  to the `.template-version` stamp.
- `scripts/verify.py` (source): require `README.ja.md` in the public template contract, and extend
  the publish-workflow contract check for the new release-creation snippets.
- `.project/release.md`: note the new release step.
- `.decisions/template-release-versioning.md`, linked both ways with
  `.decisions/template-update-mechanism.md`.

## Non-goals

- A license badge (no `LICENSE` file exists; user confirmed to skip it rather than add one now).
- SemVer or a compatibility contract (CalVer only, consistent with the earlier no-SemVer decision).
- A hand-maintained changelog file (`--generate-notes` covers it).
- Translating any other document beyond the public template's own README.

## Assumptions

- Badge URL formats and CalVer rationale per `.tmp/web-research/readme-i18n-badges-versioning.md`.
- "Create a release" is covered by the GitHub App's existing `contents: write` permission (verified
  against GitHub REST API docs during planning); no workflow permission change needed.
- `gh` CLI is preinstalled on `ubuntu-latest` GitHub-hosted runners.

## Steps

1. Write `coding-agent-project-template/README.ja.md`; add switcher + badges to both README files.
2. Add `README.ja.md` to `PUBLIC_TEMPLATE_REQUIRED_PATHS` in source `scripts/verify.py`.
3. Extend `publish-template.yml` with tag computation, de-dup loop, `gh release create
   --generate-notes`, and the `release:` line in `.template-version`.
4. Extend `check_publish_workflow` required snippets in source `scripts/verify.py`.
5. Update `.project/release.md`; add the new decision record and its `Related` link back into
   `.decisions/template-update-mechanism.md`.
6. Verify: `python3 scripts/verify.py`; dry-run the tag de-dup shell logic locally.

## Progress

- [x] Step 1: README files
- [x] Step 2: contract path
- [x] Step 3: publish workflow
- [x] Step 4: contract snippets
- [x] Step 5: docs and decision
- [x] Step 6: verification

## Verification

- `python3 scripts/verify.py`
- Local dry run of the tag de-dup loop logic
- Manual read-through of both README files for working relative links

## Open Issues

- The release badge and actual release creation can only be observed after this reaches `main`
  (publish only runs on push to `main`); not verifiable end-to-end from this branch.
