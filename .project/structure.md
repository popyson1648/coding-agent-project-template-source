# Structure

## Top-level Directories

- `coding-agent-project-template/`: the exact contents published to the public template repository.
- `.plans/`: task plans for maintaining the source repository.
- `.decisions/`: decisions about the source repo and publish model.
- `.project/`: source-side operating documentation.
- `.template/`: source repo document templates.
- `scripts/`: source-side verification tooling.

## Important Modules

- `scripts/verify.py`: verifies the source layout, publish workflow, and template subtree.
- `.github/workflows/publish-template.yml`: mirrors the public template subtree into the public repository.

## Where To Make Changes

- Change end-user template files under `coding-agent-project-template/`.
- Change publish mechanics, verification, and operator documentation at the source repository root.

## Areas That Require Extra Care

- Never place source-management files inside `coding-agent-project-template/`.
- Never treat `coding-agent-project-template/` as a nested Git repository.
- Keep the publish workflow scoped to `coding-agent-project-template/` so the public repository never receives source-only files.
