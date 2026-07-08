# Decision

## Title

Keep AGENTS.md, CLAUDE.md, and GEMINI.md synchronized

## Date

2026-07-08

## Status

Accepted

## Decision

The repository ships the same durable project guidance in `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.
Each triplet must stay byte-identical in both the source repository root and the public template
subtree.

## Context

The template targets multiple coding agents. Each agent family documents a persistent project
instruction file:

- OpenAI Codex documents `AGENTS.md` for reusable repository guidance:
  https://developers.openai.com/codex/guides/agents-md
- Anthropic documents `CLAUDE.md` for repository code style, review criteria, project rules, and
  preferred patterns:
  https://docs.anthropic.com/en/docs/claude-code/github-actions
- Gemini CLI documents `GEMINI.md` context files for project-specific instructions and coding style
  guides:
  https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html

## Alternatives

- Maintain one provider-specific file only: rejected because the template is intended to work across
  Codex, Claude Code, Gemini CLI, and similar tools.
- Let the files diverge by provider: rejected for the default template because divergent rules can
  make the same repository behave differently depending on which agent reads it.
- Generate provider files from a source file: rejected for now because byte-identical checked-in
  files are simple and sufficient.

## Reason

Keeping the files identical gives every supported agent the same durable repository rules while
matching the documented instruction-file discovery model of each provider.

## Consequences

- Provider-specific exceptions should be rare and require a new decision before relaxing the
  invariant.
- `scripts/verify.py` enforces the invariant for both source and public-template triplets.

## Revisit Conditions

- A provider documents incompatible instruction-file requirements.
- The template introduces provider-specific behavior that cannot be expressed in shared rules.

## Related

- Issue #52
