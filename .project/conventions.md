# Conventions

## Naming

- Use issue- or phase-based branch names and keep one branch focused on one chunk of work.
- Prefer `feature/phase{N}-{M}-{slug}` for plan-driven work and `feature/issue-{N}-{slug}` for direct issue work.

## Durable Implementation

- Make each change complete, maintainable, appropriately tested, and consistent with the codebase for its current known requirements.
- Do not knowingly ship an avoidable deficiency on the assumption that it will be repaired later.
- Use clear names, cohesive responsibilities, explicit interfaces, and existing project patterns.
- Choose the simplest design that satisfies current requirements; do not add abstractions, extension points, or functionality for hypothetical future needs.
- Document material tradeoffs. If a constraint makes debt unavoidable, record its reason, scope, impact, and follow-up or revisit condition in a tracked task or decision.
- Treat refactoring required by genuinely new requirements as normal evolution, not proof that the earlier implementation failed this standard.

## Test Timing

- Write or update tests in the same chunk as the change they cover; a change that needs tests is not complete, and is not merged, without them.
- Choose the technique per task instead of fixing one methodology:
  - test-first (TDD) fits when the expected inputs and outputs are clear up front; state that intent explicitly so implementation is not faked against unwritten tests
  - writing tests alongside or immediately after the code fits when the design is still being discovered
- Start a bug fix with a failing test that reproduces the bug whenever the test harness can express it, and keep that test after the fix.
- Deferring tests to a later chunk requires the same recorded approval as any other known deficiency under Durable Implementation.

## Code Style

- Keep source-side operational docs aligned with the published template rules where the same workflow applies.
- Write contributor guidance as explicit rules, not as implied team knowledge.

## Evidence and Research

- Inspect the repository and current environment before relying on external assumptions.
- Before a material proposal, decision, or implementation depends on an uncertain, externally defined, or version-dependent fact, search the web and verify it.
- Prefer current official documentation, specifications, standards, upstream source, and upstream release notes. Use secondary sources only when primary evidence is unavailable, and state that limitation.
- Increase the depth and independence of corroboration with the impact and uncertainty of the decision.
- Cite the evidence used and separate verified facts from inferences, proposals, and unresolved uncertainty.
- Do not put secrets, credentials, private source, or other sensitive data in search queries.
- Web research is optional for stable self-evident facts and facts established directly from the local repository or environment.

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
- Do not list inactive, unused, or non-review automation as PR bots.
- Do not rely on manual browser actions for routine GitHub tasks that `gh` can perform.
