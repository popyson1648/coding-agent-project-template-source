#!/usr/bin/env python3

from __future__ import annotations

import argparse
from fnmatch import fnmatchcase
import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
import tomllib


DEFAULT_ORDER = [
    "secrets",
    "format",
    "lint",
    "typecheck",
    "build",
    "test_unit",
    "test_integration",
    "test_e2e",
    "test_component",
    "test_contract",
    "accessibility",
    "performance",
    "bundle_size",
]

MODE_FLAG_MAP = {
    "all": None,
    "edit": "run_on_edit",
    "pre-commit": "run_pre_commit",
    "pre-push": "run_pre_push",
    "ci": "run_in_ci",
}

EVENTS = {"full", "changed", "scheduled", "manual"}
SELECTIVE_EVENTS = EVENTS - {"full"}
WHEN_POLICIES = {"always", "changed", "scheduled", "manual"}
SELECTION_KEYS = {"selector_paths", "global_paths"}
INPUT_KEYS = {"paths", "depends_on"}
PHASE_KEYS = {
    "enabled",
    "command",
    "reason",
    "run_on_edit",
    "run_pre_commit",
    "run_pre_push",
    "run_in_ci",
    "when",
    "inputs",
}
TOP_LEVEL_KEYS = {"version", "selection", "inputs", "phases"}

SOURCE_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_TEMPLATE_ROOT = SOURCE_ROOT / "coding-agent-project-template"
PUBLISH_WORKFLOW = SOURCE_ROOT / ".github" / "workflows" / "publish-template.yml"

SOURCE_REQUIRED_PATHS = [
    Path("README.md"),
    Path(".plans"),
    Path(".decisions"),
    Path(".project"),
    Path(".template"),
    Path(".project/verification.toml"),
    Path("renovate.json"),
    Path(".github/workflows/ci.yml"),
    Path("scripts/verify.py"),
    Path("tests/test_verify.py"),
]

PUBLIC_TEMPLATE_REQUIRED_PATHS = [
    Path("README.md"),
    Path("README.ja.md"),
    Path("LICENSE"),
    Path(".gitignore"),
    Path("AGENTS.md"),
    Path("CLAUDE.md"),
    Path("GEMINI.md"),
    Path(".plans/TEMPLATE.md"),
    Path(".decisions/TEMPLATE.md"),
    Path(".project/README.md"),
    Path(".project/build.md"),
    Path(".project/conventions.md"),
    Path(".project/release.md"),
    Path(".project/structure.md"),
    Path(".project/testing.md"),
    Path(".project/verification.toml"),
    Path(".template/ci.yml"),
    Path(".template/pre-commit-config.yaml"),
    Path(".template/project-build.md"),
    Path(".template/project-conventions.md"),
    Path(".template/project-readme.md"),
    Path(".template/project-release.md"),
    Path(".template/project-structure.md"),
    Path(".template/project-testing.md"),
    Path(".template/verification.toml"),
    Path(".github/dependabot.yml"),
    Path(".github/workflows/ci.yml"),
    Path(".pre-commit-config.yaml"),
    Path("scripts/verify.py"),
]

PYTHON_SYNTAX_PATHS = [
    SOURCE_ROOT / "scripts" / "verify.py",
    PUBLIC_TEMPLATE_ROOT / "scripts" / "verify.py",
    SOURCE_ROOT / "tests" / "test_verify.py",
]

PUBLISH_WORKFLOW_REQUIRED_ACTIONS = [
    "actions/checkout",
    "actions/create-github-app-token",
]

PUBLISH_WORKFLOW_REQUIRED_SNIPPETS = [
    "branches:",
    "- main",
    "cancel-in-progress: false",
    "client-id: ${{ vars.APP_ID }}",
    "private-key: ${{ secrets.APP_PRIVATE_KEY }}",
    "permission-workflows: write",
    "repository: popyson1648/coding-agent-project-template",
    "path: public-template",
    "rsync -a --delete --exclude='.git/' --exclude='.template-version'",
    "git status --porcelain",
    "> .template-version",
    "git push",
    "gh release create",
    "gh release view",
    "--generate-notes",
    "release: %s",
]

PINNED_ACTION_WORKFLOWS = [
    SOURCE_ROOT / ".github" / "workflows" / "ci.yml",
    SOURCE_ROOT / ".github" / "workflows" / "publish-template.yml",
    SOURCE_ROOT / ".template" / "ci.yml",
    PUBLIC_TEMPLATE_ROOT / ".github" / "workflows" / "ci.yml",
    PUBLIC_TEMPLATE_ROOT / ".template" / "ci.yml",
]

WORKFLOWS_REQUIRING_READ_PERMISSIONS = PINNED_ACTION_WORKFLOWS

AGENT_RULE_FILES = [Path("AGENTS.md"), Path("CLAUDE.md"), Path("GEMINI.md")]

CI_SELECTION_WORKFLOWS = [
    SOURCE_ROOT / ".github" / "workflows" / "ci.yml",
    SOURCE_ROOT / ".template" / "ci.yml",
    PUBLIC_TEMPLATE_ROOT / ".github" / "workflows" / "ci.yml",
    PUBLIC_TEMPLATE_ROOT / ".template" / "ci.yml",
]

CI_SELECTION_REQUIRED_SNIPPETS = [
    "fetch-depth: 0",
    "github.event.pull_request.base.sha",
    "github.event.pull_request.head.sha",
    "github.event.before",
    "--mode ci",
    "--event changed",
    '--base "$VERIFICATION_BASE_SHA"',
    '--head "$VERIFICATION_HEAD_SHA"',
]

