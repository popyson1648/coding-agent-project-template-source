# Plan

## Status

done

## Date

2026-07-25

## Issues

- #69

## Goal

Add conservative, language-independent impact-based verification selection while preserving plain
`python3 scripts/verify.py` as the explicit full-verification command.

## Success Criteria

- [x] Verification inputs and event policies are configurable without a language-specific tool.
- [x] Changed paths and transitive input dependencies select the affected verification phases.
- [x] Unknown, global, selector, and indeterminate changes fall back to full verification.
- [x] Selection reports why each phase runs or is omitted.
- [x] Plain `python3 scripts/verify.py` remains explicit full verification.
- [x] Source and public-template configuration, documentation, CI, and verifier behavior stay
  synchronized in their required scopes.
- [x] Selection and post-#68 loop-policy integration have regression coverage and independent
  review.

## Scope

- Add schema version 2 selection metadata to `verification.toml`:
  - named input scopes with repository-relative path patterns
  - transitive input dependencies
  - selector and global paths that force full verification
  - per-phase `always`, `changed`, `scheduled`, and `manual` policies
- Add an event-selection CLI that stays independent from the existing environment-oriented
  `--mode` filter.
- Derive changed paths from an explicit Git base/head pair or repeated changed-file arguments.
- Select phases from direct input matches and the reverse dependency closure.
- Fall back to all eligible phases for unknown paths, global or selector changes, and any
  indeterminate Git or selection result.
- Print deterministic reasons for every phase that is run or omitted.
- Keep the required CI workflow and job running, and perform phase selection inside `verify.py`.
- Apply the same selection contract to the source repository and published template.
- Add unit and integration coverage for schema validation, path matching, Git changes, dependency
  propagation, policies, fallbacks, explanations, and source/template parity.
- Record the design decision and supersede the CI portion of the plain-invocation decision.

## Non-goals

- Requiring Nx, Gradle, Bazel, or a language-specific monorepo or build tool.
- Adding caching, distributed execution, or historical/flakiness-based test prediction.
- Skipping the required GitHub Actions workflow or job with path filters.
- Creating a default schedule for projects generated from the template.
- Turning input dependencies into command ordering or build prerequisites.
- Removing the existing `--mode`, `--only`, `--list`, or source-only `--check` interfaces.

## Assumptions

- Schema version 1 remains accepted and behaves conservatively: missing impact metadata is treated
  as `always`, so an upgraded runner cannot silently omit an existing phase.
- Schema version 2 uses `[inputs.<name>]` tables with `paths` and `depends_on`; phase `inputs`
  reference those names. A scope may represent a module, configuration group, documentation, or
  any other repository input.
- `input_b depends_on input_a` means a change to `input_a` also affects `input_b`. The selector
  computes the transitive reverse-dependent closure and rejects missing references or dependency
  cycles as configuration errors.
- `[selection]` distinguishes `selector_paths` from `global_paths`. The active config file and
  running `verify.py` are protected automatically. A changed path that matches no named input is
  unknown and forces full verification. A named input referenced by no phase explicitly represents
  a known unrelated change.
- Repository path patterns are whole-path, case-sensitive POSIX-style globs. `*`, `?`, and character
  classes stay within one segment; a complete `**` segment matches zero or more segments. Empty,
  absolute, parent-traversing, and negative patterns are rejected.
- The new CLI contract is `--event full|changed|scheduled|manual`, defaulting to `full`.
  `--event changed` accepts `--base` plus `--head`, or repeated `--changed-file`; unavailable or
  indeterminate change data causes a reported full fallback.
- Git comparison resolves one merge base from the base and event head SHAs and reads NUL-delimited
  name/status output with rename detection disabled, so moves are conservatively seen as deletion
  plus addition and unusual path characters are not parsed ambiguously.
- `full` ignores event policies but continues to honor `enabled`, the existing `--mode` filter, and
  an explicit `--only` restriction.
- `scheduled` and `manual` are phase-selection events, not trigger mechanisms. A scheduler, CI
  service, or human remains responsible for invoking them.
- CI compares the checked-out head with the pull-request base SHA or push `before` SHA and fetches
  sufficient history. First pushes, missing history, and invalid SHAs fall back to full.

## Research

- Nx derives affected tasks from Git changes and the reverse project-dependency graph, and defaults
  dependency-file changes to all projects as a fail-safe:
  https://nx.dev/docs/features/ci-features/affected
- Gradle requires complete task input declarations for correct incremental and cached results:
  https://docs.gradle.org/current/userguide/incremental_build.html
  https://docs.gradle.org/current/userguide/build_cache.html
- Git documents merge-base comparison and machine-readable NUL-delimited name/status output:
  https://git-scm.com/docs/git-diff
  https://git-scm.com/docs/git-merge-base
