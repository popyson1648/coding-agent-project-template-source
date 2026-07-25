# Decision

## Title

Use a provider-neutral, evidence-driven autonomous execution loop

## Date

2026-07-25

## Status

Accepted

## Decision

The source repository and published template define autonomous loop engineering as a repository
contract, not as a dependency on any coding-agent product.

For each approved reviewable chunk, a capable coding agent automatically repeats:

1. observe the durable plan, repository state, and latest evidence
2. choose and perform one bounded authorized action
3. run relevant verification
4. record the result and adapt the next action
5. complete on objective evidence or stop at an explicit boundary

The task's `.plans/` file is the durable state across turns, context compaction, sessions, and agent
products. It records success criteria, stop conditions, approval boundaries, progress, compact loop
state, verification evidence, and open blockers. `scripts/verify.py` is the common verification
entry point, but its result proves only the relevant enabled phases that actually ran.

Iteration is bounded by the task plan. If no stricter no-progress limit is recorded, the agent stops
after two consecutive cycles without material progress or immediately when no materially different
evidence-backed action is available. Every chunk also has a finite total limit: a plan-specific
limit or a default maximum of eight cycles. A single repeated action is allowed only to test a
documented plausible transient or flaky result. After implementation begins, raising, removing, or
resetting any loop limit requires explicit user or maintainer approval for a new finite limit.

Completion requires evidence for every success criterion on the integrated state, successful
execution of all required verification, current plan state, and final review with no unresolved
material concern except a risk explicitly accepted under the existing approval rules. Model
assertions, checkboxes, subagent reports, and successful worker or session exits are not completion
evidence by themselves.

Product-native loop commands, goals, hooks, schedulers, worktrees, checkpoints, subagents, and agent
APIs are optional adapters. They may automate or accelerate the repository contract but cannot
expand authority, reset limits, weaken verification, or bypass approval boundaries.

## Context

[Loop Engineering](https://addyosmani.com/blog/loop-engineering/) describes an outer system that
finds work, delegates it, checks results, persists what happened, and chooses the next action. It
also emphasizes that durable state must live outside one conversation and that a claim of completion
is not proof. This is an influential practitioner account, not an official Google product
specification, so product behavior is corroborated separately.

[OpenAI's Codex agent-loop explanation](https://openai.com/index/unrolling-the-codex-agent-loop/)
describes the portable observe-and-adapt mechanism: tool results return to the model for subsequent
decisions, possibly over many iterations, while context remains a bounded resource.

[OpenAI Symphony](https://openai.com/index/open-source-codex-orchestration-symphony/) demonstrates
durable task state, bounded concurrency and turns, retries, stall handling, and the distinction
between a successful run, a human-review handoff, and terminal completion. Its Codex app-server and
issue-tracker implementation is an example, not a dependency of this decision.

[Anthropic's agent-loop documentation](https://code.claude.com/docs/en/agent-sdk/agent-loop)
separates tool observations, final results, permissions, maximum turns, maximum budget, and error
outcomes. [Anthropic's long-running-agent research](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
shows why incremental work, persistent progress artifacts, clean handoffs, and explicit testing are
needed across context windows.

[Google's Gemini CLI policy engine](https://geminicli.com/docs/reference/policy-engine/) separates
allowed, denied, and confirmation-required actions, and
[Gemini CLI checkpointing](https://geminicli.com/docs/cli/checkpointing/) persists recoverable state
outside the conversation.
[Google's Managed Agents announcement](https://blog.google/innovation-and-ai/technology/developers-tools/managed-agents-gemini-api/)
also supports versionable Markdown instructions such as `AGENTS.md`, reinforcing a portable
repository-level control surface even when an optional hosted harness is used.

These sources implement different products but converge on the same invariants: persistent state,
bounded tool-driven iteration, objective verification, explicit authority, resource limits, and
distinct success, handoff, blocked, and failed outcomes.

## Alternatives

- Require product-specific `/loop`, `/goal`, hooks, or an SDK. Rejected because availability and
  semantics differ across Codex, Claude Code, Gemini CLI, Antigravity, and other agents.
- Add an always-on scheduler or issue-tracker orchestrator. Rejected because Issue #68 excludes it
  and the repository first needs a portable contract that such orchestrators can consume.
- Treat a successful `scripts/verify.py` exit as sufficient completion evidence. Rejected because a
  new template intentionally begins with many phases disabled; a no-op or partial run cannot prove
  uncovered behavior.
- Retry until success without explicit limits. Rejected because it can waste context and cost,
  repeat deterministic failures, conceal blockers, and cross approval boundaries.
- Introduce new plan statuses such as `blocked` or `awaiting-approval`. Rejected for now to preserve
  the established status lifecycle. A paused loop remains `in-progress` with its stop reason in
  `Loop State` and `Open Issues`.

## Reason

Repository instructions, Markdown state, Git, and executable verification are available across the
target coding-agent ecosystem and survive session boundaries. They express the behavior the project
needs without assuming a particular UI, slash command, model, API, or background service.

Explicit evidence and stop rules let agents proceed autonomously inside already-approved work while
preserving human control over scope, external effects, risk acceptance, publishing, deployment, and
irreversible actions.

## Consequences

- Approved work can continue through corrective cycles without repeated user prompts.
- The same contract can be followed manually, by an interactive agent, or by an optional automated
  orchestrator.
- Plans carry a small amount of additional state and must be updated at meaningful verification
  cycles and handoffs.
- Projects must configure relevant verification before its runner can provide meaningful completion
  evidence; otherwise the agent reports a verification gap.
- Autonomous iteration stops sooner when evidence does not change, which may require a focused human
  decision instead of spending more turns on speculative retries.
- Repository rules cannot wake a client after its host runtime has ended. Recurring or unattended
  execution across sessions needs an optional product, CI, or scheduler adapter that honors the same
  state, evidence, authority, and stop contract.
- Source and public-template loop sections and plan templates are guarded by repository verification.

## Revisit Conditions

- A broadly adopted cross-provider standard offers portable loop state and approval semantics beyond
  repository Markdown.
- The plan-state fields prove too heavy or insufficient in real template adoption.
- False stops show that the default two-cycle no-progress limit needs adjustment.
- A later issue adds an optional orchestrator adapter and needs a machine-readable projection of the
  same contract.

## Related

- https://github.com/popyson1648/coding-agent-project-template-source/issues/68
- [.decisions/subagent-delegation.md](subagent-delegation.md)
- [.decisions/plan-decision-structure.md](plan-decision-structure.md)
- [.decisions/plain-verify-invocation.md](plain-verify-invocation.md)
- [.decisions/root-cause-fixes-and-suppressions.md](root-cause-fixes-and-suppressions.md)
