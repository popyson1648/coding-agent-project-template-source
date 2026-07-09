# Plan

## Status

done

## Date

2026-07-07

## Issues

Issue `#30`

## Goal

Make Chrome DevTools (via `chrome-devtools-mcp`) the default way agents verify, debug, and optimize
web UI work, using its full capability set (issue `#30`).

## Scope

- Add a `Web UI Verification` section to the generic conventions copies
  (`.template/project-conventions.md`, `coding-agent-project-template/.template/project-conventions.md`,
  `coding-agent-project-template/.project/conventions.md`) covering: DevTools as the default for
  browser-facing changes, the capability map (rendering/interaction, console, network, performance
  traces, Lighthouse, emulation, heap snapshots), setup, and the fallback rule when the environment
  has no browser.
- Record the decision in `.decisions/`.

## Non-goals

- Adding the rule to the source repository's own `.project/conventions.md`; this repository ships no
  UI surface.
- Bundling or configuring the MCP server inside the template; setup is per-environment.

## Assumptions

- Capabilities and setup per the Chrome DevTools for agents 1.0 announcement and the
  `chrome-devtools-mcp` README (`.tmp/web-research/chrome-devtools-mcp.md`).

## Steps

1. Insert the `Web UI Verification` section before `PR Handling` in the three generic copies.
2. Add `.decisions/web-ui-verification-devtools.md`.
3. Run `python3 scripts/verify.py`; confirm generic copies stay identical.

## Verification

- `python3 scripts/verify.py`
- `diff` between the three generic conventions copies is empty.

## Open Issues

- None.
