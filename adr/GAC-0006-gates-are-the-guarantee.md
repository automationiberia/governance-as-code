---
id: GAC-0006
title: Gates are the guarantee; the AI channel is guidance
status: accepted
layer: method
type: evolution
date: 2026-11-04
---

# GAC-0006: Gates are the guarantee; the AI channel is guidance

## Context

AI assistants may ignore instructions, skip a tool call or behave differently
across products. Developers may also work without AI. In the first attempt,
most enforcement depended on the agent reading and obeying text, while CI
checks were non-blocking and production content was outside their scope.

## Decision

1. **Compliance is proven by gates**: pre-commit, CI, execution environment
   build, Automation Hub publishing and AAP runtime controls.
2. Gates run in a trusted zone the agent cannot bypass, and cover **all**
   content repositories, including those that deliver to production.
3. The AI harness (mode skills, pointer, hooks) is **guidance**: it reduces
   the cost of compliance by steering the agent early. It is never the proof.
4. AI agents should run the same checker the gates use and act on its
   findings.
5. New rules enter in `warn` and move to `block` on a stated date, with a
   baseline of existing violations.

## Consequences

- Governance holds even when an agent misbehaves or when no AI is used.
- Every `mechanical` rule needs a gate implementation (see docs/spec/05-gates.md).
- `heuristic` and `process` rules rely on review and approval flows; their
  limits are explicit in the registry.
