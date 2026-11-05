---
id: ADR-0004
title: command and shell only when no module provides the capability
status: accepted
layer: organization
domain: null
type: coding-standard
slot: null
date: 2026-11-04
approvers: [automation-lead]
supersedes: null
superseded_by: null
acts_on:
  - action: tighten
    target: "lint:command-instead-of-module, lint:no-changed-when"
rules: [R-CODE-002]
---

# ADR-0004: command and shell only when no module provides the capability

## Context

ansible-lint flags common cases (`command-instead-of-module`,
`no-changed-when`) but cannot know every capability gap. Unjustified
`command` / `shell` tasks are hard to review and often not idempotent.

## Decision

`ansible.builtin.command` and `ansible.builtin.shell` are allowed only when
no module in the allowed collections provides the capability. Such a task:

1. Has a comment directly above it naming the missing capability.
2. Is idempotent: it runs only when a check shows a change is needed, and
   sets `changed_when`.

## Consequences

- Reviewers can verify each exception to "modules first" quickly.

## Enforcement

| Rule | Verifiability | Enforcement | Locked | `block` from |
|------|---------------|-------------|--------|--------------|
| R-CODE-002 | heuristic | advise | no | — |

## Alternatives considered

- Forbidding `command` / `shell` entirely: some capabilities have no module.
