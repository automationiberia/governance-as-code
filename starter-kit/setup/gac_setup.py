#!/usr/bin/env python3
"""Governance as Code — apply and verify the instance's harness slots in a repository.

Called by gac-setup.sh with the tool virtualenv's Python. Reads the instance
manifest and, for every slot entry, applies it (required entries always,
recommended entries only with --with-recommended) and verifies it.

Mechanisms:
  reference       knowledge the agent reads: check the referenced bases/paths exist
  lola-module     skills/commands installed with Lola in the assistant's format
  mcp-server      MCP server registered in the assistant's project config
  hook            assistant hook in the project settings (+ pinned binary if any)
  test-platform   container runtime and image for tests are available
  instance-check  a check of the instance itself runs and passes

Hooks are implemented for Claude Code (and the method's checker hook for Cursor);
MCP registration for Claude Code; other assistants
get lola-module entries and a "not supported yet" note for the rest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import yaml

METHOD_ROOT = Path(__file__).resolve().parents[2]
SLOTS = ["knowledge", "capabilities", "integrations", "input", "output", "guardrails", "execution", "evolution"]


@dataclass
class Result:
    slot: str
    entry: str
    status: str
    mechanism: str
    outcome: str  # applied+verified | verified | skipped | failed | not-supported
    note: str = ""


class Setup:
    def __init__(self, args: argparse.Namespace) -> None:
        self.instance: Path = args.instance
        self.repo: Path = args.repo
        self.assistant: str = args.assistant
        self.scope: str = args.scope
        self.cache: Path = args.cache
        self.with_recommended: bool = args.with_recommended
        self.manifest = yaml.safe_load((self.instance / "manifest.yml").read_text(encoding="utf-8"))
        self.bases = {b["id"]: b for b in self.manifest.get("bases", [])}
        self.venv_bin = Path(sys.executable).parent
        self.lola = shutil.which("lola", path=str(self.venv_bin)) or shutil.which("lola") or "lola"
        self.results: list[Result] = []

    # ------------------------------------------------------------------ helpers
    def run(self, cmd: list[str], **kw) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, capture_output=True, text=True, check=False, **kw)

    def checkout(self, base_id: str) -> Path:
        base = self.bases[base_id]
        target = self.cache / "bases" / f"{base_id}-{base['ref']}"
        if not (target / ".git").is_dir():
            target.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "clone", "-q", base["source"], str(target)], check=True)
            subprocess.run(["git", "-C", str(target), "checkout", "-q", base["ref"]], check=True)
        return target

    def rel_instance(self) -> str:
        try:
            return os.path.relpath(self.instance, self.repo)
        except ValueError:
            return str(self.instance)

    def claude_settings(self) -> tuple[Path, dict]:
        path = self.repo / ".claude" / "settings.json"
        data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
        return path, data

    def add_env(self, env: dict) -> None:
        if not env:
            return
        path, data = self.claude_settings()
        data.setdefault("env", {}).update({k: str(v) for k, v in env.items()})
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def add_hook(self, event: str, matcher: str, command: str) -> None:
        path, data = self.claude_settings()
        groups = data.setdefault("hooks", {}).setdefault(event, [])
        for group in groups:
            if group.get("matcher") == matcher and any(h.get("command") == command for h in group.get("hooks", [])):
                return
        groups.append({"matcher": matcher, "hooks": [{"type": "command", "command": command}]})
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    # --------------------------------------------------------------- mechanisms
    def m_reference(self, e: dict) -> tuple[str, str]:
        missing = [b for b in e.get("bases", []) if b not in self.bases]
        missing += [p for p in e.get("paths", []) if not (self.instance / p).exists()]
        missing += [p for p in e.get("method_paths", []) if not (METHOD_ROOT / p).exists()]
        if missing:
            return "failed", f"missing: {', '.join(missing)}"
        what = e.get("bases", []) + e.get("paths", []) + [Path(p).name for p in e.get("method_paths", [])]
        return "verified", f"referenced: {', '.join(what)}"

    def m_lola_module(self, e: dict) -> tuple[str, str]:
        if e.get("source") == "method":
            sources = [(e["id"], METHOD_ROOT / e["path"])]
        else:
            root = self.checkout(e["base"])
            sources = [(m if m != "." else e["id"], root / m) for m in e.get("modules", ["."])]
        installed = []
        extra = ["--module-content", e["module_content"]] if e.get("module_content") else []
        for name, path in sources:
            added = self.run([self.lola, "mod", "add", str(path), "--name", name, *extra], input="y\n")
            proc = self.run([self.lola, "install", name, str(self.repo), "-a", self.assistant, "-s", self.scope, "-f"])
            summary = next((ln.strip() for ln in proc.stdout.splitlines() if f"{self.assistant} (" in ln), "")
            if proc.returncode != 0 or not summary:
                detail = (added.stdout + added.stderr + proc.stdout + proc.stderr).strip().splitlines()
                return "failed", f"lola {name}: {detail[-1] if detail else 'no output'}"
            installed.append(f"{name} [{summary.split('(', 1)[-1].rstrip(')')}]")
        # "Installed without error" is not "installed the right thing": check the expected skills.
        expected = e.get("expect_skills", [])
        if expected and self.assistant == "claude-code" and self.scope == "project":
            missing = [s for s in expected if not (self.repo / ".claude" / "skills" / s / "SKILL.md").is_file()]
            if missing:
                return "failed", f"installed, but expected skills missing: {', '.join(missing)}"
        return "applied+verified", "; ".join(installed) + (f" — {len(expected)} expected skills present" if expected else "")

    def m_mcp_server(self, e: dict) -> tuple[str, str]:
        if self.assistant != "claude-code" or self.scope != "project":
            return "not-supported", f"MCP registration for {self.assistant}/{self.scope} not implemented"
        cfg = e["config"]
        path = self.repo / ".mcp.json"
        data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
        server = {"type": cfg.get("transport", "http"), "url": cfg["url"]}
        if cfg.get("headers"):
            server["headers"] = cfg["headers"]
        data.setdefault("mcpServers", {})[cfg["name"]] = server
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        check = json.loads(path.read_text(encoding="utf-8"))["mcpServers"].get(cfg["name"]) == server
        note = f"{cfg['name']} → {cfg['url']}"
        reachable = os.environ.get(cfg.get("url_env", ""), "")
        note += "; connectivity not checked (no endpoint configured)" if not reachable else ""
        return ("applied+verified" if check else "failed"), note

    def install_binary(self, base_id: str) -> Path:
        base = self.bases[base_id]
        art = base["artifacts"]["linux-x86_64"]
        target = self.cache / "bin" / f"{base_id}-{base['ref']}"
        binary = target / base.get("binary", base_id)
        if binary.is_file():
            return binary
        target.mkdir(parents=True, exist_ok=True)
        archive = target / Path(art["url"]).name
        urllib.request.urlretrieve(art["url"], archive)  # noqa: S310 — pinned URL, checksum verified below
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        if digest != art["sha256"]:
            archive.unlink()
            raise RuntimeError(f"checksum mismatch for {archive.name}")
        with tarfile.open(archive) as tar:
            tar.extractall(target, filter="data")
        archive.unlink()
        return binary

    def add_cursor_hook(self, event: str, matcher: str, command: str) -> None:
        """Register a hook in <repo>/.cursor/hooks.json (Cursor's project hooks, version 1)."""
        path = self.repo / ".cursor" / "hooks.json"
        data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
        data.setdefault("version", 1)
        entries = data.setdefault("hooks", {}).setdefault(event, [])
        if not any(h.get("command") == command for h in entries):
            entries.append({"command": command, "matcher": matcher, "timeout": 240})
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def m_hook(self, e: dict) -> tuple[str, str]:
        cfg = e["config"]
        cursor = self.assistant == "cursor" and self.scope == "project" and not e.get("base")
        if (self.assistant != "claude-code" and not cursor) or self.scope != "project":
            return "not-supported", f"hooks for {self.assistant}/{self.scope} not implemented"
        if e.get("base"):  # hook provided by a pinned binary (e.g. rtk)
            binary = self.install_binary(e["base"])
            command = f"{binary} {cfg['args']}"
            self.add_hook(cfg["event"], cfg["matcher"], command)
            self.add_env(cfg.get("env", {}))
            probe = self.run([str(binary), *cfg["args"].split()], cwd=self.repo,
                             input=json.dumps({"hook_event_name": cfg["event"], "tool_name": "Bash",
                                               "tool_input": {"command": cfg["probe"]["command"]}}))
            ok = cfg["probe"]["expect"] in probe.stdout
            return ("applied+verified" if ok else "failed"), f"{cfg['event']}:{cfg['matcher']} → {binary.name}; probe '{cfg['probe']['command']}' {'rewritten' if ok else 'NOT rewritten'}"
        # hook provided by the method (checker on edit)
        hooks_dir = self.repo / (".cursor" if cursor else ".claude") / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        script = hooks_dir / Path(cfg["script"]).name
        shutil.copy2(METHOD_ROOT / cfg["script"], script)
        checker = self.manifest["gates"]["checker"]
        inst = self.rel_instance()
        hook_cfg = {
            "ansible_lint": str(self.venv_bin / "ansible-lint"),
            "config": f"{inst}/{checker['config']}",
            "ignore_file": f"{inst}/{checker['ignore_file']}" if checker.get("ignore_file") else None,
            "collections_path": str(self.cache / "collections"),
            "offline": True,
        }
        (hooks_dir / "gac-hook.json").write_text(json.dumps(hook_cfg, indent=2) + "\n", encoding="utf-8")
        if cursor:
            event, matcher = cfg.get("cursor_event", "postToolUse"), cfg.get("cursor_matcher", "Write")
            self.add_cursor_hook(event, matcher, f'{sys.executable} "{script}"')
            payload = {"hook_event_name": event, "cursor_version": "probe", "workspace_roots": [str(self.repo)],
                       "tool_input": {"file_path": str(self.repo / "README.md")}}
            env = dict(os.environ, CURSOR_PROJECT_DIR=str(self.repo))
        else:
            event, matcher = cfg["event"], cfg["matcher"]
            self.add_hook(event, matcher, f'{sys.executable} "$CLAUDE_PROJECT_DIR/.claude/hooks/{script.name}"')
            payload = {"tool_input": {"file_path": str(self.repo / "README.md")}}
            env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.repo))
        probe = self.run([sys.executable, str(script)], input=json.dumps(payload), env=env)
        ok = probe.returncode == 0
        return ("applied+verified" if ok else "failed"), f"{event}:{matcher} → {script.name}"

    def m_test_platform(self, e: dict) -> tuple[str, str]:
        tp = self.manifest.get("test_platform", {})
        runtime = tp.get("runtime", "podman")
        if not shutil.which(runtime):
            return "failed", f"{runtime} not found — tests will be 'written, not run'"
        image = tp["default"]["image"]
        if self.run([runtime, "image", "exists", image]).returncode != 0:
            pull = self.run([runtime, "pull", "-q", image])
            if pull.returncode != 0:
                return "failed", f"cannot pull {image}"
        return "verified", f"{runtime} available; {image} present"

    def m_instance_check(self, e: dict) -> tuple[str, str]:
        cmd = [sys.executable if part == "python" else part for part in e["config"]["command"].split()]
        proc = self.run(cmd, cwd=self.instance)
        last = (proc.stdout.strip().splitlines() or [""])[-1]
        return ("verified" if proc.returncode == 0 else "failed"), last

    # ------------------------------------------------------------------- driver
    def apply(self) -> int:
        handlers = {"reference": self.m_reference, "lola-module": self.m_lola_module, "mcp-server": self.m_mcp_server,
                    "hook": self.m_hook, "test-platform": self.m_test_platform, "instance-check": self.m_instance_check}
        for slot in SLOTS:
            for e in self.manifest.get("slots", {}).get(slot) or []:
                status, mech = e.get("status", "required"), e.get("mechanism", "reference")
                if status == "recommended" and not self.with_recommended:
                    self.results.append(Result(slot, e["id"], status, mech, "skipped", "recommended — use --with-recommended"))
                    continue
                try:
                    outcome, note = handlers[mech](e)
                except Exception as exc:  # report and continue with the other slots
                    outcome, note = "failed", str(exc)[:200]
                self.results.append(Result(slot, e["id"], status, mech, outcome, note))
        self.claude_import_agents()
        self.report()
        return 1 if any(r.outcome == "failed" and r.status == "required" for r in self.results) else 0

    def claude_import_agents(self) -> None:
        # The pointer lives in AGENTS.md; Claude Code loads CLAUDE.md, so import it there.
        if self.assistant != "claude-code" or self.scope != "project" or not (self.repo / "AGENTS.md").is_file():
            return
        claude_md = self.repo / "CLAUDE.md"
        text = claude_md.read_text(encoding="utf-8") if claude_md.is_file() else ""
        if "@AGENTS.md" not in text.splitlines():
            claude_md.write_text("@AGENTS.md\n\n" + text, encoding="utf-8")

    def report(self) -> None:
        print(f"\nHarness slots — {self.manifest['instance']} → {self.repo} ({self.assistant}, {self.scope} scope)\n")
        print(f"{'slot':13} {'entry':26} {'status':12} {'mechanism':15} {'outcome':17} note")
        print("-" * 120)
        for r in self.results:
            print(f"{r.slot:13} {r.entry:26} {r.status:12} {r.mechanism:15} {r.outcome:17} {r.note}")
        covered = {r.slot for r in self.results if r.outcome in ("applied+verified", "verified")}
        print(f"\nSlots active: {len(covered)}/8  ({', '.join(s for s in SLOTS if s in covered)})")


def main() -> int:
    p = argparse.ArgumentParser(description="Apply and verify harness slots")
    p.add_argument("--instance", type=lambda s: Path(s).resolve(), required=True)
    p.add_argument("--repo", type=lambda s: Path(s).resolve(), required=True)
    p.add_argument("--assistant", default="claude-code")
    p.add_argument("--scope", default="project", choices=["project", "user"])
    p.add_argument("--cache", type=lambda s: Path(s).resolve(), required=True)
    p.add_argument("--with-recommended", action="store_true")
    return Setup(p.parse_args()).apply()


if __name__ == "__main__":
    sys.exit(main())
