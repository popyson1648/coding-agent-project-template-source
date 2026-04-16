# Plan

## Goal

Make `coding-agent-project-template-source` the source of truth for a public template repository whose published contents come only from `coding-agent-project-template/`.

## Scope

- Add a public-template subtree at `coding-agent-project-template/`.
- Add a source-side GitHub Actions workflow that syncs that subtree into `popyson1648/coding-agent-project-template`.
- Document the publishing model and required GitHub App configuration in the source repository only.
- Update verification so the source repository checks the new layout and publishing workflow.

## Non-goals

- Directly maintain the public repository by hand.
- Add management files to the published template repository.
- Support PAT-based publishing.

## Assumptions

- `main` is the only branch that should publish.
- Publishing uses a GitHub App installation token with write access to the public template repository.
- The public repository accepts force-free fast-forward pushes from the workflow's commits on its default branch.

## Steps

1. Create `coding-agent-project-template/` and populate it with the finished template contents only.
2. Record the source-of-truth and publishing decision in `.decisions/`.
3. Add a workflow in the source repository that checks out both repositories, mirrors only `coding-agent-project-template/`, and commits only when changes exist.
4. Update source-side docs to explain the structure, sync flow, and required secrets.
5. Update verification so the source repo validates the new subtree and publish workflow.
6. Run verification and inspect the final diff.

## Verification

- Run `python3 scripts/verify.py --mode all`.
- Check the publish workflow YAML for the expected two-repository sync flow.
- Review the new subtree to confirm only user-facing template files are included.

## Open Issues

- The GitHub App must be installed on both repositories and expose its credentials through source-repo secrets.
