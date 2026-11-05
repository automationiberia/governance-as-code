---
id: ADR-0002
title: Roles declare their interface with argument specs
status: accepted
layer: organization
domain: null
type: coding-standard
slot: null
date: 2026-11-04
approvers: [automation-lead, linux-team-representative]
supersedes: null
superseded_by: null
acts_on:
  - action: tighten
    target: "cop:roles/argument-validation"
rules: [R-DOC-001]
---

# ADR-0002: Roles declare their interface with argument specs

## Context

CoP *Argument Validation* recommends `meta/argument_specs.yml`. ACME roles
are consumed by several teams and by AAP job templates; roles without it have
caused misuse and silent defaults.

## Decision

**Tighten** the CoP recommendation: argument specs are **mandatory** for
every role and enforced by the checker (`R-DOC-001`). The content of the
specification follows CoP and the Ansible documentation; this ADR does not
restate it.

## Consequences

- Wrong or missing variables fail early with a clear message.
- Existing roles without argument specs must add them.

## Enforcement

| Rule | Verifiability | Enforcement | Locked | `block` from |
|------|---------------|-------------|--------|--------------|
| R-DOC-001 | mechanical (custom lint rule) | block | no | 2026-11-04 |

## Examples

Fixtures: [gates/rules/tests](../gates/rules/tests/) (`doc_*`).

| # | Content | Must |
|---|---------|------|
| E1 | Role with `meta/argument_specs.yml` | pass |
| E2 | Role with `argument_specs` inside `meta/main.yml` | pass |
| E3 | Role without argument specs | fail |
| E4 | Role without argument specs whose `tasks/main.yml` has a syntax error | fail |
| E5 | ansible-test integration target (`tests/integration/targets/<t>`) — not a role | pass |

## Alternatives considered

- Keep it as a CoP recommendation: roles kept shipping without it.
