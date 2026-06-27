# Conventions

## Naming

- Use short, descriptive task slugs in branch names.
- Prefer `feature/phase{N}-{M}-{slug}` for plan-driven work and `feature/issue-{N}-{slug}` for direct issue work.

## Code Style

- Keep project documents short, concrete, and written for new contributors and coding agents.
- Keep plans, implementation, verification, and project docs consistent with each other when a workflow changes.

## Review Expectations

- When a user asks to implement from an approved plan without naming a phase or step range, pick exactly one reviewable chunk:
  - find the next incomplete phase in `Progress`
  - weigh steps by complexity, touched files, and verification cost
  - group only the work needed for one self-contained chunk
- Stop for clarification only when the selected step must be split again because it grew beyond one reviewable chunk, or when the chunk depends on an unmet external prerequisite.
- Treat one request as one chunk, one branch, and one PR unless the user explicitly asks for a different grouping.
- Update `Progress` with `[ ]` before work starts, `[~]` while the selected chunk is in progress, and `[x]` only after verification passes.

## PR Handling

- After opening a PR, use `gh` for GitHub operations and wait for configured bot feedback before deciding whether more changes are needed.
- If a bot asks for another review pass, reply with the required mention and wait for the follow-up response before merging.
- Keep any repository-specific bot list under the PR handling section and include only bots that are materially active in the current workflow, with what they do and how to mention them.
- At a major stopping point, such as finishing all planned work on a branch, tell the user to clear context before the next large task.

## Fix and Verification Integrity

- Reproduce and investigate a warning, error, or failing check before changing code or tool configuration.
- Fix the underlying cause, then rerun the original failing check and the relevant verification suite.
- Do not disable checks, add broad ignores, lower severity, comment out tests, weaken assertions, or alter expected output solely to obtain a passing result.
- Allow a suppression only when evidence confirms a false positive, upstream tool defect, unavoidable compatibility constraint, or explicitly accepted risk and no practical direct fix is available.
- Keep an allowed exception to the smallest practical scope, explain the reason next to it, preserve relevant coverage, and record a removal condition or tracked follow-up when temporary.
- Require recorded user or maintainer approval before accepting a material unresolved risk.
- Report any warning, failure, or uncertainty that remains after verification.

## Forbidden Patterns

- Do not implement multiple chunks on the same branch by default.
- Do not skip the `[~]` state when work has started but is not yet complete.
- Do not merge immediately after opening a PR without checking for bot feedback.
- Do not list inactive or irrelevant bots in PR handling guidance.
- Do not use web UI steps when the same GitHub operation can be done with `gh`.
