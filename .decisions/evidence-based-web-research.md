# Decision

## Title

Use risk-based web research and primary sources for external technical facts

## Date

2026-06-27

## Status

Accepted

## Decision

Inspect the repository and current environment first. Before making a material proposal, decision, or implementation that depends on an uncertain, externally defined, or version-dependent fact, search the web and verify that fact.

Prefer current official documentation, specifications, standards, upstream source, and upstream release notes. Use secondary sources only when primary evidence is unavailable, and identify that limitation. Increase the number and independence of sources with the impact and uncertainty of the decision.

Cite the evidence used and separate verified facts from inferences, proposals, and unresolved uncertainty. Never include secrets, credentials, private source, or other sensitive data in search queries.

Web research is optional for stable self-evident facts and facts that can be established directly from the local repository or environment.

## Context

Commands, APIs, frameworks, and hosted services change. Recalled behavior can therefore be stale even when it was once correct. Issue `#16` requests mandatory web research while allowing self-evident facts to be handled without it.

## Alternatives

- Search for every fact. Rejected because it adds noise and delays without improving confidence in locally observable or self-evident facts.
- Search only when the agent feels uncertain. Rejected because confident recall can still be stale for versioned behavior.
- Accept secondary summaries as the default. Rejected because they may omit version, context, or later corrections.

## Reason

The rule makes evidence requirements explicit and proportional to risk. It follows the principle that technical facts and data take precedence over preference, while preserving efficient local inspection.

## Consequences

- Material external claims require current evidence and citations.
- Higher-risk decisions require deeper corroboration.
- Agents must communicate the boundary between evidence and judgment.
- Research must not disclose sensitive information.

## Revisit Conditions

Revisit if the template gains a structured evidence manifest or a repository-specific source policy.
