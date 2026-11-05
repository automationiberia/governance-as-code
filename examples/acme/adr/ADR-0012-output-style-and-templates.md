---
id: ADR-0012
title: "Output: artifact templates and a concise conversational style"
status: accepted
layer: organization
domain: null
type: harness-adoption
slot: output
date: 2026-11-05
approvers: [automation-lead]
supersedes: null
superseded_by: null
acts_on:
  - action: add
    target: null
rules: []
---

# ADR-0012: Output: artifact templates and a concise conversational style

> Approval simulated in this example. Admission criteria: [slot catalog](../../../slots/README.md).

## Context

Reports, contracts, PRs and ADRs must be complete and uniform; conversation should be short and actionable.

## Decision

In the **Output** slot: (1) the artifact templates shipped with the modes are **required**; (2) the `i-have-adhd` style skill is **recommended** for conversation. **Precedence: templates win** — an artifact is always complete, whatever the conversational style.

## Admission

| Criterion | Answer |
|-----------|--------|
| Touches | Response format only |
| Scope | Project |
| Pinning | Templates: method version; i-have-adhd: commit `1ecea19` |
| Conflicts | Style rules ("cap lists to 5", "no recaps") vs complete reports: templates win (P8) |
| Verification | Templates exist; style skill installed |
| Removal | Remove the entry |

## Consequences

- Applied and verified by `gac-setup` (manifest `slots.output`).
- i-have-adhd's own always-on hook is not adopted; only its skill.
