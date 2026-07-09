# Plan

## Status

done

## Date

2026-07-07

## Issues

Issue `#38`

## Goal

Give projects that already adopted the template a standard way to follow template updates, with a
version identity for the template (issue `#38`).

## Scope

- Stamp `.template-version` (source commit and publish date) into the public repository from the
  publish workflow, only when synced content actually changed, excluding the stamp from the
  delete-aware rsync so unchanged publishes stay no-ops.
- Extend the publish-workflow contract check in `scripts/verify.py` with the stamp requirements.
- Document the update procedure in the published template `README.md`:
  - primary path: template as a git remote, first sync with `--allow-unrelated-histories`, later
    syncs as ordinary three-way merges; no squash; `python3 scripts/verify.py` as the acceptance check
  - alternative path without a remote: locate the base publish commit via `.template-version`,
    apply the template diff with `git apply --reject`, resolve `.rej` files by hand
- Note the stamp in the source `.project/release.md` publish flow.
- Record the tool evaluation (Copier, cruft, actions-template-sync, pure git) and the decision in
  `.decisions/`.

## Non-goals

- Converting the template to a templating engine (Copier/cruft model); excluded by the issue.
- Shipping scheduled sync automation (actions-template-sync) as a default; it needs per-project
  tokens and is mentioned as opt-in only.
- Migrating existing adopters in bulk.

## Assumptions

- Update models of Copier, cruft, actions-template-sync, and the community git-merge pattern per
  `.tmp/web-research/template-update-sync.md`.
- Publish commits already carry the source SHA in their message
  (`Publish template from source <sha>`), which the no-remote path uses to find the base commit.

## Steps

1. Update `publish-template.yml` (rsync exclude + conditional stamp write).
2. Update the publish-workflow required snippets in source `scripts/verify.py`.
3. Add the update section to the template `README.md`; note the stamp in `.project/release.md`.
4. Add the decision record.
5. Verify: `python3 scripts/verify.py`; simulate both update paths against scratch git repositories.

## Progress

- [x] Step 1: publish workflow
- [x] Step 2: contract check
- [x] Step 3: documentation
- [x] Step 4: decision record
- [x] Step 5: verification

## Verification

- `python3 scripts/verify.py`
- Scratch-repo simulation: stamp written only on content changes; remote-merge path preserves local
  customization and merges template changes; `git apply --reject` path applies the diff and updates
  the stamp.

## Open Issues

- None.
