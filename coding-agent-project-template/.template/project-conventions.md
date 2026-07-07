# Conventions

## Naming

- Use short, descriptive task slugs in branch names.
- Prefer `feature/phase{N}-{M}-{slug}` for plan-driven work and `feature/issue-{N}-{slug}` for direct issue work.

## Durable Implementation

- Make each change complete, maintainable, appropriately tested, and consistent with the codebase for its current known requirements.
- Do not knowingly ship an avoidable deficiency on the assumption that it will be repaired later.
- Use clear names, cohesive responsibilities, explicit interfaces, and existing project patterns.
- Choose the simplest design that satisfies current requirements; do not add abstractions, extension points, or functionality for hypothetical future needs.
- Document material tradeoffs. If a constraint makes debt unavoidable, record its reason, scope, impact, and follow-up or revisit condition in a tracked task or decision.
- Treat refactoring required by genuinely new requirements as normal evolution, not proof that the earlier implementation failed this standard.

## Code Style

- Keep project documents short, concrete, and written for new contributors and coding agents.
- Keep plans, implementation, verification, and project docs consistent with each other when a workflow changes.

## Evidence and Research

- Inspect the repository and current environment before relying on external assumptions.
- Before a material proposal, decision, or implementation depends on an uncertain, externally defined, or version-dependent fact, search the web and verify it.
- Prefer current official documentation, specifications, standards, upstream source, and upstream release notes. Use secondary sources only when primary evidence is unavailable, and state that limitation.
- Increase the depth and independence of corroboration with the impact and uncertainty of the decision.
- Cite the evidence used and separate verified facts from inferences, proposals, and unresolved uncertainty.
- Do not put secrets, credentials, private source, or other sensitive data in search queries.
- Web research is optional for stable self-evident facts and facts established directly from the local repository or environment.

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

## Troubleshooting

- Start from the observed problem, not from a guessed cause: capture the exact error message, the expected behavior, the actual behavior, and the reproduction conditions.
- When the problem is actively disrupting users or work, stabilize first, then look for the cause.
- Consult sources in order of reliability: the exact error message and logs, official documentation, the upstream issue tracker and known bugs, release notes and changelogs, local configuration and version differences, and recent changes to the repository or environment.
- Form explicit hypotheses and test them one at a time against observations; prefer the simplest explanation that fits all the facts, and treat recent changes as prime suspects.
- Keep observed facts, tested results, and untested hypotheses separated. Investigation alone does not confirm a cause; a cause is confirmed when it reproduces the problem or makes it appear and disappear predictably.
- Watch for the standard traps: correlation is not causation, and "the same as last time" is a hypothesis, not a conclusion.
- Use unverified blog posts and anecdotes only as leads, and confirm them against primary sources before relying on them.
- Scale investigation depth to the impact of the problem; small problems do not require long external research. Any web research follows the Evidence and Research rules.

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
