# Structure

## Top-level Directories

- `coding-agent-project-template/`: the exact contents published to the public template repository.
- `.plans/`: task plans for maintaining the source repository.
- `.decisions/`: decisions about the source repo and publish model.
- `.project/`: source-side operating documentation.
- `.template/`: source repo document templates.
- `scripts/`: source-side verification tooling.

## Important Modules

- `scripts/verify.py`: verifies the source layout, publish workflow, template subtree, shared agent
  rule files, and template synchronization invariants; it also selects affected phases from the
  inputs declared in `.project/verification.toml`.
- `.project/verification.toml`: defines verification phases, named input scopes, input dependencies,
  and paths that conservatively force full verification.
- `.github/workflows/publish-template.yml`: serializes public template publishes, mirrors
  `coding-agent-project-template/` into the public repository, stamps `.template-version`, creates a
  dated GitHub Release, and verifies that release exists.

## Where To Make Changes

- Change end-user template files under `coding-agent-project-template/`.
- Change publish mechanics, verification, and operator documentation at the source repository root.
- Keep root `.template/` and `coding-agent-project-template/.template/` synchronized unless a
  documented exception exists.
- Keep public-template verification and CI defaults broad; source-only impact selection may be more
  granular because this repository owns its complete path and dependency map.

## Areas That Require Extra Care

- Never place source-management files inside `coding-agent-project-template/`.
- Never treat `coding-agent-project-template/` as a nested Git repository.
- Keep the publish workflow scoped to `coding-agent-project-template/` so the public repository never receives source-only files.
