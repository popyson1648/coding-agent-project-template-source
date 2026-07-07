# Decision

## Title

Use Chrome DevTools via chrome-devtools-mcp as the default web UI verification tool

## Date

2026-07-07

## Status

Accepted

## Decision

For anything that runs in a browser, agents verify, debug, and optimize through Chrome DevTools
exposed by the `chrome-devtools-mcp` MCP server, and use the full toolset the change calls for:
rendering and interaction checks, console messages and script evaluation, network inspection,
performance traces, Lighthouse audits as a quality gate, device and network emulation, and heap
snapshots for memory leaks. Web UI changes are not judged from code alone. When the environment has
no browser or MCP server, the agent states that limitation and uses the closest available
verification instead of skipping silently.

## Context

Issue `#30` asks that Chrome DevTools be used by default and that everything it can do be used. The
global working rules already require "appropriate UI verification methods" for UI changes but name
no tool. Chrome's DevTools-for-agents 1.0 release ships 50+ MCP tools across input automation,
navigation, debugging, performance, network, memory, emulation, and extension categories.

## Alternatives

- Screenshot-only verification. Rejected: misses console errors, network failures, performance
  regressions, and leaks — most of what DevTools exists to expose.
- Generic browser-automation frameworks (Playwright/Puppeteer scripts) as the default. Rejected as
  the default: they are test-authoring tools; chrome-devtools-mcp is purpose-built for agent-driven
  inspection and needs no per-project harness. Projects can still add such suites as test phases.
- Bundling MCP configuration in the template. Rejected: MCP registration is per-environment and
  per-client, not repository state.

## Reason

Google's stated purpose for the release is giving coding agents visibility to "verify, debug, and
optimize code in real time", with Lighthouse audits recommended as a quality gate. Making it the
named default turns the existing abstract "appropriate UI verification" rule into an actionable one.

## Consequences

- `Web UI Verification` section in the generic conventions copies (not the source repository's own
  conventions; this repository ships no UI).
- UI-facing completion reports are expected to cite browser-observed evidence.

## Revisit Conditions

- chrome-devtools-mcp is deprecated or superseded.
- The project standardizes on a different browser or a bundled E2E harness that covers the same
  needs.
