# Decision

## Title

License the public template under MPL-2.0

## Date

2026-07-08

## Status

Accepted

## Decision

The public template repository contents published from `coding-agent-project-template/` are licensed
under the Mozilla Public License 2.0 (MPL-2.0).

## Context

The public GitHub template is intended to be copied and reused by third parties. Without an explicit
license, the reuse terms are unclear for template users.

The maintainer selected MPL-2.0 for the public template in issue #45.

## Alternatives

- No license: rejected because it leaves reuse terms unclear.
- MIT: rejected because the maintainer selected MPL-2.0.

## Reason

MPL-2.0 provides explicit open-source reuse terms while preserving file-level copyleft for covered
source files. The selected license is added only to the published template subtree; source
repository licensing remains out of scope for this decision.

## Consequences

- `coding-agent-project-template/LICENSE` contains the MPL-2.0 text.
- The public template README can display a license badge and point users to `LICENSE`.
- Future public template files are covered by MPL-2.0 unless a more specific notice says otherwise.

## Revisit Conditions

- The maintainer chooses a different license for the public template.
- The source repository license policy is decided separately and requires alignment.

## Related

- Issue #45
