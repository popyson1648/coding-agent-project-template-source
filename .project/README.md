# Project Guide

## What This Project Is

A source-of-truth repository for the public GitHub template repository `popyson1648/coding-agent-project-template`.
The finished public template lives under `coding-agent-project-template/`.
Everything outside that subtree is management-only material for maintaining and publishing the template.

## Where To Start

- Edit end-user template files only under `coding-agent-project-template/`.
- Update source-side plans, decisions, and operational docs at the repository root.
- Review `.project/structure.md` before changing the publish flow.

## Minimum Setup

- Python 3.11 or later for `scripts/verify.py`.
- A GitHub App whose numeric app ID is stored in the source repository Actions variable `APP_ID`.
- The same GitHub App's private key is stored in the source repository secret `APP_PRIVATE_KEY`.

## Related Documents

- `.project/conventions.md`
- `.project/structure.md`
- `.project/release.md`
- `.decisions/template-publication-model.md`
