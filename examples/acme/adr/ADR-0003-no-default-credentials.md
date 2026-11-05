---
id: ADR-0003
title: No credentials in role defaults
status: accepted
layer: organization
domain: null
type: security-policy
slot: null
date: 2026-11-04
approvers: [automation-lead, security]
supersedes: null
superseded_by: null
acts_on:
  - action: add
    target: null
rules: [R-SEC-001]
---

# ADR-0003: No credentials in role defaults

## Context

Roles that set default passwords (for example, a password equal to the user
name) create accounts with guessable credentials whenever the consumer
forgets to override them.

## Decision

Roles must not define default values for passwords, tokens or keys. Such
variables are required inputs (declared in argument specs) and their values
come from a vault or a credential store.

## Consequences

- Consumers must always provide credentials explicitly.
- Detecting every form of credential default is not reliably mechanical; the
  rule is reviewed by the Auditor and in pull requests.

## Enforcement

| Rule | Verifiability | Enforcement | Locked | `block` from |
|------|---------------|-------------|--------|--------------|
| R-SEC-001 | heuristic | advise | yes | — |

## Alternatives considered

- A lint rule matching variable names containing `password`: too many false
  positives and negatives; may be added later as a `warn` helper.
