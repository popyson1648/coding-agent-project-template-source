# Coding Agent Project Template

A project harness for working with coding agents (Claude Code, Gemini CLI, Codex, and similar).
It ships shared agent rules, a plan and decision log, project documentation skeletons, and a single
verification entry point wired into pre-commit and CI.

After adopting the template, replace this README with your project's own README.

## What You Get

- `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`: repository rules that agents load; kept identical.
- `.plans/`: one Markdown plan per task (`.plans/TEMPLATE.md`).
- `.decisions/`: one Markdown record per decision (`.decisions/TEMPLATE.md`).
- `.project/`: current project documentation (conventions, structure, build, testing, release).
- `.template/`: source templates for the `.project/` files and for the config files.
- `scripts/verify.py`: runs the verification phases defined in `.project/verification.toml`.
- `.pre-commit-config.yaml` and `.github/workflows/ci.yml`: both call `python3 scripts/verify.py`.

## Start a New Project

1. Click **Use this template** on GitHub and create the repository.
2. Fill in the `.project/` documents from the skeletons in `.template/`.
3. Enable verification phases in `.project/verification.toml` as you add real tooling.
4. Install the local hook: `pre-commit install`.

## Adopt Into an Existing Project

GitHub's "Use this template" only creates new repositories, so adoption is a file copy.

1. Download the template without git history (any equivalent download works):

   ```bash
   npx giget@latest gh:popyson1648/coding-agent-project-template .tmp/agent-template
   ```

2. From your project root, copy everything that does not exist yet (`-n` never overwrites; recent
   GNU cp prints a portability warning for it and offers `--update=none` as the equivalent):

   ```bash
   cp -Rn .tmp/agent-template/.plans .tmp/agent-template/.decisions \
          .tmp/agent-template/.project .tmp/agent-template/.template .
   cp -n .tmp/agent-template/AGENTS.md .tmp/agent-template/CLAUDE.md \
         .tmp/agent-template/GEMINI.md .tmp/agent-template/.pre-commit-config.yaml .
   mkdir -p scripts .github/workflows
   cp -n .tmp/agent-template/scripts/verify.py scripts/
   cp -n .tmp/agent-template/.github/workflows/ci.yml .github/workflows/
   ```

3. Reconcile by hand anything that already existed: merge the template's rules into your existing
   `AGENTS.md`/`CLAUDE.md`/`GEMINI.md` (keep the three identical), and merge the verification step
   into your existing pre-commit and CI configs so both run `python3 scripts/verify.py`.
4. Fill in the `.project/` documents from `.template/` and put your real commands into
   `.project/verification.toml` (phases start disabled so CI stays green until you enable them).
5. Verify and clean up:

   ```bash
   python3 scripts/verify.py
   pre-commit install
   rm -rf .tmp/agent-template
   ```

## Keep Up With Template Updates

Every published change to this template also refreshes `.template-version` (the source commit and
publish date). The file identifies which template version a project carries; never edit it by hand.

### Recommended: merge from the template remote

This works whether the project was created with "Use this template" or adopted by file copy.

```bash
git remote add template https://github.com/popyson1648/coding-agent-project-template.git
git fetch template
git merge template/main --allow-unrelated-histories   # first sync only
```

Every later sync is an ordinary three-way merge:

```bash
git fetch template && git merge template/main
```

- Git records the merge base, so your local customizations survive and conflicts appear only where
  both sides changed the same lines. Resolve them, run `python3 scripts/verify.py`, then commit.
- Do not squash template merges: squashing discards the merge base, and every future sync conflicts
  from scratch.

### Alternative: apply the template diff without adding a remote

If the project has a `.template-version`, you can apply only the template's old-to-new diff:

```bash
git clone https://github.com/popyson1648/coding-agent-project-template .tmp/template
BASE=$(git -C .tmp/template log --format=%H \
  --grep "$(sed -n 's/^source-commit: //p' .template-version)")
git -C .tmp/template diff "$BASE"..HEAD | git apply --reject
rm -rf .tmp/template
```

Resolve any `.rej` files by hand (the diff also refreshes `.template-version`), run
`python3 scripts/verify.py`, then commit. Prefer the merge path when possible; a real three-way
merge resolves more cases than a blind patch.

Projects adopted before `.template-version` existed should use the merge path; its first
`--allow-unrelated-histories` sync establishes the merge base.

For scheduled, automated update PRs, see the third-party
[actions-template-sync](https://github.com/AndreasAugustin/actions-template-sync) action (needs its
own token setup per project).

## Requirements

- Python 3.11+ (for `scripts/verify.py`)
- [pre-commit](https://pre-commit.com/) for the local hook
