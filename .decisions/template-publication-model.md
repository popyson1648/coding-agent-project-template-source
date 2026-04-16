# Decision

## Title

Publish the public template repository from a managed subtree in the source repository

## Date

2026-04-16

## Status

Accepted

## Decision

`coding-agent-project-template-source` is the only repository that is edited directly.
The finished public template lives in the tracked directory `coding-agent-project-template/`.
GitHub Actions in the source repository mirrors only that directory into `popyson1648/coding-agent-project-template`.

## Context

The public repository must contain only end-user template files.
The source repository needs management files, plans, decisions, and publishing automation that must never leak into the public template repository.
The template subtree must stay a normal directory inside the source repository rather than a nested Git repository.

## Alternatives

- Maintain the public repository by hand.
- Use the source repository root as the published repository content.
- Use a nested Git repository or submodule for the public template.
- Publish with a fine-grained PAT.

## Reason

Keeping the public template in a normal subtree preserves a single source of truth while clearly separating management artifacts from published artifacts.
Mirroring only that subtree guarantees the public repository contains only finished template files and removes stale files with a delete-aware sync.
GitHub App authentication is preferred because it provides scoped, revocable repository access and avoids a user-bound long-lived PAT.

## Consequences

- Template changes must be made under `coding-agent-project-template/`.
- Source-side documentation must explain the sync flow and app-secret setup.
- Verification must validate both the subtree layout and the publish workflow contract.
- The publish workflow becomes the only supported write path into the public repository.

## Revisit Conditions

- The public repository needs multiple publish targets or branches.
- GitHub App authentication is no longer available.
- The template needs generated build artifacts before publication.
