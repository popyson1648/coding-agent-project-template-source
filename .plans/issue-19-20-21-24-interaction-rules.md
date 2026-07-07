# Plan

## Status

done

## Date

2026-07-07

## Issues

#19, #20, #21, #24

## Goal

Document interaction rules for agents: check current state before proposing or acting, keep facts,
inferences, and proposals separated, make no external changes during consultation (including issue
creation), keep unrequested suggestions minimal, and define when to suggest dependency-risk checks.

## Scope

- Add a `Current State First` section to the conventions doc (issues #20, #24).
- Add a `Scoped Suggestions` section with judgment criteria and a `Dependency Risk` subsection
  covering dependency alerts and Dependabot (issues #19, #21).
- Add a forbidden pattern banning unrequested external artifacts such as issues.
- Apply identically to the generic conventions copies (`.template/project-conventions.md`,
  `coding-agent-project-template/.template/project-conventions.md`,
  `coding-agent-project-template/.project/conventions.md`) and to the source repository's
  `.project/conventions.md`.
- Record the decisions in `.decisions/`.

## Non-goals

- A trigger table or per-task checklist (explicitly excluded by issue #19).
- Shipping a `.github/dependabot.yml`; enabling Dependabot is a per-project, policy-confirmed step.
- New tooling; these are documentation rules.

## Assumptions

- Suggestion-restraint and state-checking guidance follows Anthropic, OpenAI, and Google published
  practices collected in `.tmp/web-research/agent-best-practices.md`.
- Dependabot feature separation per GitHub docs in `.tmp/web-research/dependabot.md`.

## Steps

1. Insert the two new sections before `Review Expectations` in the four conventions files.
2. Extend `Forbidden Patterns` in the same files.
3. Add `.decisions/current-state-first.md` and `.decisions/scoped-suggestions.md`.
4. Run `python3 scripts/verify.py` and confirm the three generic copies stay identical.

## Verification

- `python3 scripts/verify.py`
- `diff` between the three generic conventions copies is empty.

## Open Issues

- None.
