# Decision

## Title

Fix root causes and permit only evidenced, narrow suppressions

## Date

2026-06-27

## Status

Accepted

## Decision

Reproduce and investigate a warning, error, or failing check before modifying code or tool configuration. Fix the underlying cause and rerun the original failing check plus the relevant verification suite.

Do not disable checks, add broad ignores, lower severity, comment out tests, weaken assertions, or alter expected output solely to obtain a passing result.

A suppression is allowed only when evidence confirms a false positive, upstream tool defect, unavoidable compatibility constraint, or explicitly accepted risk and no practical direct fix is available. Use the smallest practical scope, explain the reason next to the exception, preserve relevant coverage, and record a removal condition or tracked follow-up when temporary. A material accepted risk requires recorded user or maintainer approval.

## Context

Issue `#25` identifies warning suppression as an example of a hack that hides a problem instead of correcting it. Some diagnostic tools also provide suppression mechanisms for legitimate false positives and controlled migrations, so an absolute ban would be inaccurate.

## Alternatives

- Ban all suppressions. Rejected because tools can produce false positives and officially support controlled exceptions.
- Permit suppressions whenever verification passes afterward. Rejected because the check may no longer exercise its intended policy.
- Require root-cause correction with narrow, evidenced exceptions. Accepted because it preserves verification integrity without denying legitimate tool limitations.

## Reason

Passing verification is meaningful only when checks and assertions retain their intended strength. Evidence, narrow scope, and explicit removal conditions make exceptional suppressions reviewable and reversible.

## Consequences

- Diagnosis precedes configuration changes.
- Passing checks cannot be manufactured by weakening the checks.
- Exceptions carry enough context for future removal.
- Material risk acceptance is explicit rather than inferred.

## Revisit Conditions

Revisit if the repository adopts a centralized suppression register or automated suppression-expiry checks.
