#!/usr/bin/env python3

from __future__ import annotations

import argparse
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
    Path(".github/dependabot.yml"),
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

PINNED_ACTION_WORKFLOWS = [
    SOURCE_ROOT / ".github" / "workflows" / "ci.yml",
    SOURCE_ROOT / ".github" / "workflows" / "publish-template.yml",
    SOURCE_ROOT / ".template" / "ci.yml",
    PUBLIC_TEMPLATE_ROOT / ".github" / "workflows" / "ci.yml",
    PUBLIC_TEMPLATE_ROOT / ".template" / "ci.yml",
]

WORKFLOWS_REQUIRING_READ_PERMISSIONS = PINNED_ACTION_WORKFLOWS

AGENT_RULE_GROUPS = [
    (
        "source repository agent rules",
        SOURCE_ROOT,
        [Path("AGENTS.md"), Path("CLAUDE.md"), Path("GEMINI.md")],
    ),
    (
        "public template agent rules",
        PUBLIC_TEMPLATE_ROOT,
        [Path("AGENTS.md"), Path("CLAUDE.md"), Path("GEMINI.md")],
    ),
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


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        print(f"verification config not found: {config_path}", file=sys.stderr)
        raise SystemExit(2)

    with config_path.open("rb") as f:
        data = tomllib.load(f)

    if not isinstance(data, dict):
        print("verification config must be a TOML table", file=sys.stderr)
        raise SystemExit(2)

    return data


def normalize_phase(name: str, entry: dict) -> dict:
    if not isinstance(entry, dict):
        print(f"phase '{name}' must be a TOML table", file=sys.stderr)
        raise SystemExit(2)

    return {
        "name": name,
        "enabled": bool(entry.get("enabled", False)),
        "command": str(entry.get("command", "")).strip(),
        "reason": str(entry.get("reason", "")).strip(),
        "run_on_edit": _optional_bool(entry.get("run_on_edit")),
        "run_pre_commit": _optional_bool(entry.get("run_pre_commit")),
        "run_pre_push": _optional_bool(entry.get("run_pre_push")),
        "run_in_ci": _optional_bool(entry.get("run_in_ci")),
    }


def _optional_bool(value: object) -> bool | None:
    if value is None:
        return None
    return bool(value)


def collect_phases(config: dict) -> list[dict]:
    raw_phases = config.get("phases")
    if raw_phases is None:
        return []

    if not isinstance(raw_phases, dict):
        print("[phases] must be a TOML table", file=sys.stderr)
        raise SystemExit(2)

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


def workflow_has_read_permissions(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    return "\npermissions:\n  contents: read\n" in f"\n{content}\n"


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
    required_snippets = [
        "branches:",
        "- main",
        "cancel-in-progress: false",
        "actions/create-github-app-token@fee1f7d63c2ff003460e3d139729b119787bc349",
        "actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5",
        "app-id: ${{ vars.APP_ID }}",
        "private-key: ${{ secrets.APP_PRIVATE_KEY }}",
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
    missing = [snippet for snippet in required_snippets if snippet not in content]
    if missing:
        print(
            f"publish workflow is missing required content: {', '.join(missing)}",
            file=sys.stderr,
        )
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

    if unpinned_refs:
        print(
            f"workflow actions are not pinned to full commit SHAs: {', '.join(unpinned_refs)}",
            file=sys.stderr,
        )
        raise SystemExit(2)

    if missing_permissions:
        print(
            f"workflows are missing permissions.contents=read: {', '.join(missing_permissions)}",
            file=sys.stderr,
        )
        raise SystemExit(2)


@register_check("agent-rule-sync")
def check_agent_rule_sync() -> None:
    for scope, root, paths in AGENT_RULE_GROUPS:
        first = root / paths[0]
        pairs = [(first, root / path) for path in paths[1:]]
        ensure_files_identical(pairs, scope)


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


def parse_args() -> argparse.Namespace:
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)

    if args.check:
        return run_named_checks(args.check)

    config = load_config(config_path)
    phases = collect_phases(config)

    only_set = set(args.only)
    selected_phases: list[dict] = []

    for phase in phases:
        if only_set and phase["name"] not in only_set:
            continue
        if is_selected_for_mode(phase, args.mode):
            selected_phases.append(phase)

    if args.list:
        for phase in selected_phases:
            print(phase["name"])
        return 0

    if not selected_phases:
        print("no verification phases selected")
        return 0

    print(f"mode: {args.mode}")
    print(f"config: {config_path}")

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
