# Decision

## Title

Adopt a professional troubleshooting method with a source-priority order

## Date

2026-07-07

## Status

Accepted

## Decision

Problem investigation follows a documented method: capture the observed problem precisely, stabilize
first when the problem is disruptive, consult sources in order of reliability (error message and
logs, official documentation, upstream issue tracker and known bugs, release notes and changelogs,
local configuration and version differences, recent changes), test explicit hypotheses one at a time,
and keep observed facts, tested results, and untested hypotheses separated. A cause counts as
confirmed only when it reproduces the problem or toggles it predictably. Investigation depth scales
with impact, and web research defers to the existing `Evidence and Research` rules.

## Context

Issue `#23`: when an agent guesses causes from whatever is at hand, the investigation order and the
suspected components drift from how professionals isolate the same class of problem. The issue asks
for documented investigation references, a source priority, and an explicit separation between
research results, conjecture, and confirmed fact — without mandating long research for every problem.

## Alternatives

- Per-technology runbooks. Rejected: unbounded maintenance and exactly the checklist growth issue
  `#19` excludes.
- Rely on the existing `Fix and Verification Integrity` sentence "reproduce and investigate first".
  Rejected: it states that investigation must happen, not how to do it or which sources outrank
  which.
- Mandate web research for every problem. Rejected by the issue itself.

## Reason

The method is Google SRE's published troubleshooting process (problem report, triage, examine,
diagnose, test, cure), including its hypothetico-deductive core and its named pitfalls: spurious
correlation, over-reliance on past patterns, and improbable theories over simple ones. It composes
cleanly with the existing research and fix-integrity rules instead of duplicating them.

## Consequences

- `Troubleshooting` section in the shipped and source conventions docs, ahead of
  `Fix and Verification Integrity`.
- Cause claims in reports must be backed by reproduction or predictable toggling, or be labeled
  hypotheses.

## Revisit Conditions

- The project adopts incident tooling (tracing, postmortem registry) that changes the examine step.
