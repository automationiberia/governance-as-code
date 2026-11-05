---
id: ADR-0013
title: "Run the checker after every edit (guardrail)"
status: accepted
layer: organization
domain: null
type: harness-adoption
slot: guardrails
date: 2026-11-05
approvers: [automation-lead]
supersedes: null
superseded_by: null
acts_on:
  - action: add
    target: null
rules: []
---

# ADR-0013: Run the checker after every edit (guardrail)

> Approval simulated in this example. Admission criteria: [slot catalog](../../../slots/README.md).

## Context

Agents learned about rule violations only when they ran the checker or when CI failed.

## Decision

Adopt, in the **Guardrails** slot, a post-tool hook that runs the organization checker after the agent edits Ansible content and returns **only the findings of that file**. It ignores the governance instance and assistant directories.

## Admission

| Criterion | Answer |
|-----------|--------|
| Touches | Local files; runs ansible-lint offline |
| Scope | Project hook |
| Pinning | Method version (`starter-kit/hooks/gac_checker_on_edit.py`) |
| Conflicts | None: guidance only; CI remains the proof (GAC-0006) |
| Verification | Hook registered; tests for clean, violating and ignored files |
| Removal | Remove the entry |

## Consequences

- Applied and verified by `gac-setup` (manifest `slots.guardrails`).
- Developers can disable hooks locally; the CI gate still blocks.
