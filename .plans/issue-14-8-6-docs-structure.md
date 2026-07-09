# Plan

## Status

done

## Date

2026-07-07

## Issues

`#14`, `#8`, `#6`

## Goal

Structure plan and decision documents so their lifecycle and relations are greppable (issues `#14`,
`#8`) and define how `.plans/`, `.decisions/`, and `.project/` scale to multi-component repositories
(issue `#6`).

## Scope

- `.plans/TEMPLATE.md` (source and template copies): add `Status`, `Date`, `Issues`, and `Progress`
  sections. `Progress` fixes an existing inconsistency: the conventions already mandate `[ ]`/`[~]`/`[x]`
  progress tracking, but the template had no such section.
- `.decisions/TEMPLATE.md` (both copies): add a `Related` section for issues, PRs, and superseding
  or superseded decisions.
- `AGENTS.md`/`CLAUDE.md`/`GEMINI.md` (root and template): document file naming, the plan status
  lifecycle (`draft`, `approved`, `in-progress`, `done`, `abandoned`), and optional per-component
  subdirectories for multi-component repositories.
- Migrate the seven existing source plan files by adding `Status: done` metadata.
- Record the decision in `.decisions/`.

## Non-goals

- Renumbering or renaming existing plan and decision files; the naming convention applies from now on.
- Retrofitting `Related` sections onto existing decision files; their contexts already cite issues.
- Front matter (YAML): the repository's documents use plain Markdown headings; staying with headings
  keeps old and new files uniform and equally greppable.

## Assumptions

- Status lifecycle and link conventions follow common ADR practice (Nygard/MADR: proposed →
  accepted → superseded, decision logs, link-rich records) per `.tmp/web-research/adr-and-plan-structure.md`,
  adapted to plan documents.

## Steps

1. Rewrite both `.plans/TEMPLATE.md` copies.
2. Extend both `.decisions/TEMPLATE.md` copies with `Related`.
3. Update the six agent-rule files (AGENTS/CLAUDE/GEMINI × root/template).
4. Add `Status`/`Date`/`Issues` metadata to the seven existing plan files.
5. Add the decision record; run verification.

## Progress

- [x] Step 1: plan templates
- [x] Step 2: decision templates
- [x] Step 3: agent-rule files
- [x] Step 4: migrate existing plans
- [x] Step 5: decision record and verification

## Verification

- `python3 scripts/verify.py`
- Root and template AGENTS/CLAUDE/GEMINI stay byte-identical triplets.
- `find .plans -name '*.md' -not -name 'TEMPLATE.md' -exec grep -L "## Status" {} +` returns nothing.

## Open Issues

- Plan files added by the concurrently open PRs (#31–#35) receive their `Status` sections on their
  own branches so every branch stays self-consistent.
