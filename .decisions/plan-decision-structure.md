# Decision

## Title

Structure plans and decisions with lifecycle metadata, link sections, and per-component subdirectories

## Date

2026-07-07

## Status

Accepted

## Decision

Plan files carry `Status` (`draft`, `approved`, `in-progress`, `done`, `abandoned`), `Date`,
`Issues`, and a `Progress` checklist using the `[ ]`/`[~]`/`[x]` markers the conventions already
mandate. Decision files gain a `Related` section linking issues, pull requests, and superseding or
superseded records; a replaced decision is marked `superseded` and linked both ways. File naming is
fixed as `issue-{N}-{slug}.md` for issue-driven plans, `{slug}.md` otherwise, and noun-phrase slugs
for decisions. In repositories with multiple components, `.plans/`, `.decisions/`, and `.project/`
mirror component names as subdirectories; single-component repositories stay flat. Existing files
keep their names; the seven existing source plans were migrated by adding `Status: done`.

## Context

Issue `#14` asks for internal structure that improves searchability. Issue `#8` reports that
nothing records whether a plan file itself is finished, in progress, or abandoned. Issue `#6` asks
for directory structure that scales to monorepos. The conventions referenced a `Progress` section
with `[ ]`/`[~]`/`[x]` markers that the plan template never contained — a latent inconsistency this
change repairs.

## Alternatives

- YAML front matter for metadata. Rejected: every existing document uses plain Markdown headings;
  headings keep old and new files uniform and equally greppable (`grep -A2 "^## Status"`).
- MADR-style `NNNN-` numbering for decisions. Rejected for now: renaming existing records would
  churn history and break links from open branches; `Date` plus git history already orders the log.
- A separate machine-readable plan index file. Rejected: a second source of truth that drifts from
  the files it indexes.

## Reason

The structure adapts standard ADR practice — a status lifecycle, a link-rich decision log, and
supersession marked on the old record — to both document types, with the smallest change that makes
`which plans are open` and `what replaced this decision` answerable by grep.

## Consequences

- Both `TEMPLATE.md` files and the six agent-rule files (AGENTS/CLAUDE/GEMINI, root and template)
  encode the new rules.
- Plan files added by concurrently open branches adopt `Status` on their own branches.
- Future decision records include `Related`; existing records are not retrofitted.

## Revisit Conditions

- The decision log grows enough that sequence numbering or an index becomes worth the churn.
- A monorepo adopter needs cross-component plans that the subdirectory rule cannot express.

## Related

- Issues: #6, #8, #14
