# Plan

## Status

done

## Date

2026-07-07

## Issues

#23

## Goal

Document how agents investigate, isolate, and judge problems the way professionals do, including a
source-priority order and the separation of observed facts, tested results, and hypotheses (issue #23).

## Scope

- Add a `Troubleshooting` section to the conventions doc, placed before `Fix and Verification
  Integrity`, in the three generic conventions copies and the source `.project/conventions.md`.
- Record the decision in `.decisions/`.

## Non-goals

- Mandating long external research for every problem (excluded by the issue).
- Restating the web-research rules; the section defers to `Evidence and Research`.
- Per-technology runbooks.

## Assumptions

- The methodology follows the Google SRE troubleshooting process (problem report, triage, examine,
  diagnose, test, cure; hypothetico-deductive testing; known pitfalls) collected in
  `.tmp/web-research/agent-best-practices.md`.

## Steps

1. Insert the `Troubleshooting` section into the four conventions files.
2. Add `.decisions/troubleshooting-method.md`.
3. Run `python3 scripts/verify.py` and re-check the generic copies stay identical.

## Verification

- `python3 scripts/verify.py`
- `diff` between the three generic conventions copies is empty.

## Open Issues

- None.
