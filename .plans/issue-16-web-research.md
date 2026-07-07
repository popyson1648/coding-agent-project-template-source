# Plan

## Status

done

## Goal

Resolve issue `#16` by requiring evidence-based web research when a claim is uncertain, version-dependent, or material to correctness, while avoiding unnecessary searches for stable, self-evident facts.

## Scope

- Add one consistent research policy to the source conventions, template source, and published template copies.
- Require official documentation and primary sources for commands, flags, APIs, framework behavior, version-specific behavior, and other implementation details that can change.
- Require agents to distinguish verified facts, inferences, and proposals and to identify relevant versions or dates.
- Keep searches free of secrets, credentials, private source, and other sensitive data.
- Record the policy rationale in a decision document.

## Non-goals

- Requiring web searches for arithmetic, repository facts that can be inspected locally, or other stable and self-evident facts.
- Defining the full incident troubleshooting workflow requested by issue `#23`.
- Replacing repository inspection with external research.

## Assumptions

- Local state is authoritative for facts about the checked-out repository.
- Official product documentation, specifications, standards, and upstream release notes are preferred over secondary summaries.
- Research is complete only when the evidence is sufficient for the risk of the decision, not merely when one search result has been found.

## Steps

1. Create `feature/issue-16-web-research` from the latest `origin/main`, without carrying changes from other issues.
2. Add a decision record defining:
   - when web research is required
   - source priority
   - how to report verified facts, inferences, and unresolved uncertainty
   - the sensitive-data boundary
3. Update `.project/conventions.md` and `.template/project-conventions.md`.
4. Mirror the template wording into:
   - `coding-agent-project-template/.project/conventions.md`
   - `coding-agent-project-template/.template/project-conventions.md`
5. Confirm that the wording remains compatible with the future issue `#23` troubleshooting workflow.

## Verification

- Run `python3 scripts/verify.py --mode all`.
- Run `git diff --check`.
- Compare `.template/project-conventions.md`, `coding-agent-project-template/.project/conventions.md`, and `coding-agent-project-template/.template/project-conventions.md` byte-for-byte.
- Review `.project/conventions.md` against the template-facing wording for policy consistency while preserving source-repository-specific guidance.
- Manually verify the result against issue `#16`.

## Open Issues

- None. The policy intentionally scales research depth with decision risk rather than imposing the same search volume on every task.

## Research Basis

- [Google Engineering Practices: The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html) gives technical facts and data priority over opinion.
- [Google SRE: Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) separates observations, hypotheses, tests, and identified root causes.
