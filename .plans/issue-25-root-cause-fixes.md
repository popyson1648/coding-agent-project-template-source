# Plan

## Status

done

## Goal

Resolve issue `#25` by requiring root-cause fixes and preventing warnings, errors, and failing checks from being hidden merely to obtain a passing result.

## Scope

- Require inspection and diagnosis before changing code or tool configuration.
- Prohibit broad ignores, disabled checks, commented-out tests, fabricated success, and equivalent bypasses used only to make verification pass.
- Permit a narrow suppression only after confirming a false positive, upstream tool defect, compatibility constraint, or deliberately accepted risk.
- Require an allowed exception to use the smallest practical scope, explain the reason near the exception, preserve relevant tests, and state a removal condition or tracked follow-up when temporary.
- Record the exception model and its relationship to issues `#16`, `#22`, and `#23`.

## Non-goals

- Prohibiting every suppression mechanism provided by a compiler or linter.
- Requiring an unrelated legacy warning backlog to be fixed in one change.
- Defining the full evidence-gathering and troubleshooting workflow requested by issue `#23`.
- Treating a warning as proof of a defect without investigation.

## Assumptions

- A passing check is evidence only when the check still exercises its intended policy or behavior.
- Some tools produce legitimate false positives or support controlled migration of existing violations.
- Broad or unexplained suppressions conceal risk and make later removal difficult.

## Steps

1. Create `feature/issue-25-root-cause-fixes` from the latest `origin/main`, without carrying changes from other open issue branches.
2. Add a decision record defining prohibited bypasses and the narrow exception criteria.
3. Update `.project/conventions.md` and `.template/project-conventions.md` with diagnosis, root-cause correction, and exception rules.
4. Mirror the template wording into the two published-template convention copies.
5. Check consistency with:
   - issue `#16`: evidence required before accepting an exception
   - issue `#22`: no silent technical debt
   - issue `#23`: later troubleshooting guidance may expand the diagnosis process

## Verification

- Run `python3 scripts/verify.py --mode all`.
- Run `git diff --check`.
- Compare the three template-facing convention files byte-for-byte.
- Manually verify the result against issue `#25`.

## Open Issues

- None. The exception criteria are intentionally tool-neutral; language-specific projects may add stricter rules.

## Research Basis

- [Google SRE: Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) uses observed state, explicit hypotheses, tests, and corrective action to prevent recurrence.
- [NIST Secure Software Development Framework 1.1](https://www.nist.gov/publications/secure-software-development-framework-ssdf-version-11-recommendations-mitigating-risk) recommends addressing root causes to prevent recurrence in its security scope.
- [ESLint: Configure Rules](https://eslint.org/docs/latest/use/configure/rules) supports local configuration descriptions and reporting unused inline configuration.
- [ESLint: Bulk Suppressions](https://eslint.org/docs/latest/use/suppressions) keeps new violations enforced while existing violations are resolved and supports pruning obsolete suppressions.
