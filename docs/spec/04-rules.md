# 05 — Rules

> Status: draft v0.1

A rule is the single, machine-readable form of an organization decision
([GAC-0004](../../adr/GAC-0004-single-source-for-rules.md)).

## Registry entry

See [rule.yml](../../starter-kit/gac-modes/module/skills/gac-librarian/templates/rule.yml). Required fields:

| Field | Purpose |
|-------|---------|
| `id` | `R-<AREA>-NNN` |
| `adr` | Accepted ADR that produced it |
| `layer` | `organization` or `domain` |
| `statement` | One sentence a reviewer can apply |
| `scope` | Content types, promotion paths and, optionally, other repository classification attributes (e.g. `criticality`) it applies to |
| `verifiability` | `mechanical` · `heuristic` · `process` |
| `enforcement` | `advise` · `warn` · `block` |
| `block_from` | Date `warn` becomes `block` |
| `locked` | Red line: lower layers cannot relax it |
| `owner` | Grants exceptions when locked |
| `acts_on` | Relation to L0: `add` · `replace` · `tighten` · `disable` + target |
| `ai_hint` | One or two lines for agents, including the compliant alternative |
| `check` | Gate check id (mechanical rules) |

## Areas

| Area | Covers | Example |
|------|--------|---------|
| `NAME` | Naming of roles, variables, files, AAP objects | Internal variables use `_` prefix |
| `COLL` | Collections and dependencies | `community.general` forbidden in prod |
| `STRUCT` | Repository and content layout | Platform tasks under `tasks/platforms/` |
| `CODE` | Coding style beyond L0 | No `command`/`shell` without justification comment |
| `SEC` | Security | No plain-text secrets; vault required |
| `TEST` | Testing requirements | Production roles have an idempotency test |
| `DOC` | Documentation | Roles declare `meta/argument_specs.yml` |
| `EE` | Execution environments | Only approved base images |
| `PLAT` | AAP objects | Job template naming; approved EEs only |
| `PROC` | Process | Changes to repositories with `criticality: high` need CAB approval |

## L0 references

Organization rules refer to community items with a prefix:

| Prefix | Source | Example |
|--------|--------|---------|
| `cop:` | CoP good practices section | `cop:roles/variable-prefix` |
| `lint:` | ansible-lint rule | `lint:fqcn` |
| `ai-forge:` | ai-forge module or skill | `ai-forge:ansible-collection-sdlc` |
| `aap-skills:` | aap-skills skill | `aap-skills:aap-effective-access-review` |

ansible-lint's built-in rules are part of L0. Which ansible-lint profile the organization
uses (`basic`, `production`, ...) and which rules it disables are L1
decisions.

## Writing good rules

- Write the ADR's **Examples** (must pass / must fail) first; for mechanical
  rules they become fixtures, and the rule is done when they pass
  ([GAC-0010](../../adr/GAC-0010-define-success-before-acting.md)).
- One rule, one check. Split compound rules.
- The statement says *what*; the ADR says *why*.
- Every `ai_hint` names the compliant alternative, not only the prohibition.
- If it cannot be checked mechanically, say so (`heuristic` / `process`);
  never pretend a gate covers it.
- Prefer `tighten` or `add` over `replace`; replacing L0 makes upgrades harder.
