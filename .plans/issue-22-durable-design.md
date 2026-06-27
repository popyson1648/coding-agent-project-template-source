# Plan

## Goal

Resolve issue `#22` by defining a durable implementation standard that avoids known, preventable rework without promising perfect or permanently final code.

## Scope

- Require changes to improve or preserve code health, maintainability, readability, and consistency.
- Require clear names, cohesive responsibilities, explicit interfaces, appropriate tests, and documentation updates.
- Reject knowingly deficient implementations that defer necessary work without recording it.
- Reject speculative abstractions and functionality that are not justified by current requirements.
- Require material tradeoffs and accepted debt to be explicit and tracked.
- Record why the policy uses a durable current-requirements standard instead of an absolute no-future-refactoring guarantee.

## Non-goals

- Guaranteeing that future requirements will never require refactoring.
- Requiring speculative extensibility or exhaustive up-front design.
- Refactoring all existing code.
- Defining warning suppression and root-cause correction rules, which belong to issue `#25`.

## Assumptions

- “Never needs refactoring” is not a verifiable engineering acceptance criterion because requirements and constraints can change.
- A practical standard is to leave no known avoidable deficiency for current requirements and to avoid unsupported future complexity.
- Reviewable, focused changes make design and verification more reliable.

## Steps

1. Use the existing `feature/issue-22-durable-implementation` branch only after rebasing it onto the latest `origin/main`; do not carry issue `#16` or `#25` changes unless they have already merged.
2. Add a decision record that defines the durable implementation standard and rejects both knowingly temporary work and speculative overengineering.
3. Update `.project/conventions.md` and `.template/project-conventions.md` with concrete design and implementation rules.
4. Mirror the template wording into the two published-template convention copies.
5. Review the wording against issue `#16` so evidence requirements support design judgments without duplicating the research policy.

## Verification

- Run `python3 scripts/verify.py --mode all`.
- Run `git diff --check`.
- Compare the three template-facing convention files byte-for-byte.
- Manually verify the result against issue `#22`.

## Open Issues

- None. Future refactoring caused by genuinely new requirements is not treated as a failure of this policy.

## Research Basis

- [Google Engineering Practices: The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html) favors continuous code-health improvement over unattainable perfection.
- [Google Engineering Practices: What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) requires appropriate design and tests while rejecting unnecessary complexity and speculative future functionality.
- [Google Engineering Practices: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) explains why focused changes are easier to design and review well.
