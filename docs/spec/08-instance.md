# 09 — Organization instance

> Status: draft v0.1

An instance is one organization's governance. The method requires certain
artifacts; it recommends, but does not impose, a layout.

## Required artifacts

| # | Artifact | Purpose |
|---|----------|---------|
| 1 | Instance manifest | Bases and versions, method version, layers, promotion paths, slot adoptions, gates |
| 2 | ADR log | Organization (and domain) decisions with status and approvers |
| 3 | Rule registry | Single source of rules |
| 4 | Exception register | Scoped, owned, expiring exceptions |
| 5 | Gate wiring | CI and pre-commit running the checker in every content repository |
| 6 | AI entry point | AGENTS.md pointer in each content repository |
| 7 | Role mapping | Who holds each role in [03-roles.md](03-roles.md) |
| 8 | Evidence | Audit reports, baselines, metrics |
| 9 | Test platform | How disposable test hosts are created (manifest `test_platform`, adopted by ADR in the Execution slot) |
| 10 | Rule fixtures | Tests for every organization lint rule, run by the instance CI |

## Recommended layout

One governance repository per organization; content repositories consume a
pinned version of it.

```text
<org>-governance/
├── manifest.yml
├── adr/                 # ADR-NNNN-*.md
├── rules/               # registry, split by area if large
├── exceptions/
├── domains/<name>/      # optional L2: adr/, rules/
├── templates/           # organization overrides of method templates
├── gates/               # ansible-lint config, organization rules, ignore files
└── reports/             # audits, baselines

<content repos>  (collections, roles, playbooks)
├── .lola-req            # bases + gac-modes, pinned
├── .pre-commit-config.yaml
└── CI workflow          # checker, governance @ pinned version
```

## Onboarding steps

1. Create the governance repository from the instance template.
2. Pin community bases and the method version in the manifest.
3. First ADR: ansible-lint profile and which L0 modules are enabled.
4. Import existing conventions as ADRs — only the delta from L0 (UC-12).
5. Run Auditor on representative repositories; refine candidate rules.
6. Accept initial ADRs; generate channels.
7. Wire gates in `warn` in every content repository; record baselines.
8. Agree `block_from` dates per rule.