AGENT_RULE_GROUPS = [
    (
        "source repository agent rules",
        SOURCE_ROOT,
        AGENT_RULE_FILES,
    ),
    (
        "public template agent rules",
        PUBLIC_TEMPLATE_ROOT,
        AGENT_RULE_FILES,
    ),
]

AGENT_RULE_CROSS_SCOPE_PAIRS = [
    (SOURCE_ROOT / path, PUBLIC_TEMPLATE_ROOT / path) for path in AGENT_RULE_FILES
]

LOOP_POLICY_HEADING = "Autonomous Execution Loop"

LOOP_POLICY_AGENT_FILES = [
    root / path
    for root in (SOURCE_ROOT, PUBLIC_TEMPLATE_ROOT)
    for path in AGENT_RULE_FILES
]

LOOP_POLICY_CONVENTION_FILES = [
    SOURCE_ROOT / ".project" / "conventions.md",
    SOURCE_ROOT / ".template" / "project-conventions.md",
    PUBLIC_TEMPLATE_ROOT / ".template" / "project-conventions.md",
    PUBLIC_TEMPLATE_ROOT / ".project" / "conventions.md",
]

LOOP_POLICY_PLAN_TEMPLATES = [
    SOURCE_ROOT / ".plans" / "TEMPLATE.md",
    PUBLIC_TEMPLATE_ROOT / ".plans" / "TEMPLATE.md",
]

LOOP_POLICY_REQUIRED_PLAN_SECTIONS = [
    "Status",
    "Goal",
    "Success Criteria",
    "Stop Conditions",
    "Approval Boundaries",
    "Progress",
    "Loop State",
    "Verification",
    "Open Issues",
]

LOOP_POLICY_REQUIRED_AGENT_ANCHORS = [
    "product-specific loop command",
    "finite total-cycle limit",
    "two consecutive cycles without measurable progress",
    "do not raise, remove, or reset",
    "completion evidence by itself",
    "never expands the user's authorization",
    "external writes",
]

LOOP_POLICY_REQUIRED_CONVENTION_ANCHORS = [
    "### Entry Contract",
    "### Cycle",
    "### Evidence and Completion",
    "### Stop and Escalation",
    "default maximum of eight cycles",
    "do not raise, remove, or reset",
    "`scripts/verify.py` supports only",
    "A loop does not expand authority",
]

LOOP_POLICY_REQUIRED_PLAN_ANCHORS = [
    "maximum 8 cycles",
    "Already-authorized actions (authority source):",
    "Actions requiring confirmation:",
    "resetting a loop limit after implementation starts",
    "- Current cycle:",
    "- Last material observation:",
    "- Next action:",
    "- Consecutive cycles without material progress:",
    "- Stop or escalation reason:",
]

ROOT_TEMPLATE_FILES = [
    Path("ci.yml"),
    Path("pre-commit-config.yaml"),
    Path("project-build.md"),
    Path("project-conventions.md"),
    Path("project-readme.md"),
    Path("project-release.md"),
    Path("project-structure.md"),
    Path("project-testing.md"),
    Path("verification.toml"),
]

PUBLIC_TEMPLATE_GENERATED_PAIRS = [
    (Path(".template/ci.yml"), Path(".github/workflows/ci.yml")),
    (Path(".template/pre-commit-config.yaml"), Path(".pre-commit-config.yaml")),
    (Path(".template/project-build.md"), Path(".project/build.md")),
    (Path(".template/project-conventions.md"), Path(".project/conventions.md")),
    (Path(".template/project-readme.md"), Path(".project/README.md")),
    (Path(".template/project-release.md"), Path(".project/release.md")),
    (Path(".template/project-structure.md"), Path(".project/structure.md")),
    (Path(".template/project-testing.md"), Path(".project/testing.md")),
    (Path(".template/verification.toml"), Path(".project/verification.toml")),
]

ACTION_REF_RE = re.compile(r"^\s*(?:-\s*)?uses:\s+([^@\s]+)@([^#\s]+)")
PINNED_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

CHECK_HANDLERS: dict[str, Callable[[], None]] = {}


