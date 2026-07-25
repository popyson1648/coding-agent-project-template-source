from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_verify_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_selection_config() -> dict:
    return {
        "version": 2,
        "selection": {
            "selector_paths": ["selection/**"],
            "global_paths": ["pyproject.toml"],
        },
        "inputs": {
            "shared": {
                "paths": ["lib/**"],
                "depends_on": [],
            },
            "app": {
                "paths": ["src/app/**"],
                "depends_on": ["shared"],
            },
            "frontend": {
                "paths": ["src/frontend/**"],
                "depends_on": ["app"],
            },
            "docs": {
                "paths": ["docs/**/*.md"],
                "depends_on": [],
            },
            "notes": {
                "paths": ["notes/**"],
                "depends_on": [],
            },
        },
        "phases": {
            "always_check": {
                "enabled": True,
                "command": "true",
                "inputs": [],
                "when": ["always"],
            },
            "test_unit": {
                "enabled": True,
                "command": "true",
                "inputs": ["shared"],
                "when": ["changed"],
            },
            "test_integration": {
                "enabled": True,
                "command": "true",
                "inputs": ["app"],
                "when": ["changed"],
            },
            "test_e2e": {
                "enabled": True,
                "command": "true",
                "inputs": ["frontend"],
                "when": ["changed"],
            },
            "docs_check": {
                "enabled": True,
                "command": "true",
                "inputs": ["docs"],
                "when": ["changed"],
            },
            "scheduled_check": {
                "enabled": True,
                "command": "true",
                "inputs": [],
                "when": ["scheduled"],
            },
            "manual_check": {
                "enabled": True,
                "command": "true",
                "inputs": [],
                "when": ["manual"],
            },
            "changed_or_manual": {
                "enabled": True,
                "command": "true",
                "inputs": ["app"],
                "when": ["changed", "manual"],
            },
            "disabled_check": {
                "enabled": False,
                "reason": "not configured",
                "inputs": [],
                "when": ["always"],
            },
        },
    }


class VerifyCommonBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.modules = [
            load_verify_module("source_verify", REPO_ROOT / "scripts" / "verify.py"),
            load_verify_module(
                "template_verify",
                REPO_ROOT / "coding-agent-project-template" / "scripts" / "verify.py",
            ),
        ]

    def test_collect_phases_orders_default_names_before_unknown_names(self) -> None:
        config = {
            "phases": {
                "z_custom": {"enabled": True, "command": "z"},
                "lint": {"enabled": True, "command": "lint"},
                "a_custom": {"enabled": True, "command": "a"},
                "format": {"enabled": False, "reason": "skip"},
            }
        }

        for module in self.modules:
            with self.subTest(module=module.__name__):
                phases = module.collect_phases(config)
                self.assertEqual(
                    [phase["name"] for phase in phases],
                    ["format", "lint", "a_custom", "z_custom"],
                )

    def test_collect_phases_rejects_non_table_phases(self) -> None:
        for module in self.modules:
            with self.subTest(module=module.__name__):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        module.collect_phases({"phases": []})
                self.assertEqual(raised.exception.code, 2)

    def test_is_selected_for_mode_respects_enabled_and_mode_flags(self) -> None:
        phase = {
            "enabled": True,
            "run_on_edit": False,
            "run_pre_commit": None,
            "run_pre_push": True,
            "run_in_ci": None,
        }

        for module in self.modules:
            with self.subTest(module=module.__name__):
                self.assertTrue(module.is_selected_for_mode(phase, "all"))
                self.assertFalse(module.is_selected_for_mode(phase, "edit"))
                self.assertTrue(module.is_selected_for_mode(phase, "pre-commit"))
                self.assertTrue(module.is_selected_for_mode(phase, "pre-push"))
                self.assertTrue(module.is_selected_for_mode(phase, "ci"))
                self.assertFalse(module.is_selected_for_mode({"enabled": False}, "all"))

    def test_load_config_reads_toml_table(self) -> None:
        for module in self.modules:
            with self.subTest(module=module.__name__):
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "verification.toml"
                    path.write_text("version = 1\n", encoding="utf-8")
                    self.assertEqual(module.load_config(path), {"version": 1})

    def test_load_config_rejects_missing_file(self) -> None:
        for module in self.modules:
            with self.subTest(module=module.__name__):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        module.load_config(Path("does-not-exist.toml"))
                self.assertEqual(raised.exception.code, 2)


class ImpactSelectionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.modules = [
            load_verify_module(
                "source_verify_selection",
                REPO_ROOT / "scripts" / "verify.py",
            ),
            load_verify_module(
                "template_verify_selection",
                REPO_ROOT / "coding-agent-project-template" / "scripts" / "verify.py",
            ),
        ]

    def normalized_config(self, module):
        return module.validate_config(
            copy.deepcopy(make_selection_config()),
            Path(".custom/verification.toml"),
        )

    def assert_config_error(self, module, config: dict) -> str:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as raised:
                module.validate_config(config, Path(".project/verification.toml"))
        self.assertEqual(raised.exception.code, 2)
        return stderr.getvalue()

    def decision_map(self, decisions: list[dict]) -> dict[str, dict]:
        result = {decision["name"]: decision for decision in decisions}
        self.assertEqual(len(result), len(decisions))
        for decision in decisions:
            self.assertIsInstance(decision["selected"], bool)
            self.assertIsInstance(decision["reason"], str)
            self.assertTrue(decision["reason"])
            self.assertEqual(decision["phase"]["name"], decision["name"])
        return result

    def selected_names(self, decisions: list[dict]) -> set[str]:
        return {
            decision["name"]
            for decision in decisions
            if decision["selected"]
        }

    def enabled_names(self, config: dict) -> set[str]:
        return {
            phase["name"]
            for phase in config["phases"]
            if phase["enabled"]
        }

    def test_version_one_remains_conservative(self) -> None:
        config = {
            "version": 1,
            "phases": {
                "lint": {
                    "enabled": True,
                    "command": "lint",
                    "inputs": ["ignored"],
                    "when": ["changed"],
                },
                "test_unit": {
                    "enabled": True,
                    "command": "test",
                    "when": ["manual"],
                },
            },
        }

        for module in self.modules:
            with self.subTest(module=module.__name__):
                normalized = module.validate_config(copy.deepcopy(config))
                self.assertEqual(normalized["version"], 1)
                self.assertTrue(
                    all(phase["when"] == ["always"] for phase in normalized["phases"])
                )
                self.assertTrue(
                    all(phase["inputs"] == [] for phase in normalized["phases"])
                )
                self.assertEqual(
                    self.selected_names(
                        module.select_for_event(
                            normalized,
                            "changed",
                            ["unmapped.file"],
                        )
                    ),
                    {"lint", "test_unit"},
                )

    def test_version_two_schema_is_normalized(self) -> None:
        for module in self.modules:
            with self.subTest(module=module.__name__):
                normalized = self.normalized_config(module)
                self.assertEqual(normalized["version"], 2)
                self.assertEqual(set(normalized["inputs"]), {
                    "shared",
                    "app",
                    "frontend",
                    "docs",
                    "notes",
                })
                phases = {phase["name"]: phase for phase in normalized["phases"]}
                self.assertEqual(phases["test_unit"]["inputs"], ["shared"])
                self.assertEqual(phases["test_unit"]["when"], ["changed"])
                self.assertEqual(
                    phases["changed_or_manual"]["when"],
                    ["changed", "manual"],
                )

    def test_schema_rejects_unsupported_versions(self) -> None:
        for module in self.modules:
            for version in (0, 3, "2", None):
                with self.subTest(module=module.__name__, version=version):
                    config = make_selection_config()
                    config["version"] = version
                    message = self.assert_config_error(module, config)
                    self.assertIn("version", message.lower())

    def test_schema_rejects_invalid_repository_patterns(self) -> None:
        invalid_patterns = [
            "",
            "/absolute/**",
            "../outside/**",
            "src/../outside",
            "!src/**",
            "src//file.py",
            "src/**suffix",
            "src\\file.py",
        ]

        for module in self.modules:
            for pattern in invalid_patterns:
                with self.subTest(module=module.__name__, pattern=pattern):
                    config = make_selection_config()
                    config["inputs"]["app"]["paths"] = [pattern]
                    message = self.assert_config_error(module, config)
                    self.assertTrue(message.strip())

    def test_version_two_schema_rejects_unknown_keys_and_loose_types(self) -> None:
        mutations = [
            lambda config: config.__setitem__("unexpected", True),
            lambda config: config["selection"].__setitem__("unexpected", []),
            lambda config: config["inputs"]["app"].__setitem__("unexpected", []),
            lambda config: config["phases"]["test_unit"].__setitem__(
                "unexpected",
                True,
            ),
            lambda config: config["phases"]["test_unit"].__setitem__(
                "enabled",
                "yes",
            ),
            lambda config: config["phases"]["test_unit"].__setitem__(
                "command",
                123,
            ),
            lambda config: config["phases"]["test_unit"].__setitem__(
                "run_in_ci",
                "yes",
            ),
            lambda config: config["selection"]["selector_paths"].append(
                "selection/**"
            ),
            lambda config: config["inputs"]["app"]["paths"].append(
                "src/app/**"
            ),
            lambda config: config["inputs"]["app"]["depends_on"].append(
                "shared"
            ),
            lambda config: config["phases"]["test_unit"]["inputs"].append(
                "shared"
            ),
        ]

        for module in self.modules:
            for index, mutate in enumerate(mutations):
                with self.subTest(module=module.__name__, mutation=index):
                    config = make_selection_config()
                    mutate(config)
                    self.assertTrue(self.assert_config_error(module, config).strip())

    def test_schema_rejects_missing_dependencies_and_cycles(self) -> None:
        for module in self.modules:
            with self.subTest(module=module.__name__, case="missing"):
                config = make_selection_config()
                config["inputs"]["app"]["depends_on"] = ["missing"]
                message = self.assert_config_error(module, config)
                self.assertIn("missing", message)

            with self.subTest(module=module.__name__, case="cycle"):
                config = make_selection_config()
                config["inputs"]["shared"]["depends_on"] = ["frontend"]
                message = self.assert_config_error(module, config)
                self.assertIn("cycle", message.lower())

    def test_schema_rejects_unknown_phase_inputs(self) -> None:
        for module in self.modules:
            with self.subTest(module=module.__name__):
                config = make_selection_config()
                config["phases"]["test_unit"]["inputs"] = ["missing"]
                message = self.assert_config_error(module, config)
                self.assertIn("missing", message)

    def test_schema_rejects_invalid_event_policies(self) -> None:
        invalid_policies = [
            [],
            ["sometimes"],
            ["always", "changed"],
            ["changed", "changed"],
            "changed",
        ]

        for module in self.modules:
            for when in invalid_policies:
                with self.subTest(module=module.__name__, when=when):
                    config = make_selection_config()
                    config["phases"]["test_unit"]["when"] = when
                    message = self.assert_config_error(module, config)
                    self.assertTrue(message.strip())

    def test_matches_whole_posix_paths(self) -> None:
        cases = [
            ("verify.py", "*.py", True),
            ("scripts/verify.py", "*.py", False),
            ("scripts/a.py", "scripts/?.py", True),
            ("scripts/ab.py", "scripts/?.py", False),
            ("src/a.py", "src/[ab].py", True),
            ("src/c.py", "src/[ab].py", False),
            ("src/generated/file.py", "src/*/file.py", True),
            ("src/a/b/file.py", "src/*/file.py", False),
            ("src/file.py", "src/**/file.py", True),
            ("src/a/b/file.py", "src/**/file.py", True),
            ("file.py", "**/*.py", True),
            ("src/a/file.py", "**/*.py", True),
            ("src", "src/**", True),
            ("src/a/b", "src/**", True),
            ("docs/guide.md.bak", "docs/**/*.md", False),
            ("Docs/guide.md", "docs/**/*.md", False),
        ]

        for module in self.modules:
            for path, pattern, expected in cases:
                with self.subTest(
                    module=module.__name__,
                    path=path,
                    pattern=pattern,
                ):
                    self.assertIs(
                        module.matches_path(path, pattern),
                        expected,
                    )

    def test_affected_inputs_include_transitive_reverse_dependencies(self) -> None:
        for module in self.modules:
            with self.subTest(module=module.__name__):
                normalized = self.normalized_config(module)
                affected, fallback, reasons = module.collect_affected_inputs(
                    normalized,
                    ["lib/core.py"],
                )
                self.assertEqual(affected, {"shared", "app", "frontend"})
                self.assertIsNone(fallback)
                self.assertTrue(reasons)
                self.assertTrue(all(reasons.values()))

    def test_known_unreferenced_input_does_not_force_full(self) -> None:
        for module in self.modules:
            with self.subTest(module=module.__name__):
                normalized = self.normalized_config(module)
                affected, fallback, reasons = module.collect_affected_inputs(
                    normalized,
                    ["notes/idea.txt"],
                )
                self.assertEqual(affected, {"notes"})
                self.assertIsNone(fallback)
                self.assertTrue(reasons)
                self.assertTrue(all(reasons.values()))

                decisions = module.select_for_event(
                    normalized,
                    "changed",
                    ["notes/idea.txt"],
                )
                self.assertEqual(
                    self.selected_names(decisions),
                    {"always_check"},
                )

    def test_unknown_global_selector_and_automatic_paths_force_full(self) -> None:
        cases = [
            ("unknown/file.txt", ("unknown",)),
            ("pyproject.toml", ("global",)),
            ("selection/rules.toml", ("selector",)),
            (".custom/verification.toml", ("config", "selector")),
            ("scripts/verify.py", ("runner", "selector")),
        ]

        for module in self.modules:
            normalized = self.normalized_config(module)
            for path, reason_words in cases:
                with self.subTest(module=module.__name__, path=path):
                    affected, fallback, _ = module.collect_affected_inputs(
                        normalized,
                        [path],
                    )
                    self.assertEqual(affected, set())
                    self.assertIsNotNone(fallback)
                    self.assertTrue(
                        any(word in fallback.lower() for word in reason_words),
                        fallback,
                    )

                    decisions = module.select_for_event(
                        normalized,
                        "changed",
                        [path],
                    )
                    self.assertEqual(
                        self.selected_names(decisions),
                        self.enabled_names(normalized),
                    )
                    for decision in decisions:
                        if decision["selected"]:
                            self.assertIn("fallback", decision["reason"].lower())

    def test_changed_event_selects_direct_and_transitive_dependents(self) -> None:
        expected_by_path = {
            "lib/core.py": {
                "always_check",
                "test_unit",
                "test_integration",
                "test_e2e",
                "changed_or_manual",
            },
            "src/app/main.py": {
                "always_check",
                "test_integration",
                "test_e2e",
                "changed_or_manual",
            },
            "src/frontend/view.py": {
                "always_check",
                "test_e2e",
            },
            "docs/guide/start.md": {
                "always_check",
                "docs_check",
            },
        }

        for module in self.modules:
            normalized = self.normalized_config(module)
            for path, expected in expected_by_path.items():
                with self.subTest(module=module.__name__, path=path):
                    decisions = module.select_for_event(
                        normalized,
                        "changed",
                        [path],
                    )
                    self.decision_map(decisions)
                    self.assertEqual(self.selected_names(decisions), expected)

    def test_source_loop_contract_changes_select_lint(self) -> None:
        module = self.modules[0]
        config = module.load_config(
            REPO_ROOT / ".project" / "verification.toml"
        )
        normalized = module.validate_config(config)

        for path in (".plans/TEMPLATE.md", ".project/conventions.md"):
            with self.subTest(path=path):
                decisions = module.select_for_event(
                    normalized,
                    "changed",
                    [path],
                )
                self.assertIn("lint", self.selected_names(decisions))

    def test_changed_selection_reasons_are_independent_of_path_order(self) -> None:
        paths = ["src/app/z.py", "src/app/a.py", "lib/core.py"]

        for module in self.modules:
            with self.subTest(module=module.__name__):
                normalized = self.normalized_config(module)
                forward = module.select_for_event(
                    normalized,
                    "changed",
                    paths,
                )
                reverse = module.select_for_event(
                    normalized,
                    "changed",
                    list(reversed(paths)),
                )
                self.assertEqual(forward, reverse)

    def test_full_scheduled_and_manual_events_apply_their_policies(self) -> None:
        expected = {
            "full": None,
            "scheduled": {"always_check", "scheduled_check"},
            "manual": {
                "always_check",
                "manual_check",
                "changed_or_manual",
            },
        }

        for module in self.modules:
            normalized = self.normalized_config(module)
            expected["full"] = self.enabled_names(normalized)
            for event, selected in expected.items():
                with self.subTest(module=module.__name__, event=event):
                    decisions = module.select_for_event(normalized, event)
                    self.decision_map(decisions)
                    self.assertEqual(self.selected_names(decisions), selected)

    def test_explicit_git_fallback_selects_all_eligible_phases(self) -> None:
        for module in self.modules:
            with self.subTest(module=module.__name__):
                normalized = self.normalized_config(module)
                decisions = module.select_for_event(
                    normalized,
                    "changed",
                    fallback_reason="Git merge base is unavailable",
                )
                self.assertEqual(
                    self.selected_names(decisions),
                    self.enabled_names(normalized),
                )
                for decision in decisions:
                    if decision["selected"]:
                        self.assertIn("git merge base", decision["reason"].lower())

    def test_empty_changed_set_is_deterministic_and_not_a_fallback(self) -> None:
        for module in self.modules:
            with self.subTest(module=module.__name__):
                normalized = self.normalized_config(module)
                decisions = module.select_for_event(
                    normalized,
                    "changed",
                    [],
                )
                mapped = self.decision_map(decisions)
                self.assertEqual(self.selected_names(decisions), {"always_check"})
                self.assertIn("no", mapped["test_unit"]["reason"].lower())

    def test_parse_args_supports_event_and_change_sources(self) -> None:
        for module in self.modules:
            with self.subTest(module=module.__name__, case="default"):
                args = module.parse_args([])
                self.assertEqual(args.event, "full")

            with self.subTest(module=module.__name__, case="explicit files"):
                args = module.parse_args(
                    [
                        "--event",
                        "changed",
                        "--changed-file",
                        "src/app/main.py",
                        "--changed-file",
                        "lib/core.py",
                        "--mode",
                        "ci",
                        "--only",
                        "lint",
                    ]
                )
                changed_files = getattr(
                    args,
                    "changed_files",
                    getattr(args, "changed_file", None),
                )
                self.assertEqual(
                    changed_files,
                    ["src/app/main.py", "lib/core.py"],
                )
                self.assertEqual(args.mode, "ci")
                self.assertEqual(args.only, ["lint"])

            with self.subTest(module=module.__name__, case="git range"):
                args = module.parse_args(
                    [
                        "--event",
                        "changed",
                        "--base",
                        "base-ref",
                        "--head",
                        "head-ref",
                    ]
                )
                self.assertEqual(args.base, "base-ref")
                self.assertEqual(args.head, "head-ref")

    def test_cli_prints_reasons_for_selected_and_omitted_phases(self) -> None:
        config = """\
version = 2

[selection]
selector_paths = []
global_paths = []

[inputs.app]
paths = ["src/**"]
depends_on = []

[inputs.docs]
paths = ["docs/**"]
depends_on = []

[phases.lint]
enabled = true
command = "true"
inputs = ["app"]
when = ["changed"]

[phases.test_unit]
enabled = true
command = "true"
inputs = ["docs"]
when = ["changed"]

[phases.always_check]
enabled = true
command = "true"
inputs = []
when = ["always"]
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_path = root / "verification.toml"
            config_path.write_text(config, encoding="utf-8")

            for module in self.modules:
                script_path = Path(module.__file__).resolve()
                with self.subTest(module=module.__name__):
                    completed = subprocess.run(
                        [
                            sys.executable,
                            str(script_path),
                            "--config",
                            "verification.toml",
                            "--event",
                            "changed",
                            "--changed-file",
                            "src/main.py",
                        ],
                        cwd=root,
                        check=False,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(completed.returncode, 0, completed.stderr)
                    self.assertRegex(
                        completed.stdout,
                        r"(?m)^\[verify\] selected: lint \(.+\)$",
                    )
                    self.assertRegex(
                        completed.stdout,
                        r"(?m)^\[verify\] skipped: test_unit \(.+\)$",
                    )
                    self.assertRegex(
                        completed.stdout,
                        r"(?m)^\[verify\] selected: always_check \(.+\)$",
                    )

    def test_cli_without_change_source_reports_full_fallback(self) -> None:
        config = """\
