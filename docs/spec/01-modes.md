# 01 — Modes

> Status: draft v0.1

Modes are **how people use the method**. Layers and slots are how it is built
inside. Modes are **common to every organization**; what changes per
organization is the governance they consume ([GAC-0007](../../adr/GAC-0007-modes-are-common-orchestrators.md)).

## Modes and targets

A **mode** is what you do. A **target** is what you do it on
([GAC-0008](../../adr/GAC-0008-modes-and-targets.md)).

| Mode ↓ / Target → | **Content** (Git: collections, roles, playbooks, plugins) | **Platform** (live AAP) |
|---|---|---|
| **Auditor** | Review existing content, report debt | Review AAP state: access, EEs, health |
| **Builder** | Create or modernize content | Create Controller objects as code *(later)* |
| **Operator** | — | Run jobs, check status, diagnose *(read-only first)* |
| **Librarian** | Evolve governance: ADRs, rules, exceptions, slot adoptions — no target, it works on governance itself | |

## Modes are thin orchestrators

A mode owns the **workflow**. It does not contain Ansible knowledge; it
delegates that to the community bases (L0) and applies the organization's
effective governance on top.

```text
  user intent ──▶ MODE (workflow)
                    ├─▶ effective governance for the scope   (rules + exceptions)
                    ├─▶ base skills                          (ai-forge, aap-skills)
                    ├─▶ checker                              (same as the gates)
                    └─▶ output template                      (report, PR, ADR)
                                │
                                ▼
                    artifact + evidence
```

## Common contract

Every mode, in every response:

1. **Declares itself** in one line:
   `Mode: Builder · Target: content · Governance: acme@2026.11`
2. **Resolves effective governance** for the scope before acting (see
   [06-ai-channel.md](06-ai-channel.md)).
3. **Runs the checker** before claiming a task is done, when content changed.
4. **Cites the source** of every rule it applies or reports: rule id, ADR,
   layer (`L0 cop`, `L1 ADR-0005`, ...).
5. **Never decides rules.** When governance is missing or blocks the task, it
   stops and proposes (exception or ADR) instead of improvising.
6. **Never commits, pushes or writes to a live system** without explicit human
   confirmation.

## Auditor

| | |
|---|---|
| **Purpose** | Find where existing content or platform state deviates from effective governance |
| **Targets** | Content, Platform |
| **Triggered by** | "audit", "review", "check compliance", "what is wrong with…", PR review |
| **Inputs** | Scope (repo, paths, PR, AAP organization), effective governance |
| **Delegates to** | Content: `ansible-cop-review` and `ansible-zen` (ai-forge), checker. Platform: `aap-platform-health-check`, `aap-effective-access-review` (aap-skills) |
| **Output** | Audit report ([template](../../starter-kit/gac-modes/module/skills/gac-auditor/templates/audit-report.md)): findings by rule, source layer, severity, verifiability, suggested fix; optional baseline file |
| **Human gates** | None to read. Hand-off to Builder requires the user to accept the remediation plan |
| **Must not** | Modify files. Invent findings without a rule or L0 reference |

Workflow:
1. Fix the scope.
2. Resolve effective governance for that scope.
3. Run the checker → mechanical findings.
4. Delegate L0 review to base skills → heuristic findings with L0 reference.
5. Apply L1 heuristic rules from the registry.
6. When preparing a modernization, record the **current behavior**: observed
   (the original is run on a disposable host of the test platform) or
   described from the code and marked for human confirmation
   ([GAC-0010](../../adr/GAC-0010-define-success-before-acting.md)).
7. Classify each finding: rule id · layer · ADR · severity · verifiability · effort.
8. Produce the report. Optionally write a baseline (for `warn` → `block` transitions).
9. Offer a remediation plan for Builder, with the deviations from current behavior it implies.

## Builder

| | |
|---|---|
| **Purpose** | Produce new or modernized content that complies with effective governance |
| **Targets** | Content (Platform later, as configuration as code) |
| **Triggered by** | "create", "scaffold", "write", "modernize", "refactor", "fix findings" |
| **Inputs** | Intake (what, why, target repository), effective governance, optional audit report |
| **Delegates to** | `ansible-scaffold-collection`, `ansible-scaffold-role`, `write-content`, `write-content-tests`, `write-module`, `write-module-tests`, `remove-deprecations`, `ansible-markdown-docs`, `changelog-fragment`, `commit`, `create-pr` (ai-forge) |
| **Output** | Content changes, plus the tests, docs and approvals required by the process rules (`TEST`, `DOC`, `PROC`) that apply to the repository, PR draft ([template](../../starter-kit/gac-modes/module/skills/gac-builder/templates/pr-body.md)) listing the rules applied |
| **Human gates** | Approvals required by `PROC` rules; commit / PR only on explicit request |
| **Must not** | Finish with failing `block` findings. Bypass a rule instead of proposing an exception |

Workflow:
1. Intake: what, why, target repository.
2. Resolve effective governance for the target scope. The repository's
   classification in the manifest (promotion path, optional attributes such
   as `criticality`) decides which rules apply — including process rules.
3. **Success contract**, approved by a human before building
   ([GAC-0010](../../adr/GAC-0010-define-success-before-acting.md)):
   current behavior + deviations (modernize), acceptance criteria (new),
   reproduction (bug fix).
4. Plan the structure (only conventions the organization adopted).
5. Scaffold or modify through base skills.
6. Apply the process rules returned by `gac-governance` (`TEST`, `DOC`, `PROC`).
   Where `TEST` rules apply, the contract becomes automated tests for the
   instance's test platform, and they are **run**; otherwise it is verified
   lightly. Unrun tests are reported as "written, not run".
7. Checker loop: fix until there are no `block` findings, or stop and propose an exception.
8. Summarize: contract status, files changed, rules applied (with sources), remaining `warn` findings.
9. On request: changelog fragment, commit, PR draft.

## Librarian

| | |
|---|---|
| **Purpose** | Keep governance alive: turn needs and upstream changes into proposals |
| **Targets** | Governance (the instance itself) |
| **Triggered by** | New need, recurring audit finding, upstream base release, repeatedly renewed exception, request to adopt a tool |
| **Inputs** | The need, current governance, upstream diff, audit history |
| **Delegates to** | Auditor in dry-run mode, to estimate the impact of a proposed rule |
| **Output** | ADR draft (`proposed`), rule entry drafts, manifest diff, impact analysis (estimated baseline) |
| **Human gates** | Every output is a proposal; approvers per ADR type ([03-roles.md](03-roles.md)) |
| **Must not** | Set an ADR to `accepted`. Edit L0. Write a rule without an ADR |

## Operator

| | |
|---|---|
| **Purpose** | Operate AAP under the organization's governance |
| **Targets** | Platform |
| **Triggered by** | "run", "launch", "status of job", "why did it fail" |
| **Inputs** | Effective governance (e.g. approved EEs, naming, who may run what), AAP MCP Server |
| **Delegates to** | aap-skills through the AAP MCP Server |
| **Output** | Status, diagnosis, executed action log |
| **Human gates** | v1 read-only. Any write requires explicit confirmation (`human_gate: confirm`) and RBAC |
| **Must not** | Call AAP outside the MCP Server. Act on objects that violate a `block` rule |

## Hand-offs

```text
  Auditor ──(remediation plan accepted)──▶ Builder ──(checker green)──▶ PR
     │                                        │
     └──(recurring finding)──▶ Librarian ◀───(blocked: needs exception or rule)
```
