---
id: ADR-0001
title: Adopt the community baseline and tighten loop variable naming
status: accepted
layer: organization
domain: null
type: evolution
slot: null
date: 2026-11-04
approvers: [automation-lead]
supersedes: null
superseded_by: null
acts_on:
  - action: add
    target: "cop-good-practices, ai-forge, aap-skills, ansible-lint@production"
  - action: tighten
    target: "lint:loop-var-prefix"
rules: [R-CODE-001]
---

# ADR-0001: Adopt the community baseline and tighten loop variable naming

## Context

ACME starts its governance from the community. CoP good practices recommend
prefixing role loop variables with `__<role>_`. ansible-lint implements this
as the optional `loop-var-prefix` rule, which no ansible-lint profile enables.

## Decision

1. Consume, pinned as recorded in `manifest.yml`: CoP good practices,
   ai-forge (all five modules), aap-skills, and ansible-lint with the
   `production` profile.
2. Adopt the `gac-modes` module as the way AI assistants work.
3. **Tighten** L0: enable `loop-var-prefix` with prefix `__<role>_`
   (rule `R-CODE-001`).

## Consequences

- Everything not covered by later ACME ADRs follows the community baseline.
- Roles using the implicit `item` variable fail the checker.

## Enforcement

| Rule | Verifiability | Enforcement | Locked | `block` from |
|------|---------------|-------------|--------|--------------|
| R-CODE-001 | mechanical | block | no | 2026-11-04 |

## Alternatives considered

- Keep ansible-lint's default prefix (`__` or `<role>_`): less consistent
  with CoP.
