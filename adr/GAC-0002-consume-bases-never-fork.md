---
id: GAC-0002
title: Consume community bases, never fork them
status: accepted
layer: method
type: evolution
date: 2026-11-04
---

# GAC-0002: Consume community bases, never fork them

## Context

The community bases (CoP good practices, ai-forge, aap-skills) evolve
continuously. The first attempt created organization skills in parallel to
ai-forge skills and copied AAP skills from a separate repository instead of
the official one. Every copy became a fork to maintain, and upstream
improvements stopped flowing in.

## Decision

1. Community bases are consumed at L0, **as published**, pinned to a
   specific version (commit, tag or release).
2. An instance never edits, patches or forks a base. Organization behavior is
   added on top through L1 (rules, overrides, slot adoptions).
3. Wrapping a base capability is allowed only when no other extension point
   works, and must be justified by an organization ADR.
4. Upgrading a base is an L1 decision, reviewed like any other change.
5. Instances consume the **official** source of each base.

## Consequences

- Upstream improvements reach every instance by bumping a version.
- The question "how does a base skill learn our rules without being
  modified?" must be answered by the method (see docs/spec/06-ai-channel.md).
- Some organization needs may have to wait for an extension point rather than
  be patched into a base.
