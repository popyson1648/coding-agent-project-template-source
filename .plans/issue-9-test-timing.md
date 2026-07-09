# Plan

## Status

done

## Date

2026-07-07

## Issues

Issue `#9`

## Goal

Decide and document the stage at which tests are written, without locking development into a single
methodology such as TDD (issue `#9`).

## Scope

- Add a `Test Timing` section to the conventions doc (three generic copies plus the source
  `.project/conventions.md`): tests land in the same chunk as the change they cover; test-first
  versus test-alongside is a per-task choice; bug fixes start from a failing reproduction test when
  the test harness can express one.
- Record the decision in `.decisions/`.

## Non-goals

- Mandating TDD or any single technique (excluded by the issue).
- Coverage thresholds or test-type selection; `.project/testing.md` owns per-project specifics.

## Assumptions

- Anthropic's guidance treats tests as one of several verification signals, recommends stating TDD
  intent explicitly when used, and demonstrates the failing-reproduction-test-first bug-fix flow
  (`.tmp/web-research/agent-best-practices.md`).

## Steps

1. Insert the `Test Timing` section before `Code Style` in the four conventions files.
2. Add `.decisions/test-timing.md`.
3. Run `python3 scripts/verify.py`; confirm generic copies stay identical.

## Verification

- `python3 scripts/verify.py`
- `diff` between the three generic conventions copies is empty.

## Open Issues

- None.
