#!/usr/bin/env python3
"""Guardrails hook: run the governance checker after the agent edits a file.

One script, two assistants. Reads the hook JSON on stdin; when the edited file
is Ansible content, runs the checker from the repository root (same command as
pre-commit and CI) and reports only the findings of the edited file, so the
agent fixes them before going on. Silent otherwise.

- Claude Code, PostToolUse (matcher Edit|Write|MultiEdit): findings on stderr,
  exit code 2 — Claude Code shows them to the agent.
- Cursor, postToolUse (matcher Write): findings as {"additional_context": ...}
  on stdout, exit 0 — Cursor injects them into the conversation.

Configuration: gac-hook.json next to the script (.claude/hooks/ or
.cursor/hooks/), written by gac-setup:
  {"ansible_lint": "/path/to/ansible-lint", "config": "governance/gates/ansible-lint.yml",
   "ignore_file": "...", "collections_path": "...", "offline": true}

Guidance, not proof: the CI gate still decides (GAC-0006).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

CONTENT_SUFFIXES = {".yml", ".yaml", ".j2"}
SKIP_DIRS = {"governance", ".claude", ".lola", ".git", ".ansible", ".cursor", ".github"}
MAX_LINES = 20


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    cursor = "cursor_version" in payload or payload.get("hook_event_name") == "postToolUse"
    tool_input = payload.get("tool_input") or {}
    file_path = next((tool_input[k] for k in ("file_path", "path", "target_file") if tool_input.get(k)), None)
    if not file_path:
        return 0
    roots = payload.get("workspace_roots") or []
    root = Path(
        os.environ.get("CLAUDE_PROJECT_DIR") or os.environ.get("CURSOR_PROJECT_DIR")
        or (roots[0] if roots else None) or payload.get("cwd") or "."
    ).resolve()
    edited = Path(file_path)
    edited = (edited if edited.is_absolute() else root / edited).resolve()
    try:
        rel = edited.relative_to(root)
    except ValueError:
        return 0
    if edited.suffix not in CONTENT_SUFFIXES or (rel.parts and rel.parts[0] in SKIP_DIRS):
        return 0

    candidates = (Path(__file__).resolve().parent, root / ".claude" / "hooks", root / ".cursor" / "hooks")
    cfg_file = next((d / "gac-hook.json" for d in candidates if (d / "gac-hook.json").is_file()), None)
    if cfg_file is None:
        return 0
    cfg = json.loads(cfg_file.read_text(encoding="utf-8"))
    config = Path(cfg["config"])
    config = config if config.is_absolute() else root / config
    cmd = [cfg.get("ansible_lint", "ansible-lint"), "-c", str(config), "-f", "pep8", "--nocolor"]
    if cfg.get("ignore_file"):
        ignore = Path(cfg["ignore_file"])
        cmd += ["-i", str(ignore if ignore.is_absolute() else root / ignore)]
    if cfg.get("offline", True):
        cmd.append("--offline")

    env = dict(os.environ)
    env.setdefault("GAC_REPOSITORY", root.name)
    if cfg.get("collections_path"):
        env["ANSIBLE_COLLECTIONS_PATH"] = cfg["collections_path"]
    proc = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, check=False, timeout=240)

    prefix = f"{rel.as_posix()}:"
    findings = [line for line in proc.stdout.splitlines() if line.startswith(prefix)]
    if not findings:
        return 0
    shown = findings[:MAX_LINES]
    more = f"\n… and {len(findings) - MAX_LINES} more" if len(findings) > MAX_LINES else ""
    message = (
        f"Governance checker: {len(findings)} finding(s) in {rel.as_posix()} "
        "(rule ids starting with R- come from the organization's ADRs):\n"
        + "\n".join(shown) + more
        + "\nFix them before continuing, or propose an exception with /librarian."
    )
    if cursor:
        print(json.dumps({"additional_context": message}))
        return 0
    print(message, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