version = 2

[selection]
selector_paths = []
global_paths = []

[inputs.app]
paths = ["src/**"]
depends_on = []

[phases.lint]
enabled = true
command = "true"
inputs = ["app"]
when = ["changed"]
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "verification.toml").write_text(config, encoding="utf-8")

            for module in self.modules:
                script_path = Path(module.__file__).resolve()
                with self.subTest(module=module.__name__):
                    completed = subprocess.run(
                        [
                            sys.executable,
                            str(script_path),
                            "--config",
                            "verification.toml",
                            "--event",
                            "changed",
                        ],
                        cwd=root,
                        check=False,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(completed.returncode, 0, completed.stderr)
                    self.assertRegex(
                        completed.stdout.lower(),
                        r"(?m)^\[verify\] selected: lint \(full fallback: .+\)$",
                    )

    def test_git_adapter_reads_renames_and_unusual_paths_conservatively(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(
                ["git", "config", "user.email", "verify@example.com"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Verify Test"],
                cwd=root,
                check=True,
            )
            (root / "old name.txt").write_text("old\n", encoding="utf-8")
            (root / "modified.txt").write_text("before\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "base"],
                cwd=root,
                check=True,
            )
            base = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            (root / "old name.txt").rename(root / "new name.txt")
            (root / "modified.txt").write_text("after\n", encoding="utf-8")
            (root / "line\nbreak.txt").write_text("unusual\n", encoding="utf-8")
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "head"],
                cwd=root,
                check=True,
            )
            head = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            expected = {
                "old name.txt",
                "new name.txt",
                "modified.txt",
                "line\nbreak.txt",
            }
            for module in self.modules:
                with self.subTest(module=module.__name__):
                    changed, fallback = module.collect_changed_files(
                        root,
                        base,
                        head,
                    )
                    self.assertEqual(set(changed), expected)
                    self.assertIsNone(fallback)

    def test_git_adapter_returns_a_fallback_for_invalid_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)

            for module in self.modules:
                with self.subTest(module=module.__name__):
                    changed, fallback = module.collect_changed_files(
                        root,
                        "missing-base",
                        "missing-head",
                    )
                    self.assertEqual(changed, [])
                    self.assertIsInstance(fallback, str)
                    self.assertTrue(fallback)

    def test_source_and_public_modules_have_selection_parity(self) -> None:
        source, public = self.modules
        source_config = self.normalized_config(source)
        public_config = self.normalized_config(public)
        self.assertEqual(source_config["version"], public_config["version"])
        self.assertEqual(source_config["inputs"], public_config["inputs"])
        self.assertEqual(source_config["phases"], public_config["phases"])
        expected_selection = make_selection_config()["selection"]
        for name, patterns in expected_selection.items():
            self.assertEqual(
                [
                    pattern
                    for pattern in source_config["selection"][name]
                    if pattern in patterns
                ],
                patterns,
            )
            self.assertEqual(
                [
                    pattern
                    for pattern in public_config["selection"][name]
                    if pattern in patterns
                ],
                patterns,
            )

        cases = [
            ("full", None, None),
            ("changed", ["lib/core.py"], None),
            ("changed", ["notes/idea.txt"], None),
            ("changed", ["unknown.txt"], None),
            ("changed", None, "Git data unavailable"),
            ("scheduled", None, None),
            ("manual", None, None),
        ]
        for event, changed_paths, fallback in cases:
            with self.subTest(event=event, changed_paths=changed_paths):
                self.assertEqual(
                    source.select_for_event(
                        source_config,
                        event,
                        changed_paths,
                        fallback,
                    ),
                    public.select_for_event(
                        public_config,
                        event,
                        changed_paths,
                        fallback,
                    ),
                )


class VerifyHelperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_verify_module(
            "source_verify_helpers",
            REPO_ROOT / "scripts" / "verify.py",
        )

    def test_pinned_sha_re_matches_40_char_hex(self) -> None:
        self.assertIsNotNone(self.module.PINNED_SHA_RE.match("a" * 40))

    def test_pinned_sha_re_rejects_short_refs(self) -> None:
        self.assertIsNone(self.module.PINNED_SHA_RE.match("v4"))
        self.assertIsNone(self.module.PINNED_SHA_RE.match("abc123"))

    def test_action_ref_re_extracts_action_and_ref(self) -> None:
        match = self.module.ACTION_REF_RE.match(
            "      - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4"
        )

        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "actions/checkout")
        self.assertEqual(match.group(2), "34e114876b0b11c390a56381ad16ebd13914f8d5")

    def test_action_ref_re_ignores_local_actions(self) -> None:
        self.assertIsNone(
            self.module.ACTION_REF_RE.match("      - uses: ./.github/actions/local")
        )

    def test_workflow_has_read_permissions_detects_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "workflow.yml"
            path.write_text(
                "name: CI\n\npermissions:\n  contents: read\n",
                encoding="utf-8",
            )

            self.assertTrue(self.module.workflow_has_read_permissions(path))

    def test_workflow_has_read_permissions_rejects_missing_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "workflow.yml"
            path.write_text(
                "name: CI\n\njobs:\n  verify:\n    runs-on: ubuntu-latest\n",
                encoding="utf-8",
            )

            self.assertFalse(self.module.workflow_has_read_permissions(path))

    def test_ensure_files_identical_accepts_matching_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            left = root / "left.txt"
            right = root / "right.txt"
            left.write_text("same\n", encoding="utf-8")
            right.write_text("same\n", encoding="utf-8")

            self.module.ensure_files_identical([(left, right)], "test")

    def test_ensure_files_identical_rejects_different_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            left = root / "left.txt"
            right = root / "right.txt"
            left.write_text("left\n", encoding="utf-8")
            right.write_text("right\n", encoding="utf-8")

            original_source_root = self.module.SOURCE_ROOT
            self.module.SOURCE_ROOT = root
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        self.module.ensure_files_identical([(left, right)], "test")
                self.assertEqual(raised.exception.code, 2)
            finally:
                self.module.SOURCE_ROOT = original_source_root

    def test_agent_rule_sync_rejects_source_public_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_rule = root / "source-AGENTS.md"
            public_rule = root / "public-AGENTS.md"
            source_rule.write_text("source\n", encoding="utf-8")
            public_rule.write_text("public\n", encoding="utf-8")

            original_source_root = self.module.SOURCE_ROOT
            original_groups = self.module.AGENT_RULE_GROUPS
            original_pairs = self.module.AGENT_RULE_CROSS_SCOPE_PAIRS
            self.module.SOURCE_ROOT = root
            self.module.AGENT_RULE_GROUPS = []
            self.module.AGENT_RULE_CROSS_SCOPE_PAIRS = [(source_rule, public_rule)]
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        self.module.check_agent_rule_sync()
                self.assertEqual(raised.exception.code, 2)
            finally:
                self.module.SOURCE_ROOT = original_source_root
                self.module.AGENT_RULE_GROUPS = original_groups
                self.module.AGENT_RULE_CROSS_SCOPE_PAIRS = original_pairs

    def test_current_loop_policy_is_valid(self) -> None:
        self.module.check_loop_policy()

    def test_extract_markdown_section_rejects_missing_or_duplicate_heading(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "policy.md"

            for content in (
                "# Policy\n",
                "## Loop\n\nfirst\n\n## Loop\n\nsecond\n",
            ):
                with self.subTest(content=content):
                    path.write_text(content, encoding="utf-8")
                    with contextlib.redirect_stderr(io.StringIO()):
                        with self.assertRaises(SystemExit) as raised:
                            self.module.extract_markdown_section(path, "Loop")
                    self.assertEqual(raised.exception.code, 2)

    def test_extract_markdown_section_supports_section_at_eof(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "policy.md"
            path.write_text("# Policy\n\n## Loop\n\ncontent\n", encoding="utf-8")

            self.assertEqual(
                self.module.extract_markdown_section(path, "Loop"),
                "## Loop\n\ncontent\n",
            )

    def test_extract_markdown_section_ignores_headings_inside_fences(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "policy.md"

            for fence in ("```", "~~~"):
                with self.subTest(fence=fence):
                    path.write_text(
                        "# Policy\n\n"
                        "## Loop\n\n"
                        "before\n\n"
                        f"{fence}markdown\n"
                        "## Loop\n"
                        "## Example\n"
                        f"{fence}\n\n"
                        "after\n\n"
                        "## Next\n\n"
                        "outside\n",
                        encoding="utf-8",
                    )

                    self.assertEqual(
                        self.module.extract_markdown_section(path, "Loop"),
                        "## Loop\n\n"
                        "before\n\n"
                        f"{fence}markdown\n"
                        "## Loop\n"
                        "## Example\n"
                        f"{fence}\n\n"
                        "after\n\n",
                    )

    def test_markdown_section_sync_rejects_different_section_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            left = root / "left.md"
            right = root / "right.md"
            left.write_text("# Left\n\n## Loop\n\nleft\n", encoding="utf-8")
            right.write_text("# Right\n\n## Loop\n\nright\n", encoding="utf-8")

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    self.module.ensure_markdown_section_identical(
                        [left, right],
                        "Loop",
                        "test loop",
                    )
            self.assertEqual(raised.exception.code, 2)

    def test_text_anchor_check_rejects_missing_contract_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "policy.md"
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as raised:
                    self.module.ensure_text_anchors(
                        "portable core\n",
                        ["portable core", "authority boundary"],
                        path,
                        "test policy",
                    )

            self.assertEqual(raised.exception.code, 2)
            self.assertIn("authority boundary", stderr.getvalue())

    def test_loop_policy_rejects_source_public_plan_template_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_plan = root / "source-plan.md"
            public_plan = root / "public-plan.md"
            plan = (REPO_ROOT / ".plans" / "TEMPLATE.md").read_text(
                encoding="utf-8"
            )
            source_plan.write_text(plan, encoding="utf-8")
            public_plan.write_text(
                plan.replace("Criterion 1", "Different criterion", 1),
                encoding="utf-8",
            )

            original_source_root = self.module.SOURCE_ROOT
            self.module.SOURCE_ROOT = root
            try:
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    with self.assertRaises(SystemExit) as raised:
                        self.module.ensure_files_identical(
                            [(source_plan, public_plan)],
                            "source and public template plan state",
                        )
                self.assertEqual(raised.exception.code, 2)
                self.assertIn(
                    "source and public template plan state mismatch",
                    stderr.getvalue(),
                )
            finally:
                self.module.SOURCE_ROOT = original_source_root

    def test_loop_policy_rejects_missing_required_plan_heading(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "plan.md"
            incomplete_plan = "\n".join(
                f"## {heading}\n"
                for heading in self.module.LOOP_POLICY_REQUIRED_PLAN_SECTIONS
                if heading != "Loop State"
            )
            plan.write_text(incomplete_plan, encoding="utf-8")

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    self.module.ensure_markdown_sections(
                        plan,
                        self.module.LOOP_POLICY_REQUIRED_PLAN_SECTIONS,
                        "test plan",
                    )
            self.assertEqual(raised.exception.code, 2)

    def test_loop_policy_rejects_missing_required_plan_state_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "plan.md"
            content = (REPO_ROOT / ".plans" / "TEMPLATE.md").read_text(
                encoding="utf-8"
            )
            plan.write_text(
                content.replace("- Last material observation:\n", "", 1),
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    self.module.ensure_text_anchors(
                        plan.read_text(encoding="utf-8"),
                        self.module.LOOP_POLICY_REQUIRED_PLAN_ANCHORS,
                        plan,
                        "loop plan template",
                    )
            self.assertEqual(raised.exception.code, 2)

    def test_loop_policy_check_rejects_plan_drift_through_registered_wiring(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            agent = root / "AGENTS.md"
            convention = root / "conventions.md"
            source_plan = root / "source-plan.md"
            public_plan = root / "public-plan.md"
            agent.write_text(
                (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            convention.write_text(
                (REPO_ROOT / ".project" / "conventions.md").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            plan = (REPO_ROOT / ".plans" / "TEMPLATE.md").read_text(
                encoding="utf-8"
            )
            source_plan.write_text(plan, encoding="utf-8")
            public_plan.write_text(
                plan.replace("Criterion 1", "Different criterion", 1),
                encoding="utf-8",
            )

            originals = (
                self.module.SOURCE_ROOT,
                self.module.LOOP_POLICY_AGENT_FILES,
                self.module.LOOP_POLICY_CONVENTION_FILES,
                self.module.LOOP_POLICY_PLAN_TEMPLATES,
            )
            self.module.SOURCE_ROOT = root
            self.module.LOOP_POLICY_AGENT_FILES = [agent]
            self.module.LOOP_POLICY_CONVENTION_FILES = [convention]
            self.module.LOOP_POLICY_PLAN_TEMPLATES = [source_plan, public_plan]
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        self.module.check_loop_policy()
                self.assertEqual(raised.exception.code, 2)
            finally:
                (
                    self.module.SOURCE_ROOT,
                    self.module.LOOP_POLICY_AGENT_FILES,
                    self.module.LOOP_POLICY_CONVENTION_FILES,
                    self.module.LOOP_POLICY_PLAN_TEMPLATES,
                ) = originals

    def test_github_actions_check_rejects_missing_ci_selection_contract(self) -> None:
        current_workflow = (
            REPO_ROOT / ".github" / "workflows" / "ci.yml"
        ).read_text(encoding="utf-8")

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ci.yml"
            path.write_text(
                current_workflow.replace("          fetch-depth: 0\n", ""),
                encoding="utf-8",
            )

            original = self.module.CI_SELECTION_WORKFLOWS
            self.module.CI_SELECTION_WORKFLOWS = [path]
            try:
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    with self.assertRaises(SystemExit) as raised:
                        self.module.check_github_actions()
                self.assertEqual(raised.exception.code, 2)
                self.assertIn("fetch-depth: 0", stderr.getvalue())
            finally:
                self.module.CI_SELECTION_WORKFLOWS = original


class PublishWorkflowCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_verify_module(
            "source_verify_publish_workflow",
            REPO_ROOT / "scripts" / "verify.py",
        )
        cls.workflow = (
            REPO_ROOT / ".github" / "workflows" / "publish-template.yml"
        ).read_text(encoding="utf-8")

    @contextlib.contextmanager
    def publish_workflow(self, content: str):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "publish-template.yml"
            path.write_text(content, encoding="utf-8")

            original = self.module.PUBLISH_WORKFLOW
            self.module.PUBLISH_WORKFLOW = path
            try:
                yield
            finally:
                self.module.PUBLISH_WORKFLOW = original

    def assert_check_fails(self, content: str) -> str:
        stderr = io.StringIO()
        with self.publish_workflow(content):
            with contextlib.redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as raised:
                    self.module.check_publish_workflow()

        self.assertEqual(raised.exception.code, 2)
        return stderr.getvalue()

    def test_accepts_current_publish_workflow(self) -> None:
        with self.publish_workflow(self.workflow):
            self.module.check_publish_workflow()

    def test_accepts_updated_action_pins(self) -> None:
        updated = re.sub(r"@[0-9a-f]{40} # v\d+", f"@{'b' * 40} # v9", self.workflow)

        self.assertNotEqual(updated, self.workflow)
        with self.publish_workflow(updated):
            self.module.check_publish_workflow()

    def test_rejects_missing_required_action(self) -> None:
        without_app_token = "\n".join(
            line
            for line in self.workflow.splitlines()
            if "uses: actions/create-github-app-token@" not in line
        )

        message = self.assert_check_fails(without_app_token)
        self.assertIn("missing required actions", message)
        self.assertIn("actions/create-github-app-token", message)

    def test_rejects_missing_required_behavior(self) -> None:
        without_release = self.workflow.replace("gh release create", "true")

        message = self.assert_check_fails(without_release)
        self.assertIn("missing required content", message)
        self.assertIn("gh release create", message)

    def test_collect_action_names_ignores_unpinned_local_actions(self) -> None:
        content = "\n".join(
            [
                "      - uses: actions/checkout@" + "a" * 40,
                "      - uses: ./.github/actions/local",
                "        uses: actions/setup-python@" + "c" * 40,
            ]
        )

        self.assertEqual(
            self.module.collect_action_names(content),
            {"actions/checkout", "actions/setup-python"},
        )


if __name__ == "__main__":
    unittest.main()
