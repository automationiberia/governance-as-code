---
id: ADR-0005
title: Forbid community.general in production content
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
rules: [R-COLL-001]
---

# ADR-0005: Forbid community.general in production content

> Drafted by the Librarian ([proposal](../../ex-03-forbid-community-general/reports/librarian-proposal.md));
> approved by automation-lead and security (approval simulated in this example).

## Context

Production automation must only depend on collections covered by a support
agreement. `community.general` is a large community collection without that
coverage; teams add it as a dependency for one or two modules. CoP, ansible-lint
and ai-forge say nothing about which collections are allowed.

## Decision

In repositories on the **prod** promotion path, nothing from
`community.general` is used: no modules, plugins, filters, lookups,
dependencies (`requirements.yml`, `galaxy.yml`) or execution environment
content. Use `ansible.builtin`, `ansible.posix` or certified collections.

Repositories not classified in the manifest are treated as prod.

Exceptions only through the exception register, approved by the rule owner
(security), scoped to a repository and items, with an expiry date.

## Consequences

- One repository (`firewall_legacy`) needs an exception until its migration.
- Teams lose some convenience modules; when no supported alternative exists,
  they request an exception or propose an allowlist addition.
- Every repository must be classified in the manifest, or it is treated as prod.

## Enforcement

| Rule | Verifiability | Enforcement | Locked | `block` from |
|------|---------------|-------------|--------|--------------|
| R-COLL-001 | mechanical (custom lint rule) | block | yes (owner: security) | 2026-11-04 |

Impact at decision time: 1 of 6 repositories affected (3 findings), so no
warn period or baseline.

## Examples

Fixtures: [gates/rules/tests](../gates/rules/tests/) (`coll_*` and exception unit tests).

| # | Content (prod repository unless stated) | Must |
|---|------------------------------------------|------|
| E1 | Task using `community.general.ufw` | fail |
| E2 | `community.general.json_query` filter | fail |
| E3 | `community.general` in `requirements.yml`, `galaxy.yml` or `execution-environment.yml` | fail |
| E4 | `community.general` only in a comment or a task name | pass |
| E5 | Same content in a nonprod repository | pass |
| E6 | Same content in an unclassified repository | fail (deny by default) |
| E7 | Covered by an approved, unexpired exception for that repository and item | pass |
| E8 | Exception expired, not approved, other repository, or item outside its scope | fail |

## Alternatives considered

- **Allowlist of certified collections only**: stronger, but needs an
  inventory of what teams use today. Candidate for a later ADR.
- **warn only**: would not stop new dependencies from reaching production.
