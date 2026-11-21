# Live demo — an AI assistant working under your rules

An automation team has been asked to modernize a role written in 2017,
[silvinux/ansible-manage-users](https://github.com/silvinux/ansible-manage-users).
The company already has a governance: its decisions, rules and exceptions live
in a git repository. The team clones the role, connects the governance, and its
AI assistant works under it.

- 🖥️ **Terminal**: the IDE terminal
- 💬 **AI chat**: the IDE's AI assistant chat, in a **new chat**

---

## Part 1 · Get the role, connect the governance

### 1.1 · Clone the role

🖥️ **Terminal**

```bash
git clone https://github.com/silvinux/ansible-manage-users .
```

### 1.2 · Add the company governance

🖥️ **Terminal**

```bash
git submodule add git@github.com:automationiberia/governance-as-code.git governance
cp governance/examples/acme/AGENTS.pointer.md AGENTS.md
```

**Watch:** the governance as a pinned submodule; the ACME instance in
`governance/examples/acme`: decisions (ADRs), rules, exceptions, repository map.

### 1.3 · Install the harness

🖥️ **Terminal**

```bash
governance/starter-kit/setup/gac-setup.sh --instance governance/examples/acme --repo .
cp ../demo-settings.json .claude/settings.local.json
```

**Watch:** every entry of the manifest pinned, applied and verified: community
skills, the company modes, the guardrail hook, the test platform, the exception
watch. `Slots active: 6/8`.

### 1.4 · What changed

🖥️ **Terminal**

```bash
git status --short
```

**Watch:** the submodule and `AGENTS.md` to commit; the assistant's skills,
commands and hook installed locally.

---

## Part 2 · Audit the role

### 2.1 · Audit

💬 **AI chat** (new chat)

```text
/audit this role
```

**Watch:** the mode declared · the company rules found on its own · every
finding cites its rule and decision (ADR) · it changes nothing and asks before building.

### 2.2 · The guardrail: the AI writes something forbidden

💬 **AI chat** (new chat)

```text
This is a test of the guardrail. Write tasks/sudoers.yml with exactly this content, then fix it the way the governance requires:

- name: Allow the admins group to use sudo
  community.general.sudoers:
    name: admins
    group: admins
    commands: ALL
```

**Watch:** right after the write, the governance answers (rule **R-COLL-001**,
decision **ADR-0005**), and the AI fixes its own code before anything reaches CI.

---

## Part 3 · Modernize the role

### 3.1 · Build: success agreed first

💬 **AI chat** (new chat)

```text
/build Modernize this role so it complies with the company governance. Keep its behaviour. Keep it minimal: one Molecule scenario.
```

**Watch:** production read from the repository map · a **success contract**:
what stays, what changes · it stops and waits for a person.

### 3.2 · Approve

💬 **AI chat** (same chat)

```text
Approved. Write the Molecule scenario but don't run it; CI runs it.
```

**Watch:** the role rewritten under the company rules · the checker loop until
0 findings · the test written and declared as not run here.

### 3.3 · The gate, without any AI

🖥️ **Terminal**

```bash
ansible-lint -c governance/examples/acme/gates/ansible-lint.yml -i governance/examples/acme/gates/ansible-lint-ignore.txt
```

**Watch:** the same check CI runs on every pull request. No AI involved.

---

<details>
<summary>Before the demo</summary>

From the root of `governance-as-code`, with no IDE window or terminal inside
`demo/workspaces/`. Network and SSH access to GitHub are needed.

```bash
demo/reset.sh --machine                     # once per laptop: tools, collections, pinned bases
demo/reset.sh                               # every rehearsal: an empty demo/workspaces/ansible-manage-users
code demo/workspaces/ansible-manage-users   # or: cursor demo/workspaces/ansible-manage-users
```

In that IDE window, open this file (`demo/README.md`) and a terminal, then:

```bash
source ../../env.sh                         # must print: tools: ok
```

| File | Purpose |
|------|---------|
| `reset.sh` | Empties `workspaces/` and creates the empty `ansible-manage-users` folder plus `demo-settings.json`. `--machine` warms `~/.cache/gac` |
| `env.sh` | Terminal preparation: the pinned tools on `PATH` |
| `permissions.json` | Source of `demo-settings.json` (step 1.3): the commands Claude Code may run without asking (`git commit`/`push` denied). `reset.sh` adds the pinned tools to its `env`: the IDE chat does not inherit the terminal environment |
| `fallback/checker.sh` | Plan B without AI, deterministic: `legacy`, `modernized`, `guardrail`, `collections` |
| `rehearsal/run.sh` | Headless rehearsal of the whole demo with Claude Code, reset to reset, timed per step; outputs in `rehearsal/` (not committed) |

The submodule pins the commit of `governance-as-code` on GitHub: the demo uses
what is pushed. Without network, use a local clone:
`git -c protocol.file.allow=always submodule add <path to a governance-as-code clone> governance`.

The IDE opens on the demo folder because an IDE's AI chat works on the folder
the window has open, and the commands, skills, guardrail and permissions are
installed there.

| AI assistant | Modes and skills | Guardrail on every edit | Slots |
|--------------|------------------|-------------------------|-------|
| Claude Code (VS Code or Cursor) | ✅ | ✅ | 6/8 |
| Cursor chat: `gac-setup.sh … --assistant cursor`, no `cp` | ✅ (`.cursor/commands`, `.cursor/skills`, `.cursor/rules`) | not implemented yet: the CI gate still blocks | 5/8 |

</details>
