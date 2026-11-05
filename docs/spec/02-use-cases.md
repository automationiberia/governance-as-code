# 02 — Use cases

> Status: draft v0.1

The entry point for users. Each use case says which mode to use, what
happens, and what proves it is done.

## Catalog

| ID | I want to… | Mode | Target | Proven by |
|----|------------|------|--------|-----------|
| UC-01 | Create a collection | Builder | Content | CI gates |
| UC-02 | Create a role | Builder | Content | CI gates |
| UC-03 | Create a playbook | Builder | Content | CI gates |
| UC-04 | Modernize a role (`with_*` → `loop`, FQCN, deprecated modules) | Auditor → Builder | Content | Audit report + CI gates |
| UC-05 | Write a module or plugin | Builder | Content | CI gates + unit tests |
| UC-06 | Audit a repository | Auditor | Content | Audit report |
| UC-07 | Review a pull request | Auditor | Content | Review comments citing rules |
| UC-08 | Add an organization rule | Librarian | Governance | Accepted ADR + rule entry + check |
| UC-09 | Request a project exception | Librarian | Governance | Approved exception entry |
| UC-10 | Adopt a tool into a slot | Librarian | Governance | Accepted harness-adoption ADR + manifest entry |
| UC-11 | Upgrade a community base | Librarian | Governance | Upstream impact report + evolution ADR |
| UC-12 | Onboard a new organization | Librarian + Auditor | Governance | Instance with initial ADRs, gates in `warn`, baseline |
| UC-13 | Audit AAP access and health | Auditor | Platform | Platform audit report |
| UC-14 | Check a job / diagnose a failure | Operator | Platform | Diagnosis |

## Detailed flows

### UC-04 — Modernize a role

```text
 /audit roles/<role>          Auditor: report with findings by rule and layer
        │                     (e.g. with_dict → L0 cop · no argument_specs → L1 ADR-0002)
        ▼
 accept plan + contract       human: remediation plan, success contract, deviations
        ▼
 /build fix findings          Builder: refactor via base skills, checker loop
        ▼
 checker green                no block findings; remaining warn listed
        ▼
 PR draft                     lists rules applied and their sources
```

Worked example: [10-examples.md#ex-01](10-examples.md#ex-01--modernize-ansible-manage-users).

### UC-01 — Create a collection

1. `/build collection <namespace.name>` → Builder runs intake (what, why, target repository).
2. Builder resolves governance for `content: collection` in that repository: its classification in the manifest decides which rules apply (naming, allowed dependencies, required tests and docs).
3. Builder writes the **acceptance criteria** (success contract) and gets them approved.
4. Scaffold via `ansible-scaffold-collection`; apply organization deltas.
5. Content and tests via `write-content` / `write-content-tests`; tests run on the test platform when `TEST` rules apply.
6. Checker loop until green.
7. Docs via `ansible-markdown-docs`; changelog fragment; PR draft on request.

### UC-08 — Add an organization rule

1. `/librarian rule "<need>"` → Librarian drafts ADR (`proposed`) with **examples** (must pass / must fail) and rule entries; for mechanical rules, fixtures first, then the lint rule.
2. Librarian runs Auditor dry-run → estimated baseline (how much content would violate it).
3. Approvers review per ADR type → `accepted`.
4. Rule enters in `warn`; check is wired into gates; `block_from` date is set.

### UC-12 — Onboard a new organization

The most important use case: the organization **already has a way of
working**.

1. Create the instance from the starter kit ([08-instance.md](08-instance.md)); pin bases.
2. **Import existing conventions**: Librarian reads the organization's
   current standards (documents, wikis, review checklists) and drafts one ADR
   per real difference from L0. Restating L0 is discarded.
3. **Discover reality**: Auditor runs on representative repositories against
   L0 + draft ADRs → findings and candidate rules.
4. Approvers accept the initial ADRs.
5. Gates in `warn` everywhere; baseline recorded.
6. `block_from` dates agreed per rule.

## Commands

Modes are invoked through slash commands installed with the starter kit:

| Command | Mode |
|---------|------|
| `/audit <scope>` | Auditor |
| `/build <what>` | Builder |
| `/librarian <need>` | Librarian |
| `/operate <action>` | Operator |

Natural language works too; the mode skills are triggered by intent.
