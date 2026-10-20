"""Tests for optout_cli.py. Run: python3 -m unittest -v test_optout_cli (from scripts/)."""
import json
import tempfile
import tomllib
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import optout_cli as oc


def run(home: Path, *args: str) -> int:
    with redirect_stdout(StringIO()):
        return oc.main(["--home", str(home), *args])


class OptoutTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_skips_missing_tools(self):
        self.assertEqual(run(self.home), 0)
        self.assertFalse((self.home / ".claude").exists())
        self.assertFalse((self.home / ".codex").exists())

    def test_claude_merges_and_preserves(self):
        d = self.home / ".claude"
        d.mkdir()
        (d / "settings.json").write_text(json.dumps({"model": "opus", "env": {"FOO": "bar", "DISABLE_TELEMETRY": "yes"}}))
        self.assertEqual(run(self.home, "--only", "claude"), 0)
        data = json.loads((d / "settings.json").read_text())
        self.assertEqual(data["model"], "opus")
        self.assertEqual(data["env"]["FOO"], "bar")
        self.assertEqual(data["env"]["DISABLE_TELEMETRY"], "yes")  # existing non-empty value kept
        self.assertEqual(data["env"]["DISABLE_FEEDBACK_COMMAND"], "1")
        self.assertEqual(data["feedbackSurveyRate"], 0)
        self.assertNotIn("CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC", data["env"])
        self.assertEqual(len(list(d.glob("settings.json.bak-optout-*"))), 1)

    def test_claude_strict(self):
        (self.home / ".claude").mkdir()
        run(self.home, "--only", "claude", "--strict")
        data = json.loads((self.home / ".claude" / "settings.json").read_text())
        self.assertEqual(data["env"]["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"], "1")

    def test_invalid_json_left_untouched(self):
        d = self.home / ".claude"
        d.mkdir()
        bad = '{ "env": { // comment\n } }'
        (d / "settings.json").write_text(bad)
        self.assertEqual(run(self.home, "--only", "claude"), 1)
        self.assertEqual((d / "settings.json").read_text(), bad)

    def test_dry_run_writes_nothing(self):
        (self.home / ".claude").mkdir()
        (self.home / ".codex").mkdir()
        run(self.home, "--dry-run")
        self.assertFalse((self.home / ".claude" / "settings.json").exists())
        self.assertFalse((self.home / ".codex" / "config.toml").exists())

    def test_codex_preserves_comments_and_updates(self):
        d = self.home / ".codex"
        d.mkdir()
        original = (
            '# my config\nmodel = "gpt-5"\n\n[analytics]\nenabled = true  # was on\n\n'
            '[mcp_servers.x]\ncommand = "foo"\n'
        )
        (d / "config.toml").write_text(original)
        self.assertEqual(run(self.home, "--only", "codex"), 0)
        text = (d / "config.toml").read_text()
        self.assertIn("# my config", text)
        cfg = tomllib.loads(text)
        self.assertEqual(cfg["model"], "gpt-5")
        self.assertEqual(cfg["mcp_servers"]["x"]["command"], "foo")
        self.assertIs(cfg["analytics"]["enabled"], False)
        self.assertIs(cfg["feedback"]["enabled"], False)
        self.assertEqual(cfg["otel"]["metrics_exporter"], "none")
        self.assertIs(cfg["otel"]["log_user_prompt"], False)

    def test_codex_inline_table_refused(self):
        d = self.home / ".codex"
        d.mkdir()
        original = "analytics = { enabled = true }\n"
        (d / "config.toml").write_text(original)
        self.assertEqual(run(self.home, "--only", "codex"), 1)
        self.assertEqual((d / "config.toml").read_text(), original)

    def test_idempotent(self):
        for name in (".claude", ".codex", ".gemini", ".codebuddy", ".kimi-code", ".kimi"):
            (self.home / name).mkdir()
        run(self.home)
        snap = {p: p.read_text() for p in self.home.rglob("*") if p.is_file() and "bak-optout" not in p.name}
        baks = len(list(self.home.rglob("*.bak-optout-*")))
        run(self.home)
        self.assertEqual(snap, {p: p.read_text() for p in snap})
        self.assertEqual(baks, len(list(self.home.rglob("*.bak-optout-*"))))  # no new backups

    def test_gemini_and_codebuddy(self):
        (self.home / ".gemini").mkdir()
        (self.home / ".gemini" / "settings.json").write_text(json.dumps({"theme": "dark", "usageStatisticsEnabled": True}))
        (self.home / ".codebuddy").mkdir()
        run(self.home, "--only", "gemini", "codebuddy")
        g = json.loads((self.home / ".gemini" / "settings.json").read_text())
        self.assertEqual(g["theme"], "dark")
        self.assertIs(g["privacy"]["usageStatisticsEnabled"], False)
        self.assertIs(g["usageStatisticsEnabled"], False)
        env = (self.home / ".config" / "llm-optout" / "env.sh").read_text()
        self.assertIn("export CODEBUDDY_ARTIFACT_ENABLED=0", env)

    def test_kimi_toplevel_keys_and_legacy(self):
        kc = self.home / ".kimi-code"
        kc.mkdir()
        (kc / "config.toml").write_text('# kimi\ndefault_model = "k2"\ntelemetry = true\n\n[providers.x]\ntelemetry = "nested-untouched"\n')
        legacy = self.home / ".kimi"
        legacy.mkdir()
        self.assertEqual(run(self.home, "--only", "kimi"), 0)
        cfg = tomllib.loads((kc / "config.toml").read_text())
        self.assertIs(cfg["telemetry"], False)
        self.assertEqual(cfg["default_model"], "k2")
        self.assertEqual(cfg["providers"]["x"]["telemetry"], "nested-untouched")
        self.assertIn("# kimi", (kc / "config.toml").read_text())
        self.assertIs(tomllib.loads((kc / "tui.toml").read_text())["disable_feedback_survey"], True)
        self.assertIs(tomllib.loads((legacy / "config.toml").read_text())["telemetry"], False)
        self.assertIn("export KIMI_DISABLE_TELEMETRY=1", (self.home / ".config" / "llm-optout" / "env.sh").read_text())

    def test_kimi_appends_before_first_table(self):
        kc = self.home / ".kimi-code"
        kc.mkdir()
        (kc / "config.toml").write_text('[providers.x]\nkey = "v"\n')
        run(self.home, "--only", "kimi")
        cfg = tomllib.loads((kc / "config.toml").read_text())
        self.assertIs(cfg["telemetry"], False)  # top level, not inside [providers.x]
        self.assertNotIn("telemetry", cfg["providers"]["x"])

    def test_kimi_skipped_when_absent(self):
        with redirect_stdout(StringIO()) as out:
            oc.main(["--home", str(self.home)])
        self.assertIn("kimi", out.getvalue())
        self.assertFalse((self.home / ".kimi-code").exists())

    def test_muse_env_only_never_touches_settings_json(self):
        muse_dir = self.home / ".config" / "muse"
        muse_dir.mkdir(parents=True)
        original = '{"model": "muse-spark-1.2"}\n'
        (muse_dir / "settings.json").write_text(original)
        self.assertEqual(run(self.home), 0)
        env = (self.home / ".config" / "llm-optout" / "env.sh").read_text()
        self.assertIn("export TBH_DISABLE_TELEMETRY=1", env)
        self.assertIn("export TBH_DISABLE_FEATURE_CONFIG=1", env)
        self.assertEqual((muse_dir / "settings.json").read_text(), original)
        self.assertEqual(list(muse_dir.glob("*.bak-optout-*")), [])

    def test_env_file_merges_tools_and_keeps_user_exports(self):
        (self.home / ".codebuddy").mkdir()
        envf = self.home / ".config" / "llm-optout" / "env.sh"
        envf.parent.mkdir(parents=True)
        envf.write_text("export MY_VAR=keep\n")
        run(self.home, "--only", "codebuddy")
        run(self.home, "--only", "dsh")  # naming a tool in --only applies it even if not detected
        env = envf.read_text()
        self.assertIn("export MY_VAR=keep", env)
        self.assertIn("export CODEBUDDY_ARTIFACT_ENABLED=0", env)
        self.assertIn("export DSH_TELEMETRY_DISABLED=1", env)
        before = env
        run(self.home, "--only", "codebuddy", "dsh")
        self.assertEqual(before, envf.read_text())


if __name__ == "__main__":
    unittest.main()
