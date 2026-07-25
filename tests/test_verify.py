from __future__ import annotations

import importlib.util
import contextlib
import io
import re
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
