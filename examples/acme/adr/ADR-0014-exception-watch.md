---
id: ADR-0014
title: "Exception watch in the instance CI"
status: accepted
layer: organization
domain: null
type: harness-adoption
slot: evolution
date: 2026-11-05
approvers: [automation-lead]
supersedes: null
superseded_by: null
acts_on:
  - action: add
    target: null
rules: []
---

# ADR-0014: Exception watch in the instance CI

> Approval simulated in this example. Admission criteria: [slot catalog](../../../slots/README.md).

## Context

The method promised a review of expiring exceptions; nothing implemented it.

## Decision

Adopt, in the **Evolution** slot, `gates/checks/exception_watch.py` in the instance CI: expired or invalid exceptions **fail**; exceptions expiring within 30 days are **warned**, so the Librarian can renew or close them.

## Admission

| Criterion | Answer |
|-----------|--------|
| Touches | The exception register only |
| Scope | Instance CI and setup |
| Pinning | Instance version |
| Conflicts | None |
| Verification | Tests with injected dates; the check passes on today's register |
| Removal | Remove the entry and the CI step |

## Consequences

- Applied and verified by `gac-setup` (manifest `slots.evolution`).
- Renewing an exception more than twice is a signal to revisit the ADR (see docs/spec/09-evolution.md).
