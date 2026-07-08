# Coding Agent Project Template Source

This is the source-of-truth repository for the public template
`popyson1648/coding-agent-project-template`.

The published template contents live under `coding-agent-project-template/`. Everything outside that
directory is source-side maintenance material: plans, decisions, verification checks, documentation
templates, and the workflow that publishes the public template.

## Where To Work

- Change files intended for template users under `coding-agent-project-template/`.
- Change source-side plans, decisions, verification, and publish mechanics at the repository root.
- Read `.project/README.md`, `.project/structure.md`, and `.project/release.md` before changing the
  publish flow.

## Verification

Run:

```bash
python3 scripts/verify.py
```

Do not run `scripts/verify.py` directly; it is not required to be executable.
