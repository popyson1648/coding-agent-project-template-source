# Decision

## Title

Tests land in the same chunk as the change; test-first versus test-alongside stays a per-task choice

## Date

2026-07-07

## Status

Accepted

## Decision

The stage at which tests are written is fixed at the chunk level, not the keystroke level: a change
that needs tests is not complete, and is not merged, without them. Within the chunk, the technique
is chosen per task — test-first (TDD) when expected inputs and outputs are clear up front (stating
that intent explicitly), tests alongside or immediately after the code when the design is still
being discovered. Bug fixes start from a failing reproduction test whenever the harness can express
one, and the test stays after the fix. Deferring tests to a later chunk is a known deficiency that
requires recorded approval under the Durable Implementation standard.

## Context

Issue `#9` asks for a defined test-writing stage but flags that mandating TDD would freeze the
development method. The existing rules said "appropriately tested" (Durable Implementation) and "if
the change requires tests, add or update them" without saying when.

## Alternatives

- Mandate TDD. Rejected: fixes one methodology, poorly suited to exploratory design work, and is
  the concern the issue raises.
- Leave timing unspecified. Rejected: "tests later" silently becomes "tests never", the debt pattern
  Durable Implementation forbids.
- Time-based rules (e.g., tests within N days). Rejected: unenforceable and detached from review
  units; the chunk/PR is the natural gate.

## Reason

Anthropic's published guidance treats tests as one of several verification signals rather than a
mandated method, recommends explicitly declaring TDD when used so implementations are not faked
against missing tests, and demonstrates the failing-reproduction-test-first bug-fix flow. Gating at
the reviewable chunk keeps verification meaningful while leaving technique free.

## Consequences

- `Test Timing` section in the shipped and source conventions docs.
- Bug-fix chunks are expected to contain a regression test when the harness allows it.
- Test-deferral needs the same recorded approval as other accepted deficiencies.

## Revisit Conditions

- The template ships a default test harness, making stricter defaults practical.