- GitHub documents that path-filtered required workflows can remain pending, while checkout fetches
  one commit by default unless history depth is changed:
  https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs
  https://github.com/actions/checkout
- GitHub keeps schedule and manual workflow triggering separate from code executed by the job:
  https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- Python 3.11 `PurePath.match` and `fnmatch` do not provide the required whole-path recursive glob
  semantics directly, so the restricted matcher must be implemented and tested explicitly:
  https://docs.python.org/3.11/library/pathlib.html
  https://docs.python.org/3.11/library/fnmatch.html
- Google's continuous-testing study supports change/test correlation as a feedback-speed technique
  but does not justify adding predictive selection to this initial implementation:
  https://research.google/pubs/taming-google-scale-continuous-testing/

## Stop Conditions

- Success: all success criteria pass full verification, representative selection scenarios, and
  independent review.
- No progress: stop after two consecutive cycles without measurable progress and report the last
  evidence, attempted approaches, and remaining uncertainty.
- Limits: maximum 8 cycles for the current integration chunk.
- Other: stop before weakening conservative fallbacks, the full-verification path, or issue #68's
  loop-policy checks merely to obtain a passing result.

## Approval Boundaries

- Already-authorized actions (authority source): the user's request to implement all issues and the
  current instruction to push issue #69 and open a ready-for-review pull request.
- Actions requiring confirmation: merge, deploy, publish beyond the authorized pull request, secret
  or credential access, destructive or irreversible action, scope expansion, verification
  weakening, material-risk acceptance, or raising, removing, or resetting the loop limit.

## Steps

1. Add test-first coverage for the version 2 schema, path matcher, named-input dependency graph,
   event policies, reason codes, and conservative fallback matrix in both verifier modules.
2. Implement and validate the shared selection model in the source and public-template verifiers
   without changing the source-only built-in check handlers.
3. Add Git change collection, CLI composition with the existing filters, deterministic
   selected/skipped explanations, and regression coverage for command execution and exit codes.
4. Configure granular source-repository input scopes and safe broad defaults in the public template;
   update all synchronized config copies.
5. Update source and template CI to fetch history and request changed selection inside the always-run
   verification job; keep pre-commit and plain manual verification full.
6. Update source project documentation, synchronized template testing documentation, and the
   published English/Japanese README guidance.
7. Add the impact-selection decision, supersede and cross-link the affected part of the existing
   plain-invocation decision, and keep the task plan current.
8. Run targeted tests, full repository verification, pre-commit, representative selection
   scenarios, and a final consistency and regression review.

## Progress

- [x] Step 1 preparation: inspect issue #69, current implementation, tests, configuration, CI,
  documentation, and relevant decisions; verify the 18-test baseline
- [x] Step 1 preparation: confirm the affected-selection, Git, GitHub Actions, and path-matching
  constraints from official or primary sources
- [x] Step 1: add failing/characterization tests for the selection contract
- [x] Step 2: implement the shared schema and pure selection model
- [x] Step 3: implement Git/CLI/reason integration and regression tests
- [x] Step 4: update source and public-template configuration
- [x] Step 5: update synchronized CI wiring
- [x] Step 6: update source and public-template documentation
- [x] Step 7: record and cross-link the design decisions
- [x] Step 8: complete verification and final review

## Loop State

- Current cycle: 2 of 8 for post-#68 integration.
- Last material observation: the issue #69 implementation rebased onto the merged issues #67 and
  #68. Four expected conflicts were resolved while preserving both impact selection and
  `loop-policy`; the integrated suite passed 54 tests, full verification, and pre-commit. Three
  independent reviews found no unresolved code, selection-safety, provider-neutrality, CI,
  synchronization, or documentation defect after the selection-input and plan-state corrections.
- Next action: push and open the authorized ready-for-review pull request.
- Consecutive cycles without material progress: 0
- Stop or escalation reason: local success criteria and independent review are complete; remote
  publication is authorized, while merge remains a separate confirmation boundary.

## Verification

- [x] `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`: 54 tests passed.
- [x] `python3 scripts/verify.py`: explicit full verification passed.
- [x] `python3 scripts/verify.py --event full`: explicit full verification passed.
- Representative `--event changed` runs for:
  - [x] a directly matched input
  - [x] a transitive dependent input
  - [x] an explicitly known unrelated input
  - [x] an unknown path
  - [x] selector, config, and global paths
  - [x] a missing or invalid Git base
  - [x] `.plans/TEMPLATE.md` and `.project/conventions.md` select `lint`
- [x] `python3 scripts/verify.py --event scheduled --list`
- [x] `python3 scripts/verify.py --event manual --list`
- [x] `python3 coding-agent-project-template/scripts/verify.py --config coding-agent-project-template/.project/verification.toml`
- [x] `pre-commit run --all-files`
- [x] `git diff --check`

## Open Issues

- None.
