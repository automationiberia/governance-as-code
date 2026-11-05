---
id: ADR-NNNN
title: <Short decision statement>
status: proposed            # proposed | in-review | accepted | rejected | superseded | deprecated
layer: organization         # organization | domain
domain: null                # domain name when layer is "domain"
type: coding-standard       # coding-standard | security-policy | lifecycle-policy | harness-adoption | exception-policy | evolution
slot: null                  # for harness-adoption: knowledge | capabilities | integrations | input | output | guardrails | execution | evolution
date: YYYY-MM-DD
approvers: []               # names or roles required by the decision type
supersedes: null            # ADR-NNNN
superseded_by: null         # ADR-NNNN
acts_on:                    # what this decision does to a lower layer
  - action: add             # add | replace | tighten | disable
    target: null            # lower-layer item, e.g. "cop:roles/variable-prefix" or "ai-forge:ansible-collection-sdlc"
rules: []                   # rule registry entries produced, e.g. [R-COLL-001]
---

# ADR-NNNN: <Short decision statement>

## Context

What is the situation? What does the community baseline (L0) say, or not say,
about it? Why is a decision needed now?

## Decision

What the organization decides, stated so it can be turned into rules or slot
adoptions. Only the delta from L0 — do not restate community content.

## Consequences

What becomes easier or harder. Impact on existing content (expected baseline
of violations), on teams, and on channels (AI harness, gates).

## Enforcement

| Rule | Verifiability | Enforcement | Locked | `block` from |
|------|---------------|-------------|--------|--------------|
| R-XXX-NNN | mechanical / heuristic / process | advise / warn / block | yes / no | YYYY-MM-DD |

## Examples

<!-- Required for mechanical rules: they become the rule's fixtures (GAC-0010). -->

| # | Content | Must |
|---|---------|------|
| E1 | <snippet or situation that complies> | pass |
| E2 | <snippet or situation that violates the rule> | fail |
| E3 | <edge case, e.g. the term only mentioned in a task name> | pass |

## Alternatives considered

Options that were evaluated and why they were not chosen.