def config_error(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(2)


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        config_error(f"verification config not found: {config_path}")

    try:
        with config_path.open("rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as error:
        config_error(f"invalid verification config: {error}")

    if not isinstance(data, dict):
        config_error("verification config must be a TOML table")

    return data


def normalize_phase(name: str, entry: dict) -> dict:
    if not isinstance(entry, dict):
        config_error(f"phase '{name}' must be a TOML table")

    return {
        "name": name,
        "enabled": bool(entry.get("enabled", False)),
        "command": str(entry.get("command", "")).strip(),
        "reason": str(entry.get("reason", "")).strip(),
        "run_on_edit": _optional_bool(entry.get("run_on_edit")),
        "run_pre_commit": _optional_bool(entry.get("run_pre_commit")),
        "run_pre_push": _optional_bool(entry.get("run_pre_push")),
        "run_in_ci": _optional_bool(entry.get("run_in_ci")),
        "when": ["always"],
        "inputs": [],
    }


def _optional_bool(value: object) -> bool | None:
    if value is None:
        return None
    return bool(value)


def normalize_string_list(
    value: object,
    field: str,
    *,
    allow_empty: bool = True,
) -> list[str]:
    if not isinstance(value, list):
        config_error(f"{field} must be an array of strings")

    normalized: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            config_error(f"{field} must contain non-empty strings")
        if item in normalized:
            config_error(f"{field} must not contain duplicate values")
        normalized.append(item)

    if not allow_empty and not normalized:
        config_error(f"{field} must not be empty")

    return normalized


def collect_phases(config: dict) -> list[dict]:
    raw_phases = config.get("phases")
    if raw_phases is None:
        return []

    if not isinstance(raw_phases, dict):
        config_error("[phases] must be a TOML table")

    phases_by_name = {
        name: normalize_phase(name, entry)
        for name, entry in raw_phases.items()
    }

    ordered: list[dict] = []

    for name in DEFAULT_ORDER:
        phase = phases_by_name.pop(name, None)
        if phase is not None:
            ordered.append(phase)

    for name in sorted(phases_by_name.keys()):
        ordered.append(phases_by_name[name])

    return ordered


def validate_path_pattern(pattern: str) -> None:
    if not pattern:
        config_error("path patterns must not be empty")
    if pattern.startswith("/") or pattern.endswith("/"):
        config_error(f"path pattern must be repository-relative: {pattern}")
    if "\\" in pattern:
        config_error(f"path pattern must use '/' separators: {pattern}")
    if pattern.startswith("!"):
        config_error(f"negative path patterns are not supported: {pattern}")

    for segment in pattern.split("/"):
        if segment in {"", ".", ".."}:
            config_error(f"invalid path pattern segment in: {pattern}")
        if "**" in segment and segment != "**":
            config_error(f"'**' must occupy a complete path segment: {pattern}")

        index = 0
        while index < len(segment):
            if segment[index] != "[":
                index += 1
                continue

            closing = index + 1
            if closing < len(segment) and segment[closing] in {"!", "^"}:
                closing += 1
            if closing < len(segment) and segment[closing] == "]":
                closing += 1
            closing = segment.find("]", closing)
            if closing < 0:
                config_error(f"unclosed character class in path pattern: {pattern}")
            index = closing + 1


def normalize_changed_path(path: str) -> str | None:
    if not path or "\0" in path or path.startswith("/") or "\\" in path:
        return None

    segments = path.split("/")
    if any(segment in {"", ".", ".."} for segment in segments):
        return None

    return "/".join(segments)


def matches_path(path: str, pattern: str) -> bool:
    normalized_path = normalize_changed_path(path)
    if normalized_path is None:
        return False

    validate_path_pattern(pattern)
    path_segments = normalized_path.split("/")
    pattern_segments = pattern.split("/")
    memo: dict[tuple[int, int], bool] = {}

    def match_from(path_index: int, pattern_index: int) -> bool:
        key = (path_index, pattern_index)
        if key in memo:
            return memo[key]

        if pattern_index == len(pattern_segments):
            result = path_index == len(path_segments)
        elif pattern_segments[pattern_index] == "**":
            result = match_from(path_index, pattern_index + 1) or (
                path_index < len(path_segments)
                and match_from(path_index + 1, pattern_index)
            )
        else:
            result = (
                path_index < len(path_segments)
                and fnmatchcase(
                    path_segments[path_index],
                    pattern_segments[pattern_index],
                )
                and match_from(path_index + 1, pattern_index + 1)
            )

        memo[key] = result
        return result

    return match_from(0, 0)


def normalize_patterns(value: object, field: str) -> list[str]:
    patterns = normalize_string_list(value, field)
    for pattern in patterns:
        validate_path_pattern(pattern)
    return patterns


def collect_inputs(config: dict) -> dict[str, dict]:
    raw_inputs = config.get("inputs", {})
    if not isinstance(raw_inputs, dict):
        config_error("[inputs] must be a TOML table")

    inputs: dict[str, dict] = {}
    for name, entry in raw_inputs.items():
        if not isinstance(name, str) or not name:
            config_error("input names must be non-empty strings")
        if not isinstance(entry, dict):
            config_error(f"input '{name}' must be a TOML table")

        paths = normalize_patterns(
            entry.get("paths", []),
            f"input '{name}' paths",
        )
        if not paths:
            config_error(f"input '{name}' paths must not be empty")

        inputs[name] = {
            "name": name,
            "paths": paths,
            "depends_on": normalize_string_list(
                entry.get("depends_on", []),
                f"input '{name}' depends_on",
            ),
        }

    for name, entry in inputs.items():
        unknown = sorted(set(entry["depends_on"]) - set(inputs))
        if unknown:
            config_error(
                f"input '{name}' depends on unknown inputs: {', '.join(unknown)}"
            )

    visiting: list[str] = []
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visiting:
            cycle_start = visiting.index(name)
            cycle = visiting[cycle_start:] + [name]
            config_error(f"input dependency cycle: {' -> '.join(cycle)}")
        if name in visited:
            return

        visiting.append(name)
        for dependency in inputs[name]["depends_on"]:
            visit(dependency)
        visiting.pop()
        visited.add(name)

    for name in inputs:
        visit(name)

    return inputs


def validate_config(config: dict, config_path: Path | None = None) -> dict:
    if not isinstance(config, dict):
        config_error("verification config must be a TOML table")

    version = config.get("version", 1)
    if type(version) is not int or version not in {1, 2}:
        config_error("verification config version must be 1 or 2")

    if version == 1:
        selector_paths = ["scripts/verify.py"]
        if config_path is not None:
            normalized_config_path = normalize_changed_path(config_path.as_posix())
            if (
                normalized_config_path is not None
                and normalized_config_path not in selector_paths
            ):
                selector_paths.append(normalized_config_path)
        return {
            "version": 1,
            "selection": {
                "selector_paths": selector_paths,
                "global_paths": [],
            },
            "inputs": {},
            "phases": collect_phases(config),
        }

    raw_selection = config.get("selection", {})
    if not isinstance(raw_selection, dict):
        config_error("[selection] must be a TOML table")

    unknown_top_level_keys = sorted(set(config) - TOP_LEVEL_KEYS)
    if unknown_top_level_keys:
        config_error(
            "verification config has unknown top-level keys: "
            f"{', '.join(unknown_top_level_keys)}"
        )

    unknown_selection_keys = sorted(set(raw_selection) - SELECTION_KEYS)
    if unknown_selection_keys:
        config_error(
            "[selection] has unknown keys: "
            f"{', '.join(unknown_selection_keys)}"
        )

    raw_inputs = config.get("inputs", {})
    if isinstance(raw_inputs, dict):
        for name, entry in raw_inputs.items():
            if isinstance(entry, dict):
                unknown_input_keys = sorted(set(entry) - INPUT_KEYS)
                if unknown_input_keys:
                    config_error(
                        f"input '{name}' has unknown keys: "
                        f"{', '.join(unknown_input_keys)}"
                    )

    raw_phases = config.get("phases", {})
    if isinstance(raw_phases, dict):
        for name, entry in raw_phases.items():
            if isinstance(entry, dict):
                unknown_phase_keys = sorted(set(entry) - PHASE_KEYS)
                if unknown_phase_keys:
                    config_error(
                        f"phase '{name}' has unknown keys: "
                        f"{', '.join(unknown_phase_keys)}"
                    )
                if "enabled" in entry and type(entry["enabled"]) is not bool:
                    config_error(f"phase '{name}' enabled must be a boolean")
                for field in ("command", "reason"):
                    if field in entry and not isinstance(entry[field], str):
                        config_error(
                            f"phase '{name}' {field} must be a string"
                        )
                for field in (
                    "run_on_edit",
                    "run_pre_commit",
                    "run_pre_push",
                    "run_in_ci",
                ):
                    if field in entry and type(entry[field]) is not bool:
                        config_error(
                            f"phase '{name}' {field} must be a boolean"
                        )

    selection = {
        "selector_paths": normalize_patterns(
            raw_selection.get("selector_paths", []),
            "selection.selector_paths",
        ),
        "global_paths": normalize_patterns(
            raw_selection.get("global_paths", []),
            "selection.global_paths",
        ),
    }
    if "scripts/verify.py" not in selection["selector_paths"]:
        selection["selector_paths"].append("scripts/verify.py")

    inputs = collect_inputs(config)
    phases = collect_phases(config)

    for phase in phases:
        entry = config["phases"][phase["name"]]
        raw_when = entry.get("when", ["always"])
        when = normalize_string_list(
            raw_when,
            f"phase '{phase['name']}' when",
            allow_empty=False,
        )
        unknown_policies = sorted(set(when) - WHEN_POLICIES)
        if unknown_policies:
            config_error(
                f"phase '{phase['name']}' has unknown when policies: "
                f"{', '.join(unknown_policies)}"
            )
        if "always" in when and len(when) != 1:
            config_error(
                f"phase '{phase['name']}' policy 'always' must be used alone"
            )
        phase["when"] = when
        phase["inputs"] = normalize_string_list(
            entry.get("inputs", []),
            f"phase '{phase['name']}' inputs",
        )

        unknown = sorted(set(phase["inputs"]) - set(inputs))
        if unknown:
            config_error(
                f"phase '{phase['name']}' references unknown inputs: "
                f"{', '.join(unknown)}"
            )
        if "changed" in phase["when"] and not phase["inputs"]:
            config_error(
                f"phase '{phase['name']}' uses 'changed' but declares no inputs"
            )

    if config_path is not None:
        normalized_config_path = normalize_changed_path(config_path.as_posix())
        if (
            normalized_config_path is not None
            and normalized_config_path not in selection["selector_paths"]
        ):
            selection["selector_paths"].append(normalized_config_path)

    return {
        "version": version,
        "selection": selection,
        "inputs": inputs,
        "phases": phases,
    }


def collect_affected_inputs(
    normalized_config: dict,
    changed_paths: list[str],
) -> tuple[set[str], str | None, dict[str, str]]:
    selection = normalized_config["selection"]
    inputs = normalized_config["inputs"]
    directly_affected: set[str] = set()
    reasons: dict[str, str] = {}

    for raw_path in sorted(set(changed_paths)):
        path = normalize_changed_path(raw_path)
        if path is None:
            return set(), f"invalid changed path: {raw_path!r}", {}

        for pattern in selection["selector_paths"]:
            if matches_path(path, pattern):
                reason = f"selector path changed: {path!r} matched {pattern!r}"
                return set(), reason, {}

        for pattern in selection["global_paths"]:
            if matches_path(path, pattern):
                reason = f"global path changed: {path!r} matched {pattern!r}"
                return set(), reason, {}

        matched_inputs: list[tuple[str, str]] = []
        for name, entry in sorted(inputs.items()):
            for pattern in entry["paths"]:
                if matches_path(path, pattern):
                    matched_inputs.append((name, pattern))
                    break

        if not matched_inputs:
            return set(), f"unknown changed path: {path!r}", {}

        for name, pattern in matched_inputs:
            directly_affected.add(name)
            reasons.setdefault(
                name,
                f"changed path {path!r} matched input {name}:{pattern!r}",
            )

    affected = set(directly_affected)
    changed = True
    while changed:
        changed = False
        for name, entry in sorted(inputs.items()):
            if name in affected:
                continue
            dependency = next(
                (
                    dependency
                    for dependency in sorted(entry["depends_on"])
                    if dependency in affected
                ),
                None,
            )
            if dependency is None:
                continue
            affected.add(name)
            reasons[name] = f"input {name} depends on affected input {dependency}"
            changed = True

    return affected, None, reasons


def select_for_event(
    normalized_config: dict,
    event: str,
    changed_paths: list[str] | None = None,
    fallback_reason: str | None = None,
) -> list[dict]:
    if event not in EVENTS:
        config_error(f"unknown verification event: {event}")

    affected_inputs: set[str] = set()
    input_reasons: dict[str, str] = {}
    if event == "changed" and fallback_reason is None:
        affected_inputs, fallback_reason, input_reasons = collect_affected_inputs(
            normalized_config,
            changed_paths or [],
        )

    decisions: list[dict] = []
    for phase in normalized_config["phases"]:
        selected = False
        reason: str

        if not phase["enabled"]:
            reason = phase["reason"] or "phase is disabled"
        elif event == "full":
            selected = True
            reason = "explicit full verification"
        elif fallback_reason is not None:
            selected = True
            reason = f"full fallback: {fallback_reason}"
        elif "always" in phase["when"]:
            selected = True
            reason = "policy always"
        elif event in {"scheduled", "manual"}:
            selected = event in phase["when"]
            if selected:
                reason = f"policy {event}"
            else:
                reason = f"event {event} does not match phase policy"
        elif "changed" not in phase["when"]:
            reason = "event changed does not match phase policy"
        else:
            matched_input = next(
                (
                    input_name
                    for input_name in phase["inputs"]
                    if input_name in affected_inputs
                ),
                None,
            )
            if matched_input is None:
                reason = "no affected inputs"
            else:
                selected = True
                reason = input_reasons[matched_input]

        decisions.append(
            {
                "name": phase["name"],
                "phase": phase,
                "selected": selected,
                "reason": reason,
            }
        )

    return decisions


def is_selected_for_mode(phase: dict, mode: str) -> bool:
    if not phase["enabled"]:
        return False

    flag_name = MODE_FLAG_MAP[mode]
    if flag_name is None:
        return True

    flag_value = phase.get(flag_name)
    if flag_value is None:
        return True

    return bool(flag_value)


def run_command(command: str) -> int:
    completed = subprocess.run(command, shell=True)
    return completed.returncode


def git_command(repo_root: Path, arguments: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *arguments],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def git_failure_reason(operation: str, completed: subprocess.CompletedProcess) -> str:
    detail = completed.stderr.decode("utf-8", errors="replace").strip()
    if detail:
        return f"{operation} failed: {detail}"
    return f"{operation} failed with exit code {completed.returncode}"


def collect_changed_files(
    repo_root: Path,
    base: str,
    head: str,
) -> tuple[list[str], str | None]:
    if not base or not head or base.startswith("-") or head.startswith("-"):
        return [], "invalid Git base or head"

    try:
        merge_base = git_command(repo_root, ["merge-base", "--all", base, head])
    except OSError as error:
        return [], f"cannot run git merge-base: {error}"

    if merge_base.returncode != 0:
        return [], git_failure_reason("git merge-base", merge_base)

    merge_bases = [
        line
        for line in merge_base.stdout.decode("ascii", errors="replace").splitlines()
        if line
    ]
    if len(merge_bases) != 1:
        return [], f"git merge-base returned {len(merge_bases)} results"

    try:
        diff = git_command(
            repo_root,
            [
                "diff",
                "--name-status",
                "-z",
                "--no-renames",
                merge_bases[0],
                head,
                "--",
            ],
        )
    except OSError as error:
        return [], f"cannot run git diff: {error}"

    if diff.returncode != 0:
        return [], git_failure_reason("git diff", diff)

    fields = diff.stdout.split(b"\0")
    if fields and fields[-1] == b"":
        fields.pop()
    if len(fields) % 2 != 0:
        return [], "git diff returned malformed name-status output"

    changed_paths: list[str] = []
    supported_statuses = {"A", "D", "M", "T"}
    for index in range(0, len(fields), 2):
        status = fields[index].decode("ascii", errors="replace")
        path = fields[index + 1].decode("utf-8", errors="surrogateescape")

        if status not in supported_statuses:
            return [], f"git diff returned unsupported status {status!r} for {path!r}"

        normalized_path = normalize_changed_path(path)
        if normalized_path is None:
            return [], f"git diff returned invalid repository path {path!r}"
        if normalized_path not in changed_paths:
            changed_paths.append(normalized_path)

    return changed_paths, None


def register_check(name: str):
    def decorator(func):
        CHECK_HANDLERS[name] = func
        return func

    return decorator


def ensure_paths_exist(root: Path, relative_paths: list[Path], scope: str) -> None:
    missing = [str(path) for path in relative_paths if not (root / path).exists()]
    if missing:
        print(f"{scope} is missing required paths: {', '.join(missing)}", file=sys.stderr)
        raise SystemExit(2)


def ensure_files_identical(pairs: list[tuple[Path, Path]], scope: str) -> None:
    mismatches: list[str] = []

    for left, right in pairs:
        if not left.exists():
            mismatches.append(f"missing {left.relative_to(SOURCE_ROOT)}")
            continue
        if not right.exists():
            mismatches.append(f"missing {right.relative_to(SOURCE_ROOT)}")
            continue
        if left.read_bytes() != right.read_bytes():
            left_name = left.relative_to(SOURCE_ROOT)
            right_name = right.relative_to(SOURCE_ROOT)
            mismatches.append(f"{left_name} != {right_name}")

    if mismatches:
        print(f"{scope} mismatch: {', '.join(mismatches)}", file=sys.stderr)
        raise SystemExit(2)


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(SOURCE_ROOT))
    except ValueError:
        return str(path)


def markdown_heading_lines(lines: list[str]) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    fence_character = ""
    fence_length = 0

    for index, line in enumerate(lines):
        stripped = line.lstrip().rstrip("\r\n")
        fence_match = re.match(r"^(`{3,}|~{3,})", stripped)

        if fence_character:
            if (
                fence_match is not None
                and fence_match.group(1)[0] == fence_character
                and len(fence_match.group(1)) >= fence_length
                and stripped[len(fence_match.group(1)):].strip() == ""
            ):
                fence_character = ""
                fence_length = 0
            continue

        if fence_match is not None:
            fence = fence_match.group(1)
            fence_character = fence[0]
            fence_length = len(fence)
            continue

        if line.startswith("## "):
            headings.append((index, line.rstrip("\r\n")))

    return headings


def extract_markdown_section(path: Path, heading: str) -> str:
    if not path.exists():
        print(f"missing Markdown file: {display_path(path)}", file=sys.stderr)
        raise SystemExit(2)

    marker = f"## {heading}"
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    matches = [
        index
        for index, candidate in markdown_heading_lines(lines)
        if candidate == marker
    ]

    if len(matches) != 1:
        print(
            f"{display_path(path)} must contain exactly one '{marker}' heading",
            file=sys.stderr,
        )
        raise SystemExit(2)

    start = matches[0]
    end = len(lines)
    for index, candidate in markdown_heading_lines(lines):
        if index > start and candidate.startswith("## "):
            end = index
            break

    return "".join(lines[start:end])


def ensure_markdown_sections(path: Path, headings: list[str], scope: str) -> None:
    for heading in headings:
        try:
            extract_markdown_section(path, heading)
        except SystemExit:
            print(f"{scope} is invalid", file=sys.stderr)
            raise


def ensure_markdown_section_identical(
    paths: list[Path],
    heading: str,
    scope: str,
) -> None:
    reference_path = paths[0]
    reference = extract_markdown_section(reference_path, heading)
    mismatches = [
        f"{display_path(reference_path)} != {display_path(path)}"
        for path in paths[1:]
        if extract_markdown_section(path, heading) != reference
    ]

    if mismatches:
        print(f"{scope} mismatch: {', '.join(mismatches)}", file=sys.stderr)
        raise SystemExit(2)


def ensure_text_anchors(
    content: str,
    anchors: list[str],
    path: Path,
    scope: str,
) -> None:
    missing = [anchor for anchor in anchors if anchor not in content]
    if missing:
        print(
            f"{scope} in {display_path(path)} is missing required anchors: "
            f"{', '.join(missing)}",
            file=sys.stderr,
        )
        raise SystemExit(2)


def workflow_has_read_permissions(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    return "\npermissions:\n  contents: read\n" in f"\n{content}\n"


def collect_action_names(content: str) -> set[str]:
    names: set[str] = set()

    for line in content.splitlines():
        match = ACTION_REF_RE.match(line)
        if match is not None:
            names.add(match.group(1))

    return names


def source_path_label(path: Path) -> str:
    try:
        return str(path.relative_to(SOURCE_ROOT))
    except ValueError:
        return str(path)


@register_check("source-layout")
def check_source_layout() -> None:
    ensure_paths_exist(SOURCE_ROOT, SOURCE_REQUIRED_PATHS, "source repository")
    if not PUBLIC_TEMPLATE_ROOT.is_dir():
        print("public template directory is missing", file=sys.stderr)
        raise SystemExit(2)


@register_check("public-template")
def check_public_template() -> None:
    if not PUBLIC_TEMPLATE_ROOT.is_dir():
        print("public template directory is missing", file=sys.stderr)
        raise SystemExit(2)

    ensure_paths_exist(PUBLIC_TEMPLATE_ROOT, PUBLIC_TEMPLATE_REQUIRED_PATHS, "public template")

    if (PUBLIC_TEMPLATE_ROOT / ".git").exists():
        print("public template must not be a nested git repository", file=sys.stderr)
        raise SystemExit(2)


@register_check("publish-workflow")
def check_publish_workflow() -> None:
    if not PUBLISH_WORKFLOW.exists():
        print(f"publish workflow not found: {PUBLISH_WORKFLOW}", file=sys.stderr)
        raise SystemExit(2)

    content = PUBLISH_WORKFLOW.read_text(encoding="utf-8")

    missing_snippets = [
        snippet for snippet in PUBLISH_WORKFLOW_REQUIRED_SNIPPETS if snippet not in content
    ]

    used_actions = collect_action_names(content)
    missing_actions = [
        action for action in PUBLISH_WORKFLOW_REQUIRED_ACTIONS if action not in used_actions
    ]

    if missing_snippets:
        print(
            f"publish workflow is missing required content: {', '.join(missing_snippets)}",
            file=sys.stderr,
        )

    if missing_actions:
        print(
            f"publish workflow is missing required actions: {', '.join(missing_actions)}",
            file=sys.stderr,
        )

    if missing_snippets or missing_actions:
        raise SystemExit(2)


@register_check("python-syntax")
def check_python_syntax() -> None:
    for path in PYTHON_SYNTAX_PATHS:
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")


@register_check("github-actions")
def check_github_actions() -> None:
    unpinned_refs: list[str] = []
    missing_permissions: list[str] = []
    missing_selection_contract: list[str] = []

    for path in PINNED_ACTION_WORKFLOWS:
        if not path.exists():
            unpinned_refs.append(f"missing {path.relative_to(SOURCE_ROOT)}")
            continue

        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            match = ACTION_REF_RE.match(line)
            if match is None:
                continue
            action, ref = match.groups()
            if not PINNED_SHA_RE.match(ref):
                relative = path.relative_to(SOURCE_ROOT)
                unpinned_refs.append(f"{relative}:{line_number} uses {action}@{ref}")

    for path in WORKFLOWS_REQUIRING_READ_PERMISSIONS:
        if not path.exists():
            missing_permissions.append(f"missing {path.relative_to(SOURCE_ROOT)}")
        elif not workflow_has_read_permissions(path):
            missing_permissions.append(str(path.relative_to(SOURCE_ROOT)))

    for path in CI_SELECTION_WORKFLOWS:
        if not path.exists():
            missing_selection_contract.append(
                f"missing {source_path_label(path)}"
            )
            continue

        content = path.read_text(encoding="utf-8")
        missing = [
            snippet
            for snippet in CI_SELECTION_REQUIRED_SNIPPETS
            if snippet not in content
        ]
        if missing:
            relative = source_path_label(path)
            missing_selection_contract.append(
                f"{relative} missing {', '.join(missing)}"
            )

    if unpinned_refs:
        print(
            f"workflow actions are not pinned to full commit SHAs: {', '.join(unpinned_refs)}",
            file=sys.stderr,
        )

    if missing_permissions:
        print(
            f"workflows are missing permissions.contents=read: {', '.join(missing_permissions)}",
            file=sys.stderr,
        )

    if missing_selection_contract:
        print(
            "CI workflows are missing impact-selection behavior: "
            f"{'; '.join(missing_selection_contract)}",
            file=sys.stderr,
        )

    if unpinned_refs or missing_permissions or missing_selection_contract:
        raise SystemExit(2)


@register_check("agent-rule-sync")
def check_agent_rule_sync() -> None:
    for scope, root, paths in AGENT_RULE_GROUPS:
        first = root / paths[0]
        pairs = [(first, root / path) for path in paths[1:]]
        ensure_files_identical(pairs, scope)

    ensure_files_identical(
        AGENT_RULE_CROSS_SCOPE_PAIRS,
        "source and public template agent rules",
    )


@register_check("template-sync")
def check_template_sync() -> None:
    root_template_pairs = [
        (SOURCE_ROOT / ".template" / path, PUBLIC_TEMPLATE_ROOT / ".template" / path)
        for path in ROOT_TEMPLATE_FILES
    ]
    public_generated_pairs = [
        (PUBLIC_TEMPLATE_ROOT / template, PUBLIC_TEMPLATE_ROOT / generated)
        for template, generated in PUBLIC_TEMPLATE_GENERATED_PAIRS
    ]

    ensure_files_identical(root_template_pairs, "source and public template scaffolds")
    ensure_files_identical(public_generated_pairs, "public template generated files")


@register_check("loop-policy")
def check_loop_policy() -> None:
    ensure_markdown_section_identical(
        LOOP_POLICY_AGENT_FILES,
        LOOP_POLICY_HEADING,
        "agent loop policy",
    )
    for path in LOOP_POLICY_AGENT_FILES:
        ensure_text_anchors(
            extract_markdown_section(path, LOOP_POLICY_HEADING),
            LOOP_POLICY_REQUIRED_AGENT_ANCHORS,
            path,
            "agent loop policy",
        )

    ensure_markdown_section_identical(
        LOOP_POLICY_CONVENTION_FILES,
        LOOP_POLICY_HEADING,
        "project convention loop policy",
    )
    for path in LOOP_POLICY_CONVENTION_FILES:
        ensure_text_anchors(
            extract_markdown_section(path, LOOP_POLICY_HEADING),
            LOOP_POLICY_REQUIRED_CONVENTION_ANCHORS,
            path,
            "project convention loop policy",
        )

    reference_plan = LOOP_POLICY_PLAN_TEMPLATES[0]
    ensure_files_identical(
        [(reference_plan, path) for path in LOOP_POLICY_PLAN_TEMPLATES[1:]],
        "source and public template plan state",
    )

    for path in LOOP_POLICY_PLAN_TEMPLATES:
        ensure_markdown_sections(
            path,
            LOOP_POLICY_REQUIRED_PLAN_SECTIONS,
            f"loop plan template {display_path(path)}",
        )
        ensure_text_anchors(
            path.read_text(encoding="utf-8"),
            LOOP_POLICY_REQUIRED_PLAN_ANCHORS,
            path,
            "loop plan template",
        )


def run_named_checks(names: list[str]) -> int:
    unknown = [name for name in names if name not in CHECK_HANDLERS]
    if unknown:
        print(f"unknown checks: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2

    for name in names:
        print(f"[verify] check: {name}")
        CHECK_HANDLERS[name]()
        print(f"[verify] passed: {name}")

    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run repository verification phases from .project/verification.toml."
    )
    parser.add_argument(
        "--config",
        default=".project/verification.toml",
        help="Path to verification.toml",
    )
    parser.add_argument(
        "--mode",
        choices=["all", "edit", "pre-commit", "pre-push", "ci"],
        default="all",
        help="Execution mode",
    )
    parser.add_argument(
        "--event",
        choices=["full", "changed", "scheduled", "manual"],
        default="full",
        help="Verification selection event",
    )
    parser.add_argument(
        "--base",
        help="Base Git revision for --event changed",
    )
    parser.add_argument(
        "--head",
        help="Head Git revision for --event changed",
    )
    parser.add_argument(
        "--changed-file",
        action="append",
        default=[],
        help="Changed repository-relative path for --event changed; repeat as needed",
    )
    parser.add_argument(
        "--only",
        nargs="*",
        default=[],
        help="Run only the specified phases",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List selected phases and exit",
    )
    parser.add_argument(
        "--check",
        action="append",
        default=[],
        help="Run a built-in repository check by name",
    )
    args = parser.parse_args(argv)
    has_git_ref = args.base is not None or args.head is not None
    if has_git_ref and args.changed_file:
        parser.error("--changed-file cannot be combined with --base/--head")
    if args.event != "changed" and (has_git_ref or args.changed_file):
        parser.error("--base, --head, and --changed-file require --event changed")
    return args


def repository_relative_path(path: Path, repo_root: Path) -> str | None:
    try:
        relative = path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return None
    return normalize_changed_path(relative.as_posix())


def protect_selector_files(
    normalized_config: dict,
    config_path: Path,
    repo_root: Path,
) -> None:
    protected_paths = [
        repository_relative_path(config_path, repo_root),
        repository_relative_path(Path(__file__), repo_root),
    ]
    selector_paths = normalized_config["selection"]["selector_paths"]
    for protected_path in protected_paths:
        if protected_path is not None and protected_path not in selector_paths:
            selector_paths.append(protected_path)


def resolve_changed_paths(
    args: argparse.Namespace,
    repo_root: Path,
) -> tuple[list[str], str | None]:
    if args.event != "changed":
        if args.base or args.head or args.changed_file:
            config_error("change source arguments require --event changed")
        return [], None

    if args.changed_file and (args.base or args.head):
        config_error("--changed-file cannot be combined with --base or --head")

    if args.changed_file:
        changed_paths: list[str] = []
        for raw_path in args.changed_file:
            path = normalize_changed_path(raw_path)
            if path is None:
                return [], f"invalid --changed-file path: {raw_path!r}"
            if path not in changed_paths:
                changed_paths.append(path)
        return changed_paths, None

    if args.base and args.head:
        return collect_changed_files(repo_root, args.base, args.head)

    if args.base or args.head:
        return [], "--base and --head must be provided together"

    return [], "changed event has no change source"


def apply_explicit_filters(
    decisions: list[dict],
    mode: str,
    only: set[str],
) -> None:
    for decision in decisions:
        phase = decision["phase"]
        if not phase["enabled"]:
            continue
        if only and phase["name"] not in only:
            decision["selected"] = False
            decision["reason"] = "excluded by --only"
        elif not is_selected_for_mode(phase, mode):
            decision["selected"] = False
            decision["reason"] = f"excluded by mode {mode}"


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)

    if args.check:
        return run_named_checks(args.check)

    config = load_config(config_path)
    normalized_config = validate_config(config, config_path)
    protect_selector_files(normalized_config, config_path, SOURCE_ROOT)

    changed_paths, fallback_reason = resolve_changed_paths(args, SOURCE_ROOT)
    decisions = select_for_event(
        normalized_config,
        args.event,
        changed_paths,
        fallback_reason,
    )
    apply_explicit_filters(decisions, args.mode, set(args.only))
    selected_phases = [
        decision["phase"] for decision in decisions if decision["selected"]
    ]

    if args.list:
        for phase in selected_phases:
            print(phase["name"])
        return 0

    print(f"mode: {args.mode}")
    print(f"event: {args.event}")
    print(f"config: {config_path}")

    if args.event == "changed" and fallback_reason is None:
        if changed_paths:
            print(f"changed files: {len(changed_paths)}")
        else:
            print("changed files: none")

    for decision in decisions:
        outcome = "selected" if decision["selected"] else "skipped"
        print(
            f"[verify] {outcome}: {decision['name']} "
            f"({decision['reason']})"
        )

    if not selected_phases:
        print("no verification phases selected")
        return 0

    for phase in selected_phases:
        print("")
        print(f"[verify] phase: {phase['name']}")

        command = phase["command"]
        if not command:
            reason = phase["reason"]
            if reason:
                print(f"[verify] skipped: {reason}")
                continue
            print(f"[verify] failed: phase '{phase['name']}' has no command", file=sys.stderr)
            return 2

        print(f"[verify] command: {command}")
        code = run_command(command)

        if code != 0:
            print(
                f"[verify] failed: {phase['name']} ( exit code {code} )",
                file=sys.stderr,
            )
            return code

        print(f"[verify] passed: {phase['name']}")

    print("")
    print("[verify] all selected phases passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
