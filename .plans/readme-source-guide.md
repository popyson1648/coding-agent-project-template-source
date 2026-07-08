# Plan

## Status

done

## Date

2026-07-08

## Issues

None

## Goal

Improve the source repository README so maintainers and coding agents can quickly distinguish source-side maintenance work from public template content changes.

## Scope

- Rewrite the root `README.md`.
- Clarify the repository purpose, editing boundaries, required reading, verification command, and publication boundary.
- Keep the public template README unchanged.

## Non-goals

- Changing files under `coding-agent-project-template/`.
- Changing publish workflow behavior.
- Changing `.project/` operational documentation.
- Opening or merging a pull request.

## Assumptions

- The root README may be written in Japanese because the requested writing standard is Japanese technical writing.
- The detailed operational source of truth remains under `.project/`.

## Steps

1. Create an approved task plan.
2. Rewrite the root README.
3. Run repository verification.
4. Review the final diff.

## Progress

- [x] Step 1: create an approved task plan
- [x] Step 2: rewrite the root README
- [x] Step 3: run repository verification
- [x] Step 4: review the final diff

## Verification

- `python3 scripts/verify.py`
- `git diff --check`

## Open Issues

None.
