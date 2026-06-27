# Decision

## Title

Require durable implementations for current requirements without speculative design

## Date

2026-06-27

## Status

Accepted

## Decision

Each change must be complete, maintainable, tested as appropriate, and consistent with the codebase for its current known requirements. Do not knowingly ship an avoidable deficiency on the assumption that it will be repaired later.

Use clear names, cohesive responsibilities, explicit interfaces, and the simplest design that satisfies the current requirements. Do not add abstractions, extension points, or functionality solely for hypothetical future needs.

Document material tradeoffs. If a constraint makes debt unavoidable, record its reason, scope, impact, and follow-up or revisit condition in a tracked task or decision.

Future refactoring caused by genuinely new requirements is expected and does not mean the original implementation violated this standard.

## Context

Issue `#22` asks for implementations that will not become future refactoring targets. Taken literally, that outcome cannot be guaranteed because requirements, dependencies, and constraints change. An absolute guarantee would also encourage speculative complexity.

## Alternatives

- Guarantee that code will never require refactoring. Rejected because it is not verifiable and ignores future requirement changes.
- Optimize only for immediate delivery and defer design quality. Rejected because small shortcuts accumulate into maintenance cost.
- Add generic extension points in anticipation of future needs. Rejected because unsupported flexibility increases present complexity.

## Reason

The selected standard prevents known avoidable debt while keeping the design grounded in evidence and current requirements. It aligns durability with maintainability rather than permanence.

## Consequences

- Temporary implementations require an explicit, tracked constraint.
- Tests and documentation are part of implementation completeness when the change requires them.
- Review must consider both maintainability and unnecessary complexity.
- New requirements may still justify later refactoring.

## Revisit Conditions

Revisit if the repository adopts measurable architecture fitness functions or a formal technical-debt register.
