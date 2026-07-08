from __future__ import annotations

import importlib.util
import contextlib
import io
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


if __name__ == "__main__":
    unittest.main()
