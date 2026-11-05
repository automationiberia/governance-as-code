---
id: ADR-0009
title: "Adopt aap-skills for platform work"
status: accepted
layer: organization
domain: null
type: harness-adoption
slot: capabilities
date: 2026-11-05
approvers: [automation-lead, operations]
supersedes: null
superseded_by: null
acts_on:
  - action: add
    target: null
rules: []
---

# ADR-0009: Adopt aap-skills for platform work

> Approval simulated in this example. Admission criteria: [slot catalog](../../../slots/README.md).

## Context

ADR-0001 pinned aap-skills as a base, but no assistant had its skills installed: the Auditor (platform) and Operator modes had nothing to delegate to.

## Decision

Install the five customer-facing aap-skills (platform health, effective access, pre-upgrade readiness, supportability, deployment topology) in the **Capabilities** slot, pinned to the commit in `bases`. The developer tool `aap-skill-creator` is not installed.

## Admission

| Criterion | Answer |
|-----------|--------|
| Touches | Skills only; they act through the AAP MCP Server (ADR-0010) |
| Scope | Project |
| Pinning | Commit `4f30b4e` |
| Conflicts | Overlap with gac-operator: gac-operator orchestrates, aap-skills does the work |
| Verification | The five expected skills are present after install |
| Removal | Remove the entry and re-run setup |

## Consequences

- Applied and verified by `gac-setup` (manifest `slots.capabilities`).
- Lola's default discovery installed `aap-skill-creator` instead of the five skills; the entry sets `module_content: "/"` and `expect_skills`.
