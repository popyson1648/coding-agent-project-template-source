# Plan

## Status

done

## Date

2026-07-09

## Issues

None

## Goal

Add navigable tables of contents to the public template README files and make the Japanese update section heading easier to understand.

## Scope

- Update `coding-agent-project-template/README.md`.
- Update `coding-agent-project-template/README.ja.md`.
- Rename the Japanese update section to a clearer heading.
- Keep the source repository README files unchanged.

## Non-goals

- Changing template behavior or repository workflows.
- Changing adoption commands.
- Opening or merging a pull request.

## Assumptions

- The public template README files should stay aligned across English and Japanese.
- A top-level table of contents is enough for README navigation.

## Steps

1. Create a branch from `origin/dev`.
2. Add this task plan.
3. Add tables of contents to both public template README files.
4. Rename the update section heading.
5. Run verification.
6. Review the final diff.

## Progress

- [x] Step 1: create a branch from `origin/dev`
- [x] Step 2: add this task plan
- [x] Step 3: add tables of contents to both public template README files
- [x] Step 4: rename the update section heading
- [x] Step 5: run verification
- [x] Step 6: review the final diff

## Verification

- `python3 scripts/verify.py`
- `git diff --check`

## Open Issues

None.
