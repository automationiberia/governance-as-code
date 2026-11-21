# Setup — once per machine, once per repository

Everything here is done **once**, not per use case. After it, every use case
works from the assistant (`/audit`, `/build`, `/librarian`, `/operate`).

| What | When | How |
|------|------|-----|
| Tools: checker, test runner, Lola | Once per machine | `gac-setup.sh` creates a virtualenv with [environment/requirements.txt](environment/requirements.txt) and the collections in [environment/requirements.yml](environment/requirements.yml) |
| The harness: modes, community modules, MCP servers, hooks, test platform, instance checks | Once per repository | `gac-setup.sh` applies and verifies every slot entry of the instance manifest ([slot catalog](../slots/README.md)): `required` always, `recommended` with `--with-recommended` |
| Pointer to the governance instance | Once per repository | `AGENTS.md` section from [AGENTS.pointer.md](AGENTS.pointer.md) |
| Again | When the instance changes the pinned versions, when `gac-modes` changes, or when you switch assistant | Re-run `gac-setup.sh` (idempotent) |

## Requirements

- Python 3.13 or later, Git, Bash.
- podman — only for use cases that run idempotency tests in containers.
- An AI assistant supported by Lola: Claude Code, Copilot (CLI or VS Code), Cursor, Gemini CLI, OpenCode.

## Steps

```bash
# 1. Content repository layout (recommended): the governance instance as a submodule
cd <content-repo>
git submodule add <instance-repo-url> governance        # or any path; the pointer says where

# 2. Pointer — copy starter-kit/AGENTS.pointer.md into AGENTS.md and fill in
#    the instance name, path and version

# 3. Tools + modules for your assistant
<method-checkout>/starter-kit/setup/gac-setup.sh --instance governance --repo . --assistant claude-code

# 4. In every shell where you work (printed by the script)
export PATH="$HOME/.cache/gac/venv/bin:$PATH"
export ANSIBLE_COLLECTIONS_PATH="$HOME/.cache/gac/collections"
```

Then open the repository in your assistant and run, for example, `/audit roles/<role>`.

## What the script does

1. Creates or updates the virtualenv with the pinned tools (skip with `--no-tools`).
2. Reads the instance `manifest.yml` → `slots` and, for each entry, applies its
   mechanism and verifies it:

   | Mechanism | Applies | Verifies |
   |-----------|---------|----------|
   | `reference` | — | the referenced bases and paths exist |
   | `lola-module` | checks out the pinned base, registers and installs it with Lola | the expected skills are installed |
   | `mcp-server` | registers the server in `.mcp.json` (credentials from environment variables) | registration; connectivity only if an endpoint is set |
   | `hook` | downloads a pinned binary (checksum) or copies the method's hook; registers it in `.claude/settings.json` | a probe through the hook |
   | `test-platform` | pulls the declared image | runtime and image available |
   | `instance-check` | — | the check runs and passes |

3. For Claude Code, imports `AGENTS.md` from `CLAUDE.md` (`@AGENTS.md`), so the
   pointer is always loaded.
4. Prints a table: slot, entry, status, mechanism, outcome — and how many of the
   eight slots are active. A failed `required` entry makes the script fail.

## Why a script and not only `.lola-req`

Verified with Lola 0.7.0:

| Need | Lola 0.7 |
|------|----------|
| Pin a community module to a commit | Not supported in `.lola-req` or marketplace URLs |
| Several modules from the same Git repository | `.lola-req` names them all after the repository; only the first installs |
| Relative paths (repository cloned anywhere) | Not supported in `.lola-req` or marketplaces |
| Local folder with an absolute path | ✅ — what the script uses |

If Lola adds commit pinning, the script reduces to a `.lola-req` file.

## Notes

- Interactive use: the assistant asks before running commands. Unattended
  sessions (e.g. `claude -p`) need an allowlist; agents often run compound
  shell commands and `VAR=value cmd` forms that simple patterns do not match
  ([dogfooding](../docs/validation/dogfooding-2026-11-05/README.md)).
- Idempotency tests in containers need podman on the machine; the Molecule
  podman driver (`molecule-plugins[podman]`) is in the tool environment.
- The ai-forge instructions add several hundred lines to `CLAUDE.md`
  (`ansible-collection-sdlc` alone ~340). An organization that wants a smaller
  context enables only the modules it uses in `manifest.yml` `bases[].modules`.
- Generated files are per person: `.claude/settings.json` and
  `.claude/hooks/gac-hook.json` contain absolute paths of the local tool
  environment — do not commit them; each person runs the script. `.mcp.json`
  uses environment variables and can be shared.
- The guardrail hook (checker on every edit) is implemented for Claude Code
  (`.claude/settings.json`, PostToolUse) and Cursor (`.cursor/hooks.json`,
  postToolUse: findings return as `additional_context`). Binary hooks such as
  rtk and MCP registration are Claude Code only; for other assistants the script
  installs the Lola modules and reports the rest as "not supported yet".
