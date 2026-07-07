# Decision

## Title

Check current state before proposing, deciding, or acting, and make no external changes during consultation

## Date

2026-07-07

## Status

Accepted

## Decision

Before a proposal, decision, or piece of work, the agent inspects the current state that can be
checked: working tree, configuration, documentation, issue tracker, and any external service
involved. Reports keep checked facts, inferences, and proposals separated, and label unverified
assumptions as unverified.

While the user is consulting, asking, or thinking out loud, the agent does not create issues, post to
external services, change files, or change settings without the user's confirmation; it presents the
intended approach or draft first. Creating GitHub issues the user did not ask for is a forbidden
pattern.

## Context

Issue `#20` reports that acting on unchecked assumptions drifts from the user's intent and from the
actual state of the target, across consultation, research, design, implementation, and external
service changes alike. Issue `#24` reports the concrete failure: issues were created without being
asked. The existing `Evidence and Research` rules cover research-time inspection but not
consultation-stage side effects.

## Alternatives

- Keep the principle implicit in `Evidence and Research`. Rejected: that section governs research for
  material claims, not the general order of check-then-act, and it says nothing about side effects
  during consultation.
- Enumerate every situation that requires a state check. Rejected: a trigger table is the failure
  mode issue `#19` warns against.

## Reason

Anthropic's published agent guidance frames the loop as gather context, act, verify; OpenAI's
guidance likewise has agents gather enough context before acting and avoid tangential actions. A
single check-first principle plus a hard rule against unconfirmed external changes covers both
issues without a checklist.

## Consequences

- `Current State First` section in the shipped and source conventions docs.
- A forbidden pattern bans unrequested external artifacts such as GitHub issues.
- Consultation answers may take slightly longer because state is checked first.

## Revisit Conditions

- The rules prove too coarse and a specific workflow needs its own state-check contract.
