# Plan

## Status

done

## Date

2026-07-25

## Issues

- #67

## Goal

Define provider-neutral rules for autonomous, bounded subagent delegation while keeping
integration, verification, and final authority with the main agent.

## Scope

- Define when delegation is useful and when it should be avoided.
- Define a required delegation brief covering objective, scope, expected output and evidence,
  available tools and sources, authority, prohibitions, and dependencies.
- Permit parallel execution only for independent, non-conflicting work.
- Default research and review delegation to read-only, least-privilege access.
- Keep synthesis, conflict resolution, verification, and final judgment with the main agent.
- Prohibit subagent merge, deploy, and irreversible external actions.
- Align source and public-template agent rules and conventions.
- Enforce source-to-public agent-rule synchronization.
- Record the policy decision.

## Non-goals

- Requiring subagents for every task.
- Adding provider-specific subagent definitions, commands, or configuration.
- Implementing an orchestrator or scheduler.
- Allowing automatic merge, deployment, or irreversible external actions.
- Defining the complete iterative delivery loop covered by issue #68.

## Assumptions

- The rule applies only when the active coding-agent environment supports delegation.
- Delegation must provide a material context, specialization, review, or latency benefit.
- Parallel edits require isolated workspaces or explicit non-overlapping ownership.
- Subagent output is evidence to be checked, not an automatically accepted conclusion.

## Steps

1. Record the provider-neutral delegation-policy decision and its alternatives.
2. Add concise active rules to the source and public agent-rule triplets.
3. Add aligned detailed guidance to the source and public conventions.
4. Extend verification so source and public agent-rule triplets cannot drift.
5. Verify synchronization, acceptance criteria, and the full repository.
6. Perform an independent final review and address any findings.

## Progress

- [x] Inspect issue #67, current repository rules, synchronization checks, and primary sources.
- [x] Obtain plan approval.
- [x] Record the decision and update the shared delegation rules.
- [x] Update the conventions copies.
- [x] Enforce source-to-public synchronization.
- [x] Verify and review.

## Verification

- `python3 scripts/verify.py`
- `python3 scripts/verify.py --check agent-rule-sync --check template-sync`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`
- `git diff --check`
- Manual acceptance review against every issue #67 completion criterion.

## Open Issues

None.
