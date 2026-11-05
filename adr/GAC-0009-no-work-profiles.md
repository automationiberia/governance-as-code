---
id: GAC-0009
title: "No work profiles: process requirements are organization rules scoped by repository classification"
status: accepted
layer: method
type: evolution
date: 2026-11-04
---

# GAC-0009: No work profiles — process requirements are organization rules scoped by repository classification

## Context

Draft v0.1 of the method defined three work profiles (light, standard,
heavy) with default process requirements: tests, interface documentation,
design notes, reviewers, change approval. Building the worked examples
showed three problems:

1. **Duplication.** Profiles repeated a classification the instance already
   has: the promotion path of each repository in the manifest.
2. **Not verifiable.** The requester declared the profile. A gate cannot
   check a self-declared value, so the strongest requirements depended on
   the requester choosing the strictest profile.
3. **Policy inside the method.** The default requirements per profile were
   organization decisions embedded in the method, which contradicts
   [GAC-0007](GAC-0007-modes-are-common-orchestrators.md): modes are common,
   governance is data.

## Decision

1. The method has **no work profiles**.
2. Process requirements (tests, documentation, reviewers, change approval)
   are **ordinary organization rules**: ADR → rule registry → channels, in
   the areas `TEST`, `DOC` and `PROC`.
3. Their scope is defined by the **repository classification** in the
   instance manifest: the promotion path and, when needed, optional
   objective attributes such as `criticality`.
4. The classification is decided by governance (the manifest, changed
   through the Librarian and approved like any governance change), **never by
   whoever requests the work**.
5. Modes do not ask for or declare a profile. They apply the process rules
   that `gac-governance` selects for the repository.

## Consequences

- Process requirements are traceable and auditable like any other rule, and
  each organization decides them.
- A repository's requirements change when its classification changes — a
  reviewed governance change — not per request.
- Organizations that want finer distinctions add classification attributes
  (for example `criticality: high`) and scope rules to them.
- Removes `docs/spec/03-profiles.md`, the profile defaults in
  `gac-governance`, the `profiles` manifest field and the profile fields in
  templates.
