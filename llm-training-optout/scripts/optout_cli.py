#!/usr/bin/env python3
"""Turn off telemetry / feedback / data-sharing in local AI coding-agent configs.

Targets (user-level config only):
  claude     ~/.claude/settings.json        (Claude Code)
  codex      ~/.codex/config.toml           (Codex CLI, IDE extension, ChatGPT desktop)
  gemini     ~/.gemini/settings.json        (Gemini CLI)
  kimi       ~/.kimi-code/{config,tui}.toml (Kimi Code CLI/Desktop/VS Code) + legacy ~/.kimi/config.toml
  codebuddy  env file to source             (CodeBuddy Code CLI; no config-file keys documented)
  dsh        env file to source             (DeepSeek Harness feedback telemetry)
  muse       env file to source             (Meta Muse Code telemetry; undocumented vars)

Model-TRAINING opt-outs for these tools are account settings on the provider's
servers; this script cannot change them. See ../providers/*.md.

Safety: every file is backed up to <file>.bak-optout-<timestamp> before writing,
edits are idempotent, unrelated keys are preserved, and a file that fails to parse
is left untouched. Standard library only (Python >= 3.11 for tomllib).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
import tomllib
from pathlib import Path

# ---------------------------------------------------------------------------
# Desired settings (sources: code.claude.com/docs env-vars & settings;
# developers.openai.com/codex/config-reference; gemini-cli docs; codebuddy.ai/docs/cli/env-vars)
# ---------------------------------------------------------------------------
CLAUDE_ENV = {
    "DISABLE_TELEMETRY": "1",
    "DISABLE_ERROR_REPORTING": "1",
    "DISABLE_FEEDBACK_COMMAND": "1",
    "CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY": "1",
}
CLAUDE_ENV_STRICT = {"CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"}  # also disables auto-update
CLAUDE_KEYS = {"feedbackSurveyRate": 0}

CODEX_TABLES = {
    "analytics": {"enabled": False},
    "feedback": {"enabled": False},
    "otel": {
        "exporter": "none",
        "trace_exporter": "none",
        "metrics_exporter": "none",
        "log_user_prompt": False,
    },
}

GEMINI_NESTED = {
    "privacy": {"usageStatisticsEnabled": False},
    "telemetry": {"enabled": False, "logPrompts": False},
}

CODEBUDDY_ENV = {
    "DISABLE_TELEMETRY": "1",
    "DISABLE_ERROR_REPORTING": "1",
    "DISABLE_FEEDBACK_COMMAND": "1",
    "CODEBUDDY_ARTIFACT_ENABLED": "0",
}

# Kimi Code: top-level keys (not inside a [table]); legacy kimi-cli uses the same key.
KIMI_CONFIG = {"telemetry": False}
KIMI_TUI = {"disable_feedback_survey": True}
KIMI_ENV = {"KIMI_DISABLE_TELEMETRY": "1"}

# DeepSeek Harness feedback telemetry (any non-empty value disables). Session-log
# upload is a UI/plugin setting, not an env var.
DSH_ENV = {"DSH_TELEMETRY_DISABLED": "1"}

# Meta Muse Code: undocumented internal vars taken from Meta's own SDK test harness
# (github.com/meta-models/muse-code-sdk @22a8a56). Telemetry only; training is the
# /settings "Contributor mode" toggle or the model ID. settings.json keys are unpublished,
# so that file is never edited.
MUSE_ENV = {"TBH_DISABLE_TELEMETRY": "1", "TBH_DISABLE_FEATURE_CONFIG": "1"}

STAMP = time.strftime("%Y%m%d%H%M%S")


class Result:
    def __init__(self, tool: str, path: Path):
        self.tool, self.path = tool, path
        self.status = "unchanged"  # unchanged | changed | would-change | skipped | error
        self.changes: list[str] = []
        self.note = ""

    def line(self) -> str:
        detail = "; ".join(self.changes) if self.changes else ""
        extra = f" ({self.note})" if self.note else ""
        return f"[{self.status:>12}] {self.tool:<9} {self.path}{extra}" + (f"\n               {detail}" if detail else "")


def backup_and_write(path: Path, text: str) -> None:
    if path.exists():
        shutil.copy2(path, path.with_name(f"{path.name}.bak-optout-{STAMP}"))
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp-optout")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8")
    if not raw.strip():
        return {}
    data = json.loads(raw)  # raises on invalid / commented JSON -> caller reports error
    if not isinstance(data, dict):
        raise ValueError("top-level JSON is not an object")
    return data


# ---------------------------------------------------------------------------
# Claude Code
# ---------------------------------------------------------------------------
def do_claude(home: Path, mode: str, create: bool, strict: bool) -> Result:
    path = home / ".claude" / "settings.json"
    r = Result("claude", path)
    if not (home / ".claude").is_dir() and not create:
        r.status, r.note = "skipped", "~/.claude not found (use --create)"
        return r
    try:
        data = load_json(path)
    except Exception as e:  # noqa: BLE001
        r.status, r.note = "error", f"cannot parse, left untouched: {e}"
        return r
    env = data.get("env")
    if env is not None and not isinstance(env, dict):
        r.status, r.note = "error", '"env" is not an object, left untouched'
        return r
    env = dict(env or {})
    want = dict(CLAUDE_ENV, **(CLAUDE_ENV_STRICT if strict else {}))
    for k, v in want.items():
        cur = env.get(k)
        # Claude Code treats any non-empty value as "disable" for these vars.
        if cur is None or str(cur) == "":
            r.changes.append(f"env.{k}: {cur!r} -> {v!r}")
            env[k] = v
    for k, v in CLAUDE_KEYS.items():
        if data.get(k) != v:
            r.changes.append(f"{k}: {data.get(k)!r} -> {v!r}")
            data[k] = v
    data["env"] = env
    return finish(r, mode, path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Codex (TOML): text-level edit so comments/formatting are preserved, then
# re-parsed with tomllib to verify before writing.
# ---------------------------------------------------------------------------
def toml_value(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    return json.dumps(v)  # JSON string escaping is valid TOML basic-string escaping


HEADER_RE = re.compile(r"^\s*\[\s*([A-Za-z0-9_.\-\"]+)\s*\]\s*(#.*)?$")


def edit_codex_text(text: str, current: dict, r: Result) -> str:
    lines = text.splitlines()
    for table, kv in CODEX_TABLES.items():
        cur_tbl = current.get(table, {})
        if not isinstance(cur_tbl, dict):
            raise ValueError(f"'{table}' is not a table")
        todo = {k: v for k, v in kv.items() if cur_tbl.get(k) != v}
        if not todo:
            continue
        # locate [table] section
        start = next((i for i, ln in enumerate(lines) if (m := HEADER_RE.match(ln)) and m.group(1) == table), None)
        if start is None:
            # inline table or dotted top-level keys -> too risky to rewrite automatically
            if re.search(rf"^\s*{re.escape(table)}\s*=", text, re.M) or re.search(rf"^\s*{re.escape(table)}\.", text, re.M):
                raise ValueError(f"'{table}' is defined inline/dotted; edit it manually")
            if lines and lines[-1].strip():
                lines.append("")
            lines.append(f"[{table}]")
            for k, v in todo.items():
                lines.append(f"{k} = {toml_value(v)}")
                r.changes.append(f"{table}.{k}: {cur_tbl.get(k)!r} -> {v!r}")
            continue
        end = next((i for i in range(start + 1, len(lines)) if lines[i].lstrip().startswith("[")), len(lines))
        for k, v in todo.items():
            key_re = re.compile(rf"^\s*{re.escape(k)}\s*=")
            idx = next((i for i in range(start + 1, end) if key_re.match(lines[i])), None)
            new = f"{k} = {toml_value(v)}"
            if idx is None:
                lines.insert(end, new)
                end += 1
            else:
                lines[idx] = new
            r.changes.append(f"{table}.{k}: {cur_tbl.get(k)!r} -> {v!r}")
    return "\n".join(lines) + "\n"


def set_toplevel_toml(path: Path, want: dict, r: Result) -> str | None:
    """Return new text with top-level keys set (before the first [table]), or None if unchanged.
    Raises on parse/verification failure so the caller can leave the file untouched."""
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    current = tomllib.loads(text)
    lines = text.splitlines()
    first_tbl = next((i for i, ln in enumerate(lines) if ln.lstrip().startswith("[")), len(lines))
    changed = False
    for k, v in want.items():
        if current.get(k) == v:
            continue
        if k in current and not isinstance(current[k], (bool, int, float, str)):
            raise ValueError(f"'{k}' is not a scalar; edit it manually")
        key_re = re.compile(rf"^\s*{re.escape(k)}\s*=")
        idx = next((i for i in range(first_tbl) if key_re.match(lines[i])), None)
        new = f"{k} = {toml_value(v)}"
        if idx is None:
            lines.insert(first_tbl, new)
            first_tbl += 1
        else:
            lines[idx] = new
        r.changes.append(f"{path.name}:{k}: {current.get(k)!r} -> {v!r}")
        changed = True
    if not changed:
        return None
    new_text = "\n".join(lines) + "\n"
    parsed = tomllib.loads(new_text)
    for k, v in want.items():
        if parsed.get(k) != v:
            raise ValueError(f"verification failed for {k}")
    return new_text


def do_codex(home: Path, mode: str, create: bool, strict: bool) -> Result:
    path = home / ".codex" / "config.toml"
    r = Result("codex", path)
    if not (home / ".codex").is_dir() and not create:
        r.status, r.note = "skipped", "~/.codex not found (use --create)"
        return r
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    try:
        current = tomllib.loads(text)
        new_text = edit_codex_text(text, current, r)
        parsed = tomllib.loads(new_text)
        for table, kv in CODEX_TABLES.items():
            for k, v in kv.items():
                if parsed.get(table, {}).get(k) != v:
                    raise ValueError(f"verification failed for {table}.{k}")
    except Exception as e:  # noqa: BLE001
        r.changes = []
        r.status, r.note = "error", f"left untouched: {e}"
        return r
    return finish(r, mode, path, new_text)


# ---------------------------------------------------------------------------
# Gemini CLI
# ---------------------------------------------------------------------------
def do_gemini(home: Path, mode: str, create: bool, strict: bool) -> Result:
    path = home / ".gemini" / "settings.json"
    r = Result("gemini", path)
    if not (home / ".gemini").is_dir() and not create:
        r.status, r.note = "skipped", "~/.gemini not found (use --create)"
        return r
    try:
        data = load_json(path)
    except Exception as e:  # noqa: BLE001
        r.status, r.note = "error", f"cannot parse (comments?), left untouched: {e}"
        return r
    for section, kv in GEMINI_NESTED.items():
        sec = data.get(section)
        if sec is not None and not isinstance(sec, dict):
            r.status, r.note = "error", f'"{section}" is not an object, left untouched'
            r.changes = []
            return r
        sec = dict(sec or {})
        for k, v in kv.items():
            if sec.get(k) != v:
                r.changes.append(f"{section}.{k}: {sec.get(k)!r} -> {v!r}")
                sec[k] = v
        data[section] = sec
    # legacy flat key from pre-v2 settings schema
    if data.get("usageStatisticsEnabled") is True:
        r.changes.append("usageStatisticsEnabled (legacy): True -> False")
        data["usageStatisticsEnabled"] = False
    return finish(r, mode, path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Env-var-only tools (CodeBuddy Code, DeepSeek Harness): merged into one shell
# file the user sources. Existing exports in that file are preserved.
# ---------------------------------------------------------------------------
EXPORT_RE = re.compile(r"^export ([A-Za-z_][A-Za-z0-9_]*)=(.*)$")


def env_file(home: Path) -> Path:
    return home / ".config" / "llm-optout" / "env.sh"


def merge_env(r: Result, home: Path, mode: str, want: dict[str, str]) -> Result:
    path = env_file(home)
    current: dict[str, str] = {}
    if path.exists():
        for ln in path.read_text(encoding="utf-8").splitlines():
            if m := EXPORT_RE.match(ln.strip()):
                current[m.group(1)] = m.group(2)
    for k, v in want.items():
        if current.get(k) != v:
            r.changes.append(f"export {k}: {current.get(k)!r} -> {v!r}")
            current[k] = v
    if r.changes:
        r.note = f"add '. {path}' to your shell profile"
    body = "# Generated by llm-training-optout. Source from your shell profile:\n"
    body += f"#   . {path}\n"
    body += "".join(f"export {k}={v}\n" for k, v in current.items())
    return finish(r, mode, path, body)


def do_codebuddy(home: Path, mode: str, create: bool, strict: bool) -> Result:
    r = Result("codebuddy", env_file(home))
    if not (home / ".codebuddy").is_dir() and not create:
        r.status, r.note = "skipped", "~/.codebuddy not found (use --create)"
        return r
    return merge_env(r, home, mode, CODEBUDDY_ENV)


def do_dsh(home: Path, mode: str, create: bool, strict: bool) -> Result:
    # Harness usually runs via `npx @deepseek-ai/dsh`, so there is no reliable
    # install marker; apply only when `dsh` is on PATH or --create/--only dsh is given.
    r = Result("dsh", env_file(home))
    if shutil.which("dsh") is None and not create:
        r.status, r.note = "skipped", "dsh not on PATH (use --only dsh or --create if you run it via npx)"
        return r
    r = merge_env(r, home, mode, DSH_ENV)
    r.note = (r.note + "; " if r.note else "") + \
        "also turn off Settings > General > 'Upload Session Log…' in the Harness UI"
    return r


# ---------------------------------------------------------------------------
# Kimi Code (~/.kimi-code, or $KIMI_CODE_HOME) and legacy kimi-cli (~/.kimi)
# ---------------------------------------------------------------------------
def _toml_file(tool: str, path: Path, want: dict, mode: str) -> Result:
    r = Result(tool, path)
    try:
        new_text = set_toplevel_toml(path, want, r)
    except Exception as e:  # noqa: BLE001
        r.changes = []
        r.status, r.note = "error", f"left untouched: {e}"
        return r
    return finish(r, mode, path, new_text or "")


def do_kimi(home: Path, mode: str, create: bool, strict: bool) -> list[Result]:
    # Honour KIMI_CODE_HOME only for the real home dir, so tests using --home stay hermetic.
    root = Path(os.environ["KIMI_CODE_HOME"]) if os.environ.get("KIMI_CODE_HOME") and home == Path.home() \
        else home / ".kimi-code"
    legacy = home / ".kimi"
    out: list[Result] = []
    if root.is_dir() or create:
        out.append(_toml_file("kimi", root / "config.toml", KIMI_CONFIG, mode))
        out.append(_toml_file("kimi", root / "tui.toml", KIMI_TUI, mode))
        out.append(merge_env(Result("kimi", env_file(home)), home, mode, KIMI_ENV))
    if legacy.is_dir():
        out.append(_toml_file("kimi-cli", legacy / "config.toml", KIMI_CONFIG, mode))
    if not out:
        r = Result("kimi", root)
        r.status, r.note = "skipped", f"{root} not found (use --create)"
        out.append(r)
    return out


def do_muse(home: Path, mode: str, create: bool, strict: bool) -> Result:
    r = Result("muse", env_file(home))
    if not (home / ".config" / "muse").is_dir() and shutil.which("muse") is None and not create:
        r.status, r.note = "skipped", "~/.config/muse not found and muse not on PATH (use --create)"
        return r
    r = merge_env(r, home, mode, MUSE_ENV)
    r.note = (r.note + "; " if r.note else "") + \
        "undocumented vars; also run `muse` -> /settings -> Contributor mode OFF (needs >= 1.4.8)"
    return r


def finish(r: Result, mode: str, path: Path, new_text: str) -> Result:
    if not r.changes:
        r.status = "unchanged"
    elif mode == "apply":
        backup_and_write(path, new_text)
        r.status = "changed"
    else:
        r.status = "would-change"
    return r


TOOLS = {"claude": do_claude, "codex": do_codex, "gemini": do_gemini, "kimi": do_kimi,
         "codebuddy": do_codebuddy, "dsh": do_dsh, "muse": do_muse}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", help="show planned changes, write nothing")
    g.add_argument("--check", action="store_true", help="report current state only (same as --dry-run)")
    p.add_argument("--only", nargs="+", choices=sorted(TOOLS), help="limit to these tools")
    p.add_argument("--create", action="store_true",
                   help="create configs for tools not yet detected (implied for tools named in --only)")
    p.add_argument("--strict", action="store_true",
                   help="also set CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC (disables Claude Code auto-update)")
    p.add_argument("--home", type=Path, default=Path.home(), help=argparse.SUPPRESS)  # for tests
    a = p.parse_args(argv)

    mode = "dry" if (a.dry_run or a.check) else "apply"
    # Naming a tool in --only counts as asking for it even if it isn't detected.
    results: list[Result] = []
    for t in (a.only or TOOLS):
        res = TOOLS[t](a.home, mode, a.create or bool(a.only), a.strict)
        results.extend(res if isinstance(res, list) else [res])
    for res in results:
        print(res.line())
    print("\nReminder: these are telemetry/feedback settings. Model-training opt-outs are account "
          "settings (see providers/*.md).")
    return 1 if any(res.status == "error" for res in results) else 0


if __name__ == "__main__":
    sys.exit(main())
