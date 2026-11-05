# 07 — AI channel

> Status: draft v0.2

How effective governance reaches an AI agent **without modifying base skills**,
**without custom tooling** and **without flooding its context**.

The AI agent itself does the work: it reads the instance files, filters what
applies, and runs the same linter the gates run. No CLI or server is built
for this.

## Three tiers

```text
  ┌───────────────────────────────────────────────────────────────────────┐
  │ Tier 1 — Pointer (always loaded, ~20 lines)                           │
  │   AGENTS.md section in each content repository:                       │
  │   where the governance instance is · which version · modes available ·│
  │   "resolve rules before acting · run the checker before finishing ·   │
  │    never decide rules"                                                │
  ├───────────────────────────────────────────────────────────────────────┤
  │ Tier 2 — Effective rules, read on demand by the mode skill            │
  │   the mode reads manifest.yml → rules/ → exceptions/ and keeps only   │
  │   rules whose scope matches the task; it uses ai_hint lines and opens │
  │   the ADR only when it needs the reasoning                            │
  ├───────────────────────────────────────────────────────────────────────┤
  │ Tier 3 — Hooks (optional, per assistant)                              │
  │   after file writes: run the checker on changed files                 │
  └───────────────────────────────────────────────────────────────────────┘
                 base skills (ai-forge, aap-skills) remain untouched
```

## Why this design

| Concern | Answer |
|---------|--------|
| Base skills cannot be modified | Rules arrive next to them (pointer + mode skill), never inside them |
| Context must stay small | The mode loads only rules matching the scope, as `ai_hint` lines |
| Agents may ignore instructions | Tier 3 automates checks where supported; gates catch the rest |
| No custom tooling | Instance files are plain YAML/Markdown the agent reads; the checker is ansible-lint |

## Assistant support

| Capability | How it is delivered |
|------------|---------------------|
| Mode skills and commands | Lola module `gac-modes` (Claude Code, Copilot, Cursor, Gemini CLI, OpenCode) |
| Pointer | `AGENTS.md` section, from [starter-kit/AGENTS.pointer.md](../../starter-kit/AGENTS.pointer.md) |
| Instance governance | Git: the agent reads a local checkout or submodule of the instance |
| Hooks | Not installed by Lola: `gac-setup` registers them from the manifest (Guardrails and Input slots). Implemented for Claude Code |

## What an agent does (example)

Request: *"create a playbook to configure firewall and sysctl on production nodes"*.

1. Pointer → governance instance `acme` at `governance/`.
2. Builder reads `governance/rules/`, keeps rules with `content: playbook` and
   `promotion_path: prod`:
   ```text
   R-COLL-001 (ADR-0005, L1, block): community.general forbidden in prod.
              Use ansible.posix, ansible.builtin or certified collections.
   R-CODE-001 (ADR-0001, L1, block): role loop variables use the __<role>_ prefix.
   (+ L0: CoP and ansible-lint production profile apply)
   ```
3. Builds through ai-forge skills, then runs the checker and fixes findings.

Three lines of organization rules instead of the whole governance.
