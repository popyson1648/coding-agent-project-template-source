# Plan

## Status

done

## Date

2026-07-07

## Issues

#7

## Goal

Give existing projects a documented, low-maintenance way to adopt this harness (issue #7).

## Scope

- Add `README.md` to the published template covering both paths: new repositories via GitHub's
  "Use this template", and existing repositories via `npx giget@latest` download plus non-overwriting
  copy, followed by reconciliation, `.project/` fill-in, and `python3 scripts/verify.py`.
- Require `README.md` in the publish check (`PUBLIC_TEMPLATE_REQUIRED_PATHS` in `scripts/verify.py`).
- Record the decision, including why a custom npx package and a bundled install script were rejected.

## Non-goals

- Publishing an npm package or Claude Code skill for installation; maintenance cost outweighs a
  file-copy operation (see decision).
- Automatic merging of an existing project's AGENTS.md/CI with the template's; that reconciliation
  is judgment work.

## Assumptions

- `giget` is the maintained standard for downloading a repo snapshot without history
  (`.tmp/web-research/template-adoption.md`); GitHub's "Use this template" cannot target existing
  repositories.

## Steps

1. Write `coding-agent-project-template/README.md`.
2. Add `README.md` to the required-path check in source `scripts/verify.py`.
3. Add the decision record; run verification.

## Progress

- [x] Step 1: README
- [x] Step 2: publish check
- [x] Step 3: decision and verification

## Verification

- `python3 scripts/verify.py`
- Adoption commands exercised against a scratch directory.

## Open Issues

- None.
