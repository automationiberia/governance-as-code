---
id: ADR-0006
title: Production roles have an idempotency test
status: accepted
layer: organization
domain: null
type: lifecycle-policy
slot: null
date: 2026-11-04
approvers: [automation-lead, operations]
supersedes: null
superseded_by: null
acts_on:
  - action: tighten
    target: "cop:roles/idempotency"
rules: [R-TEST-001]
---

# ADR-0006: Production roles have an idempotency test

## Context

CoP *Idempotency* and *Check Mode* say roles must not report changes on a
second run. ACME has found non-idempotent roles only after they reached
production (EX-01: a role reset users' password dates on every run). Under
GAC-0009 there are no work profiles; this requirement must be an ordinary
rule scoped by repository classification.

## Decision

**Tighten** the CoP recommendation for repositories on the **prod**
promotion path: every role and collection has an automated test that applies
the content twice and fails if the second run reports changes — a Molecule
scenario with the `idempotence` step, or an integration test run twice.

Nonprod repositories are not affected.

## Consequences

- Production content needs a test harness; nonprod content does not.
- A repository moving from nonprod to prod (a manifest change) gains this
  requirement automatically.

## Enforcement

| Rule | Verifiability | Enforcement | Locked | `block` from |
|------|---------------|-------------|--------|--------------|
| R-TEST-001 | heuristic | advise | no | — |

The Auditor checks it by looking for a Molecule scenario with
`idempotence`, or an integration test run twice, covering each role, and the
second-run result in the PR.

**Proposed follow-up:** make it mechanical — a custom lint rule that requires,
for each role in a prod repository, a Molecule scenario whose test sequence
includes `idempotence` (or an integration target for the role) — and move it
to `warn`, then `block`, through a new ADR once teams have a harness.

## Alternatives considered

- Mechanical from day one: most existing repositories would fail
  immediately and no common test harness exists yet.
- Manual idempotency evidence in PRs only: not repeatable.
