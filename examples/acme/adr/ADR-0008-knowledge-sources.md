---
id: ADR-0008
title: "Knowledge sources for AI assistants"
status: accepted
layer: organization
domain: null
type: harness-adoption
slot: knowledge
date: 2026-11-05
approvers: [automation-lead]
supersedes: null
superseded_by: null
acts_on:
  - action: add
    target: null
rules: []
---

# ADR-0008: Knowledge sources for AI assistants

> Approval simulated in this example. Admission criteria: [slot catalog](../../../slots/README.md).

## Context

Assistants must decide with the same knowledge as people: the community baseline and the organization's governance — and nothing copied into prompts.

## Decision

Adopt, in the **Knowledge** slot: the community baseline (CoP good practices and the ansible-lint profile, pinned in `bases`) and the organization governance (manifest, ADRs, rules, exceptions). Assistants read them where they live, through `gac-governance`.

## Admission

| Criterion | Answer |
|-----------|--------|
| Touches | Read-only knowledge; nothing leaves the machine |
| Scope | Project (instance checkout) |
| Pinning | Bases by commit/tag; instance by version |
| Conflicts | None: precedence is defined by the layers |
| Verification | Referenced bases and paths exist |
| Removal | Remove the entry |

## Consequences

- Applied and verified by `gac-setup` (manifest `slots.knowledge`).
- No organization rule is copied into skills or prompts.
