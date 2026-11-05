---
id: GAC-0004
title: A single source for every rule
status: accepted
layer: method
type: evolution
date: 2026-11-04
---

# GAC-0004: A single source for every rule

## Context

In the first attempt, rules lived in prose documents and were copied by hand
into skills and agent instructions. Linters did not know about organization
rules at all. A rule such as "this collection is forbidden" had nowhere to
live, and it would need to reach three different places: the AI assistant,
the linter/CI, and the execution environment build.

## Decision

1. Every organization rule exists **once**, as an entry in the instance's
   **rule registry**, derived from an accepted ADR.
2. Each entry declares at least: identifier, source ADR, statement, scope,
   verifiability (`mechanical`, `heuristic`, `process`), enforcement level
   (`advise`, `warn`, `block`), whether it is locked, and a short hint for AI
   agents.
3. Channels derive their configuration from the registry. Writing a rule by
   hand into a skill, a linter configuration or a CI script is not allowed.
4. Prose documentation explains rules; it is never the source of a rule.

## Consequences

- A rule change is one registry change plus regenerated channel configuration.
- The registry needs a schema and validation (see docs/spec/04-rules.md).
- Rules that cannot be checked mechanically are still registered, with their
  verifiability stated, so that nobody assumes a gate covers them.
