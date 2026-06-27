# Plan

## Goal

Document the workflow changes required by issue `#1` so the source repository and the published template both describe the same agent operating rules.

## Scope

- Add the autonomous single-chunk implementation rule and `Progress` status conventions to the template conventions document.
- Add PR bot handling, context-reset guidance, and `gh`-based GitHub operation rules where contributors will actually look for them.
- Sync any generated or mirrored project documents that should match the template wording.
- Verify that documentation and repository checks remain aligned after the update.

## Non-goals

- Changing repository automation, bot installations, or GitHub workflow behavior.
- Inventing repository-specific bot entries that are not backed by the current repository setup.
- Updating unrelated template sections that are not needed for the accepted issue scope.

## Assumptions

- Issue `#1` is the intended task because it is the only open issue in this repository.
- The published template should receive contributor-facing operating rules through `coding-agent-project-template/.project/conventions.md`.
- Source-side operational notes may need to live at the repository root `.project/` level when they describe maintenance of this source repository rather than end-user template usage.

## Steps

1. Decide which rules belong in the template conventions document versus source-side maintenance docs, and record only the minimal text needed in each place.
2. Update `.template/project-conventions.md` and `coding-agent-project-template/.project/conventions.md` with:
   - autonomous single-chunk implementation rules
   - branch naming and `1 request = 1 chunk = 1 branch = 1 PR`
   - `Progress` checkbox transitions `[ ] -> [~] -> [x]`
3. Update source-side `.project/` docs with:
   - PR handling flow after opening a PR
   - the policy for listing only materially active bots and their mention format
   - the rule to prompt for context reset at major stopping points
   - the rule to use `gh` for GitHub operations
4. Review whether a decision record is needed for the bot-list placement or rule ownership split; add one only if the resulting structure would otherwise be unclear.
5. Run repository verification and manually review the changed docs against the issue acceptance criteria.

## Verification

- Run `python3 scripts/verify.py --mode all`.
- Manually compare the updated docs against issue `#1` acceptance criteria.
- Review the final diff to confirm template/source-side wording stays consistent where intended.

## Open Issues

- The repository currently exposes no dedicated bot inventory document, so the update may need to introduce policy language without enumerating concrete bots unless the active set can be verified from existing repository configuration.
