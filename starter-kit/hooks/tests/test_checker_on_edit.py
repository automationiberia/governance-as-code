"""Tests for the Guardrails hook: run the checker after the agent edits a file.

The hook receives Claude Code's PostToolUse JSON on stdin. It must:
- ignore files that are not Ansible content (exit 0, silent);
- ignore the governance instance and assistant directories;
- report only the findings of the edited file, on stderr, with exit 2
  (Claude Code shows stderr to the agent), so context stays small;
- stay silent with exit 0 when the edited file is clean.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOOK = HERE.parent / "gac_checker_on_edit.py"
METHOD = HERE.parents[2]
ACME_CONFIG = METHOD / "examples" / "acme" / "gates" / "ansible-lint.yml"
ANSIBLE_LINT = shutil.which("ansible-lint") or str(Path(sys.executable).parent / "ansible-lint")

SPECS = "---\nargument_specs:\n  main:\n    short_description: Demo\n    options: {}\n"
CLEAN = "---\n- name: Say hello\n  ansible.builtin.debug:\n    msg: hello\n"
FORBIDDEN = "---\n- name: Allow SSH\n  community.general.ufw:\n    rule: allow\n    port: \"22\"\n"


def make_repo(tasks: str) -> Path:
    root = Path(tempfile.mkdtemp()) / "linux_baseline"  # prod in the acme manifest
    (root / "roles/demo/tasks").mkdir(parents=True)
    (root / "roles/demo/meta").mkdir(parents=True)
    (root / "roles/demo/meta/argument_specs.yml").write_text(SPECS)
    (root / "roles/demo/tasks/main.yml").write_text(tasks)
    (root / "README.md").write_text("# demo\n")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    (root / ".claude/hooks").mkdir(parents=True)
    (root / ".claude/hooks/gac-hook.json").write_text(json.dumps({
        "ansible_lint": ANSIBLE_LINT,
        "config": str(ACME_CONFIG),
        "offline": True,
    }))
    return root


def run_hook(root: Path, file_path: str, tool: str = "Edit") -> subprocess.CompletedProcess:
    payload = {"hook_event_name": "PostToolUse", "tool_name": tool, "cwd": str(root),
               "tool_input": {"file_path": str(root / file_path)}}
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(root))
    env.pop("GAC_REPOSITORY", None)
    return subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload), capture_output=True,
                          text=True, env=env, check=False, timeout=300)


def test_non_ansible_file_is_ignored() -> None:
    root = make_repo(CLEAN)
    proc = run_hook(root, "README.md")
    assert proc.returncode == 0 and proc.stderr == ""


def test_clean_yaml_is_silent() -> None:
    root = make_repo(CLEAN)
    proc = run_hook(root, "roles/demo/tasks/main.yml")
    assert proc.returncode == 0, proc.stderr
    assert proc.stderr == ""


def test_violation_in_edited_file_is_reported_to_the_agent() -> None:
    root = make_repo(FORBIDDEN)
    proc = run_hook(root, "roles/demo/tasks/main.yml", tool="Write")
    assert proc.returncode == 2
    assert "R-COLL-001" in proc.stderr
    assert "roles/demo/tasks/main.yml" in proc.stderr


def test_findings_in_other_files_are_not_reported() -> None:
    root = make_repo(FORBIDDEN)
    (root / "roles/demo/defaults").mkdir()
    (root / "roles/demo/defaults/main.yml").write_text("---\ndemo_value: 1\n")
    proc = run_hook(root, "roles/demo/defaults/main.yml")
    assert proc.returncode == 0, proc.stderr


def test_governance_instance_is_ignored() -> None:
    root = make_repo(CLEAN)
    (root / "governance").mkdir()
    (root / "governance/rules.yml").write_text("---\n- id: x\n")
    proc = run_hook(root, "governance/rules.yml")
    assert proc.returncode == 0 and proc.stderr == ""
