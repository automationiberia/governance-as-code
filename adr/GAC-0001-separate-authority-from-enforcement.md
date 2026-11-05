---
id: GAC-0001
title: Separate authority from enforcement
status: accepted
layer: method
type: evolution
date: 2026-11-04
---

# GAC-0001: Separate authority from enforcement

## Context

A first attempt at governance as code (`ai-auto-governance-as-code`) defined
a precedence chain of *community → white book → skills → mechanical gates*.
That chain mixed two different things:

- **Sources of authority** — who decides a rule (community, organization).
- **Enforcement channels** — what applies a rule (AI skills, linters, CI).

Placing skills and gates in the same chain as decision makers made it unclear
who could change a rule, and allowed rules to be written directly into skills
or linter configuration.

## Decision

1. Precedence orders **sources of authority only**: L0 Community, L1
   Organization, L2 Domain (optional), L3 Project.
2. Skills, hooks, MCP servers, pre-commit, CI, EE builds and AAP runtime
   controls are **channels**. They consume effective governance; they never
   define it.
3. A channel may never contain a rule that does not exist in the rule
   registry.

## Consequences

- There is exactly one answer to "who decided this?": an ADR in a layer.
- Channels can be added, replaced or removed without changing any rule.
- Every channel must trace its configuration back to the registry (e.g.
  custom lint rule ids equal registry ids; see docs/spec/07-starter-kit.md).
