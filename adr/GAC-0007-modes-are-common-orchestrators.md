---
id: GAC-0007
title: Modes are common orchestrators; organization governance is data
status: accepted
layer: method
type: evolution
date: 2026-11-04
---

# GAC-0007: Modes are common orchestrators; organization governance is data

## Context

The first attempt had Auditor, Builder and Librarian modes, which made the
repository easy to use. But its mode skills embedded Ansible knowledge that
duplicated ai-forge, and organization rules were written inside them. Every
organization would need its own copy of the modes.

## Decision

1. Modes (Auditor, Builder, Librarian, Operator) are defined by the method and
   are **the same for every organization**.
2. A mode owns a **workflow**: resolve effective governance, delegate to base
   skills, run the checker, produce output from templates.
3. A mode contains **no Ansible knowledge** (delegated to L0 bases) and **no
   organization rules** (consumed as data from the instance).
4. Orchestrating base skills is not forking them and does not conflict with
   [GAC-0002](GAC-0002-consume-bases-never-fork.md).
5. Modes are distributed as part of the starter kit.

## Consequences

- One set of modes serves every instance; improvements reach everyone.
- Modes depend on base skill names and behavior; base upgrades must check
  mode delegation (part of the upstream review routine).
- Organizations customize behavior only through governance (ADRs, rules,
  templates, slot adoptions), never by editing modes.
