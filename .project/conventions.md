# Conventions

## Naming

- Use issue- or phase-based branch names and keep one branch focused on one chunk of work.
- Prefer `feature/phase{N}-{M}-{slug}` for plan-driven work and `feature/issue-{N}-{slug}` for direct issue work.

## Code Style

- Keep source-side operational docs aligned with the published template rules where the same workflow applies.
- Write contributor guidance as explicit rules, not as implied team knowledge.

## Review Expectations

- If implementation starts from an approved plan without a user-selected phase or step range, select exactly one reviewable chunk:
  - find the next incomplete phase in `Progress`
  - weigh candidate steps by complexity, touched files, and verification cost
  - stop grouping once the chunk is self-contained and reviewable
- Stop for clarification only when the selected step must be split again because it grew beyond one reviewable chunk, or when the chunk depends on an unmet external prerequisite.
- Treat one user implementation request as one chunk, one branch, and one PR unless the user explicitly requests another split.
- Update `Progress` with `[ ]` before work starts, `[~]` while the selected chunk is in progress, and `[x]` only after verification passes.

## PR Handling

- Open the PR with `gh` and use `gh` for follow-up GitHub operations.
- After opening a PR, wait for bot feedback before deciding whether the branch is ready to merge.
- If a bot comment requires action, make the change, reply with a mention when the bot expects one, and wait for the next response before merging.
- If a bot comment does not require action, record that judgment in the PR conversation or review summary and continue toward merge.
- Keep the bot list in this section limited to bots that are materially active in this repository's PR workflow.

### Active PR Bots

- No materially active PR review bot is currently verified in this repository.
- Do not list `github-actions[bot]` here unless it starts participating in PR review flow; it currently runs repository automation rather than review conversation.
- When a real PR bot is introduced, list:
  - bot name
  - what it does in PR handling
  - how to mention or re-request it

## Context Management

- When a branch reaches a major stopping point, such as finishing its goal and verification, tell the user to clear context before the next large task.

## Forbidden Patterns

- Do not implement multiple chunks on the same branch by default.
- Do not skip the `[~]` state when work has started but is not yet complete.
- Do not merge immediately after opening a PR without checking for bot feedback.
- Do not list inactive, unused, or non-review automation as PR bots.
- Do not rely on manual browser actions for routine GitHub tasks that `gh` can perform.
