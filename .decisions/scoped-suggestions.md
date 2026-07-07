# Decision

## Title

Keep unrequested suggestions minimal and criteria-based, with dependency risk as the worked case

## Date

2026-07-07

## Status

Accepted

## Decision

An unrequested suggestion is made only when it clearly relates to the current work and most of these
hold: the work measurably increases risk or operating burden, deferring carries a high rework cost,
the confirmation or setup cost is proportionate to the gain, and no equivalent measure already
exists (checked, not assumed). Suggestions that can wait are mentioned briefly, not expanded. The
rules stay judgment-based; they must not grow into a trigger table or per-task checklist.

Dependency risk is documented as the one worked case: when a package manager, lockfile, or
high-impact dependency arrives, the agent checks current GitHub settings and
`.github/dependabot.yml`, then suggests reviewing dependency alerts and Dependabot, keeping alerts,
security updates, and version updates distinct, and raising version updates or auto-merge only after
the user's operating policy is confirmed.

## Context

Issue `#19` wants context-appropriate suggestions without the template accumulating fine-grained
trigger conditions that make every task heavier. Issue `#21` wants dependency-risk moments to
trigger a Dependabot/alerts suggestion, with current settings checked first and the three Dependabot
features kept distinct.

## Alternatives

- A comprehensive suggestion checklist per work type. Rejected: explicitly excluded by issue `#19`,
  and Anthropic's guidance warns that bloated always-on rules get ignored.
- No guidance at all. Rejected: the dependency-risk case shows a real, recurring need.
- A separate standalone dependency document. Rejected: one subsection keeps the rule next to the
  criteria that justify it.

## Reason

Criteria (risk, rework cost, confirmation cost, existing coverage) transfer to unforeseen situations;
trigger lists do not. GitHub's documentation separates alerts (Settings), security updates
(Settings), and version updates (`dependabot.yml`), so the rule mirrors that split to keep proposals
accurate.

## Consequences

- `Scoped Suggestions` section with a `Dependency Risk` subsection in the shipped and source
  conventions docs.
- Future "suggest X in situation Y" requests should either fit the criteria or justify amending the
  criteria, not append new trigger rows.

## Revisit Conditions

- A second worked case proves necessary and the section starts reading like a trigger table.
