---
id: GAC-0003
title: The organization layer is a delta
status: accepted
layer: method
type: evolution
date: 2026-11-04
---

# GAC-0003: The organization layer is a delta

## Context

In the first attempt, the organization "white book" restated large parts of
the CoP good practices (coding style, roles, playbooks, plugins, inventories)
while the list of real differences from CoP had only three entries. It became
impossible to tell an organization decision from restated community content,
and every CoP change required reviewing the whole white book.

## Decision

1. L1 contains **only** what the organization does differently from, or in
   addition to, L0.
2. Each L1 item is expressed as an action on L0 — `add`, `replace`,
   `tighten` or `disable` — and references the ADR that justifies it.
3. Where L1 is silent, L0 applies. Restating L0 in L1 is not allowed.
4. Explanatory documentation may link to L0 content; it must not copy it.

## Consequences

- An organization's governance stays small and its intent stays visible.
- Upgrading L0 only requires checking the L1 items that touch the changed
  topics.
- Teams must learn to read two sources (L0 + L1 delta); the mode skills
  present the resolved view for each task (docs/spec/06-ai-channel.md).
