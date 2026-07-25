# Plan

## Status

done

## Date

2026-07-25

## Issues

- https://github.com/popyson1648/coding-agent-project-template-source/issues/68

## Goal

Make autonomous loop engineering a provider-neutral repository contract so any capable coding agent
can repeatedly investigate, act, verify, and adapt until it reaches an evidence-backed success or
stop condition without requiring a product-specific slash command or orchestrator.

## Success Criteria

- [x] Shared rules automatically enter an evidence-driven loop for approved implementation or repair
      work without requiring a provider-specific command.
- [x] The rules distinguish verified completion, approval handoff, blocking conditions, no progress,
      and resource limits.
- [x] The loop cannot expand authority, weaken verification, or treat a model or subagent assertion
      as completion evidence.
- [x] Source and public-template agent rules, conventions, and plan-state templates are synchronized
      and protected by automated checks.
- [x] Full repository verification and independent portability and safety review pass.

## Scope

- Define the autonomous execution loop in the shared agent rules and project conventions.
- Define observable success, completion, stop, retry, resource, and human-approval boundaries.
- Use `.plans/` as durable loop state across turns, context compaction, and agent products.
- Use `scripts/verify.py` and configured project checks as the primary executable evidence.
- Keep source and public-template instructions and plan templates aligned.
- Add repository checks and regression tests for the new cross-scope contract.
- Record the design decision and its official research basis.

## Non-goals

- Requiring `/loop`, `/goal`, hooks, schedulers, or any one coding-agent executable.
- Adding an always-on orchestration service.
- Granting new authority, bypassing approvals, or weakening sandbox and safety controls.
- Automatically merging, deploying, publishing, or accepting unresolved material risk.
- Treating repeated model assertions as evidence of completion.

## Assumptions

- The coding agent can read repository Markdown, edit files, and run configured verification commands.
- Product-native loops, hooks, subagents, worktrees, schedulers, and connectors may accelerate the
  workflow but remain optional adapters around the repository contract.
- The user's approval to proceed with Issue #68 approves this provider-neutral implementation
  direction; any material expansion or external write still needs separate authority.

## Stop Conditions

- Success: all success criteria have evidence and every required verification command passes.
- No progress: stop after two consecutive cycles without material progress, or immediately when no
  materially different evidence-backed action remains.
- Limits: maximum 8 cycles; keep this chunk to Issue #68 policy, plan-state schema, synchronization
  checks, tests, and supporting documentation; stop before any product-native orchestrator or
  external write.
- Other: stop for conflicting requirements, missing required tools or coverage, safety uncertainty,
  material unresolved risk, or a new approval boundary.

## Approval Boundaries

- Already-authorized actions (authority source): the user's request and approval authorize official
  web research, local documentation and verification-code changes, tests, and non-destructive local
  verification on this dedicated branch.
- Actions requiring confirmation: commit, push, PR creation, issue mutation, merge, deploy, publish,
  paid services, secrets access, destructive actions, or material scope expansion.
  Raising, removing, or resetting a loop limit after implementation starts also requires explicit
  approval for a new finite limit.

## Steps

1. Research current loop and long-running-agent guidance from primary product and engineering
   sources, then extract provider-neutral invariants.
2. Add an autonomous execution loop to agent rules and project conventions with explicit entry,
   iteration, success, stop, escalation, evidence, and authority rules.
3. Extend the plan template with observable success criteria and compact durable loop-state fields.
4. Extend repository verification and unit tests so source/public agent rules and plan-state
   templates cannot silently drift or lose required loop sections.
5. Record the decision, run the complete verification workflow, and perform an independent final
   review for portability, safety, and consistency.

## Progress

- [x] Step 1: Research provider-neutral loop-engineering invariants.
- [x] Step 2: Add the shared autonomous execution loop rules.
- [x] Step 3: Extend the durable plan-state template.
- [x] Step 4: Add synchronization and contract verification.
- [x] Step 5: Record the decision and complete verification and review.

## Loop State

- Current cycle: 5
- Last material observation: the issue #68 implementation commit was rebased without conflicts onto
  `origin/main` after issue #67 merged. The integrated policy, plan schema, structural and
  contract-anchor checks, and 29 tests passed full repository verification and pre-commit. An
  independent post-rebase review found no correctness, provider-neutrality, loop-finiteness,
  authority, or regression concern.
- Next action: await explicit approval to push the rebased branch and open a draft pull request;
  issue mutation, merge, deploy, and publish remain outside the completed implementation.
- Consecutive cycles without material progress: 0
- Stop or escalation reason: success criteria reached and the local commit and rebase are complete;
  remote publication is a separate approval boundary.

## Verification

- [x] `python3 scripts/verify.py`: passed all configured phases and 29 tests.
- [x] `pre-commit run --all-files`: `verify` hook passed.
- [x] `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`: 29 tests passed.
- [x] `python3 scripts/verify.py --check agent-rule-sync --check template-sync --check loop-policy`:
      all checks passed.
- [x] Manual comparison: all six agent-rule files, all four loop-convention sections, and both plan
      templates match in their required scopes.
- [x] Independent review: portability, safety, dangerous scenarios, and verifier implementation
      passed after resolving every blocking, High, and Medium finding.

## Open Issues

None.
