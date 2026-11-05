# Governance as Code

A **method** for governing how an organization develops Ansible content
(collections, roles, playbooks, plugins) and operates Ansible Automation
Platform — with or without AI assistants — under one set of rules.

This repository defines the method. It is **not** a product to install and it
does not contain any organization's rules. Each organization builds its own
**instance** by following the method.

## The problem

The community provides an excellent baseline:

| Base | What it gives you |
|------|-------------------|
| [Red Hat CoP Automation Good Practices](https://redhat-cop.github.io/automation-good-practices/) | Good practices for humans |
| [ansible-community/ai-forge](https://github.com/ansible-community/ai-forge) | AI skills and commands for developing Ansible content |
| [ansible/aap-skills](https://github.com/ansible/aap-skills) | AI skills for operating AAP through the AAP MCP Server |

None of them knows **your** naming conventions, your forbidden collections,
your playbook procedure or your approval flows. And new community tools that
change how AI agents work appear every week.

Governance as Code lets you **start from the community baseline and add your
own decisions on top**, without forking anything, and keep adding new pieces
without redesigning the whole thing.

## Start here

| I want to… | Mode | Command |
|------------|------|---------|
| Create a collection, role, playbook or plugin | Builder | `/build` |
| Modernize a role (`with_*` → `loop`, FQCN, deprecated modules) | Auditor → Builder | `/audit` then `/build` |
| Audit a repository or review a PR | Auditor | `/audit` |
| Add an organization rule or request an exception | Librarian | `/librarian` |
| Adopt a new tool into the harness | Librarian | `/librarian` |
| Onboard an organization that already has its own conventions | Librarian + Auditor | `/librarian`, `/audit` |
| Audit AAP access and health, or check a job | Auditor / Operator | `/audit`, `/operate` |

Full catalog: [docs/spec/02-use-cases.md](docs/spec/02-use-cases.md).

## Modes

Modes are how the method is used. They are **the same for every
organization**; what changes is the governance they consume
([GAC-0007](adr/GAC-0007-modes-are-common-orchestrators.md)).

| Mode ↓ / Target → | Content (Git) | Platform (live AAP) |
|---|---|---|
| **Auditor** | Review content, report debt | Review access, EEs, health |
| **Builder** | Create or modernize content | Controller objects as code *(later)* |
| **Operator** | — | Run jobs, check status *(read-only first)* |
| **Librarian** | Evolve governance: ADRs, rules, exceptions, slot adoptions | |

A mode owns the workflow and delegates Ansible knowledge to the community
bases (ai-forge, aap-skills). Details: [docs/spec/01-modes.md](docs/spec/01-modes.md).

## The model in one picture

```text
                       AUTHORITY (who decides)
     ┌──────────────────────────────────────────────────────┐
     │ L3 Project       exceptions only, with owner + expiry │
     │ L2 Domain        optional (business unit, platform)   │
     │ L1 Organization  ADRs → rules, red lines              │
     │ L0 Community     CoP · ai-forge · aap-skills · ...    │
     └──────────────────────────┬───────────────────────────┘
                                │ resolved by precedence
                                ▼
                     EFFECTIVE GOVERNANCE (per project)
                                │
              consumed by MODES: Auditor · Builder · Librarian · Operator
                                │
        ┌───────────────────────┴────────────────────────┐
        ▼                                                ▼
  HARNESS (how the AI agent works)              GATES (what proves it)
  organized in SLOTS:                           pre-commit · CI · EE build
  Knowledge · Capabilities · Integrations       Hub publish · AAP runtime
  Input · Output · Guardrails · Execution
  Evolution                                     ← the guarantee
  ← the guidance
```

- **Layers** answer *who decides*. Higher layers override lower ones.
- **Modes** answer *how it is used*.
- **Slots** answer *what is governed* in the AI agent's harness. Every new
  tool plugs into an existing slot.
- **Gates** answer *what proves compliance*. They do not depend on the AI.

## Core principles

1. **Community bases are consumed, never forked.** ([GAC-0002](adr/GAC-0002-consume-bases-never-fork.md))
2. **The organization layer contains only the delta.** ([GAC-0003](adr/GAC-0003-organization-layer-is-a-delta.md))
3. **Authority and enforcement are separate concerns.** ([GAC-0001](adr/GAC-0001-separate-authority-from-enforcement.md))
4. **Every rule has a single source.** ([GAC-0004](adr/GAC-0004-single-source-for-rules.md))
5. **The harness is extended through slots.** ([GAC-0005](adr/GAC-0005-harness-slots.md))
6. **Gates are the guarantee; the AI channel is guidance.** ([GAC-0006](adr/GAC-0006-gates-are-the-guarantee.md))
7. **Modes are common; governance is data.** ([GAC-0007](adr/GAC-0007-modes-are-common-orchestrators.md)) Process requirements are organization rules scoped by repository classification, not work profiles ([GAC-0009](adr/GAC-0009-no-work-profiles.md)).
8. **Define success before acting.** A human approves what will count as success before the Builder builds; tests run where they are written. ([GAC-0010](adr/GAC-0010-define-success-before-acting.md))
9. **AI never decides rules.** It applies them and may propose changes that a
   human approves.

## Read next

| Document | Purpose |
|----------|---------|
| [docs/spec/](docs/spec/README.md) | How the method is used and implemented: modes, use cases, roles, rules, gates, AI channel, starter kit, instance, evolution, examples |
| [docs/concepts/](docs/concepts/) | The model: layers, slots, precedence, rule lifecycle |
| [docs/glossary.md](docs/glossary.md) | Terms used across the method |
| [adr/](adr/README.md) | Decisions about the method itself |
| [starter-kit/SETUP.md](starter-kit/SETUP.md) | **One-time setup**: applies and verifies the instance's harness slots in your assistant |
| [slots/](slots/README.md) | Catalog of the 8 harness slots |
| [starter-kit/](starter-kit/gac-modes/README.md) | The `gac-modes` Lola module, pointer and gate definitions |
| [docs/validation/](docs/validation/dogfooding-2026-11-05/README.md) | Clean-session tests of `/audit` and `/build` |
| [presentation/](presentation/README.md) | Animated walkthrough for technical and executive audiences (open `flow.html`) |
| [examples/](examples/README.md) | Reference instance `acme` and worked examples |
| [templates/](templates/README.md) | Index of the templates used by the modes |

## Repository layout

```text
governance-as-code/
├── README.md
├── docs/
│   ├── concepts/      # layers, slots, precedence, rule lifecycle
│   ├── spec/          # modes, use cases, roles, rules, gates, ...
│   └── glossary.md
├── adr/               # method ADRs (GAC-*) — never organization rules
├── slots/             # catalog of the 8 harness slots: admission, mechanism, verification
├── starter-kit/
│   ├── gac-modes/     # Lola module: modes, commands, templates
│   ├── hooks/         # guardrail hook (checker after every edit)
│   ├── gates/         # pre-commit and CI definitions (ansible-lint)
│   └── AGENTS.pointer.md
├── templates/         # index of the templates shipped inside the skills
├── presentation/      # animated walkthrough (FlowStory), demo script
└── examples/
    ├── acme/          # reference governance instance
    └── ex-01-.../     # worked example: modernize ansible-manage-users
```

**See it working:** [examples/ex-01-modernize-ansible-manage-users](examples/ex-01-modernize-ansible-manage-users/)
— a 2017 role taken from 60 checker findings to 0 and verified idempotent.

## Status

Version 0.1 — first full draft of concepts and specification. Everything is
open for review and may change through method ADRs.
