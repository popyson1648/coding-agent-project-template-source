# Decision

## Title

Use bounded, provider-neutral delegation with main-agent ownership

## Date

2026-07-25

## Status

Accepted

## Decision

Allow the main coding agent to delegate self-contained work without a separate user request when
the active environment supports subagents and delegation offers a material benefit.

Every delegation must state:

- the objective and bounded scope
- the expected output and supporting evidence
- the tools, sources, and context available to the subagent
- whether the task is read-only or may edit an explicitly owned area
- prohibited actions and authority limits
- dependencies on other work

Research, repository exploration, comparisons, log inspection, and independent review default to
read-only access. Parallel work is allowed only when tasks have no unresolved dependency and cannot
conflict through files, branches, generated artifacts, or external state. Parallel edits require
isolated workspaces or explicit non-overlapping ownership.

Delegation never expands the authority granted to the main agent. A subagent's allowed actions must
remain within the current task and be a subset of the main agent's authority.

The main agent remains responsible for checking evidence, resolving conflicting findings,
integrating changes, rerunning verification after integration, making the final judgment, and
reporting to the user. A subagent must not merge, deploy, or perform irreversible external actions.
Subagent use is optional when it would add coordination cost without a material benefit.

These rules are expressed as provider-neutral operating constraints. The template does not require
provider-specific agent definitions, commands, configuration, or APIs.

## Context

Issue #67 asks the template to use subagents autonomously for useful independent work while making
delegation boundaries, parallelism, permissions, and result ownership explicit.

Anthropic recommends subagents for self-contained work, high-volume output, and isolated tool
access, while keeping work that needs frequent back-and-forth or shared context in the main
conversation:

- https://code.claude.com/docs/en/sub-agents

Anthropic's production multi-agent research system found that effective delegation needs an
objective, output format, tools and sources, and clear task boundaries. It also reports that work
with many dependencies is a poor fit for parallel execution:

- https://www.anthropic.com/engineering/multi-agent-research-system

OpenAI's manager-style orchestration keeps one agent responsible for combining specialist outputs
and the final answer. Its code-orchestration guidance limits parallel execution to tasks that do not
depend on one another:

- https://openai.github.io/openai-agents-js/guides/multi-agent/

Gemini CLI similarly describes automatic delegation to specialists with independent context and
restricted tools:

- https://geminicli.com/docs/core/subagents/

The shared principles are stable across providers even though their commands and configuration
formats differ.

## Alternatives

- Require the user to request every delegation. Rejected because it prevents the main agent from
  reducing context pressure and latency during ordinary independent work.
- Require a subagent for every task. Rejected because small or tightly coupled work can cost more to
  coordinate than to perform directly.
- Standardize provider-specific agent files and commands. Rejected because the public template is a
  provider-neutral project harness.
- Let subagents own integration or delivery. Rejected because distributed final authority makes
  conflicts, verification gaps, and external side effects harder to control.
- Allow shared-worktree parallel edits by default. Rejected because edit and generated-artifact
  conflicts can silently invalidate otherwise correct results.

## Reason

Bounded delegation captures the useful common denominator across coding-agent products without
making any one product a dependency. A complete delegation brief reduces context loss and ambiguous
authority. Least-privilege defaults and conflict checks make proactive use safer, while retaining
integration and final judgment in the main agent preserves a single accountable control point.

## Consequences

- Agents may proactively delegate suitable work when the environment supports it.
- Delegation prompts require enough detail for the subagent to work without hidden assumptions.
- Parallelism is unavailable when dependencies, edit ownership, or external-state ownership are
  unclear.
- The main agent must independently inspect subagent evidence and reverify integrated results.
- Environments without subagents continue with the same workflow in the main agent.
- Provider-specific features can improve execution but are never required by the template.

## Revisit Conditions

- A broadly adopted provider-neutral delegation protocol becomes available.
- The supported coding-agent environments expose materially different permission or isolation
  semantics that the common rules cannot represent safely.
- Repository tooling gains isolated workspace management that can make parallel edit ownership
  deterministic.

## Related

- https://github.com/popyson1648/coding-agent-project-template-source/issues/67
- https://github.com/popyson1648/coding-agent-project-template-source/issues/68
- [.decisions/agent-instruction-file-sync.md](agent-instruction-file-sync.md)
