# Decision

## Title

Document adoption into existing projects as a giget download plus non-overwriting copy

## Date

2026-07-07

## Status

Accepted

## Decision

The published template ships a root `README.md` that documents two adoption paths: GitHub's
"Use this template" for new repositories, and, for existing repositories, downloading a
history-free snapshot with `npx giget@latest gh:popyson1648/coding-agent-project-template` followed
by recursive, non-overwriting copies (`cp -Rn` for template directories and `cp -n` for individual
files), manual reconciliation of pre-existing agent docs and CI, filling `.project/` from
`.template/`, and `python3 scripts/verify.py` as the acceptance check. `README.md` becomes a
required path in the publish verification.

## Context

Issue `#7` asks for a mechanism to introduce this harness into existing projects and suggests
considering a skill or npx. GitHub's template feature cannot target existing repositories, so
adoption is inherently a file-copy operation plus judgment-based reconciliation.

## Alternatives

- Publish a custom npx installer package. Rejected: a published npm package needs versioning,
  release automation, and security upkeep to wrap what one `giget` command and a copy already do —
  speculative complexity under the durable-implementation standard. `giget` is the maintained
  standard downloader (unjs, no local git dependency); `degit` is unmaintained.
- Ship an `adopt.sh` inside the template. Rejected: the script lives in the thing being adopted
  (chicken-and-egg), would need cross-platform testing, and cannot automate the genuinely manual
  step — merging existing AGENTS.md/CI with the template's.
- A Claude Code skill that performs adoption. Rejected for now: couples adoption to one agent
  product; the README procedure works for any agent or human. Revisit if adoption friction proves
  real.

## Reason

A documented, copy-pasteable procedure with an explicit verification step gives existing projects a
reliable path at zero ongoing maintenance cost, and the README doubles as the template's missing
front page.

## Consequences

- `coding-agent-project-template/README.md` exists and is checked by `--check public-template`.
- Adopting projects replace the README with their own after setup (stated in the README).
- Reconciliation of pre-existing files stays a manual, reviewed step.

## Revisit Conditions

- Adoption friction reports justify automation (script, skill, or package).
- The repository moves or is renamed, changing the giget source.

## Related

- Issues: #7
