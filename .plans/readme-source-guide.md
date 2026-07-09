# Plan

## Status

done

## Date

2026-07-08

## Issues

None

## Goal

Improve the source repository README files so maintainers and coding agents can quickly distinguish source-side maintenance work from public template content changes.

## Scope

- Keep the root `README.md` in English and link it to a Japanese README.
- Add the root `README.ja.md` for Japanese source-repository guidance.
- Clarify the repository purpose, editing boundaries, required reading, verification command, and publication boundary.
- Revise the Japanese README in plain form with a commented directory tree.
- Keep the public template README unchanged.

## Non-goals

- Changing README files under `coding-agent-project-template/`.
- Changing publish workflow behavior.
- Changing `.project/` operational documentation.
- Opening or merging a pull request.

## Assumptions

- Japanese source-repository guidance belongs in the root `README.ja.md`.
- The root `README.md` remains English and only gains a language link.
- The detailed operational source of truth remains under `.project/`.

## Steps

1. Create an approved task plan.
2. Restore the root README to English and add a Japanese README.
3. Revise the Japanese README after maintainer review.
4. Run repository verification.
5. Review the final diff.

## Progress

- [x] Step 1: create an approved task plan
- [x] Step 2: restore the root README to English and add a Japanese README
- [x] Step 3: revise the Japanese README after maintainer review
- [x] Step 4: run repository verification
- [x] Step 5: review the final diff

## Verification

- `python3 scripts/verify.py`
- `git diff --check`

## Open Issues

None.
