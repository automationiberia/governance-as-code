---
id: GAC-0005
title: Extend the harness through slots
status: accepted
layer: method
type: evolution
date: 2026-11-04
---

# GAC-0005: Extend the harness through slots

## Context

New tools that change how AI agents work appear constantly: skill libraries,
MCP servers, output compressors, response style plugins, hooks, sandboxes.
In the first attempt, each new piece (ai-forge, aap-skills, a package
manager) required restructuring the repository. Governance must scale with
this flow without being redesigned each time.

## Decision

1. The AI agent's **harness** is governed through eight fixed **slots**:
   Knowledge, Capabilities, Integrations, Input, Output, Guardrails,
   Execution, Evolution.
2. Every tool is classified into a slot before adoption.
3. Adoption is an ADR in the owning layer (`type: harness-adoption`) and an
   entry in that layer's instance manifest, pinned to a version.
4. Layers and precedence apply to every slot, not only to rules.
5. A tool that fits no slot triggers a method ADR to revise the slot model.
6. Gates are not a slot; they stay outside the harness
   ([GAC-0006](GAC-0006-gates-are-the-guarantee.md)).

## Consequences

- Adding a new tool changes one slot in one layer; the model stays stable.
- Organizations can share slot configurations (e.g. a "regulated industry"
  bundle) across instances.
- The slot list itself is versioned by this method and may evolve.
