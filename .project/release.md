# Release

## When Release Is Needed

Run a release whenever `coding-agent-project-template/` changes and the public template repository should reflect that change set.

## Release Steps

1. Merge the source change into `main` in `coding-agent-project-template-source`.
2. Let `.github/workflows/publish-template.yml` mirror `coding-agent-project-template/` into `popyson1648/coding-agent-project-template`.
3. Confirm that the workflow either pushed a commit to the public repository or reported that no sync was needed.

When content changed, the workflow also stamps `.template-version` (source commit, publish date, and
release tag) into the public repository and cuts a `vYYYY.MM.DD` GitHub Release there with
auto-generated notes (`gh release create --generate-notes`, same-day republishes get a `.2`, `.3`,
... suffix). The file and the release exist only in the public repository, never in the source
subtree.

## Required Checks

- `python3 scripts/verify.py`
- Successful `Publish Public Template` workflow run on the source repository

## Required GitHub Configuration

- Source repository Actions variable: `APP_ID` with the GitHub App numeric app ID
- Source repository secret: `APP_PRIVATE_KEY`
- GitHub App installation target: `popyson1648/coding-agent-project-template`
- GitHub App repository permission: `Contents: Read and write`

## Rollback Or Recovery Notes

- Revert the source commit on `main` and let the publish workflow run again.
- Do not patch the public repository directly; it is treated as generated output.
