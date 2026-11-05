# Audit report — <scope>

| | |
|---|---|
| **Mode** | Auditor · Target: content \| platform |
| **Scope** | <repository / paths / PR / AAP organization> |
| **Governance** | <instance>@<version> · method <version> |
| **Date** | YYYY-MM-DD |

## Summary

| Severity | block | warn | advise |
|----------|-------|------|--------|
| Count | 0 | 0 | 0 |

| Source | Findings |
|--------|----------|
| L0 (community) | 0 |
| L1 (organization) | 0 |
| L2 (domain) | 0 |

## Findings

| # | Rule | Source | Enforcement | Verifiability | Location | Finding | Suggested fix |
|---|------|--------|-------------|---------------|----------|---------|---------------|
| 1 | R-XXX-NNN / lint:<rule> / cop:<section> | L1 ADR-NNNN / L0 | block | mechanical | path:line | ... | ... |

## Current behavior

<!-- When the audit prepares a modernization (GAC-0010). Remove otherwise. -->

How obtained: **observed** (ran on <runtime> against <test platform host>, twice) | **described** (from the code — to be confirmed by a human)

| # | Behavior today | Notes |
|---|----------------|-------|
| B1 | <...> | <e.g. second run reports changes> |

## Exceptions applied

| Exception | Rule | Scope | Expires |
|-----------|------|-------|---------|

## Remediation plan

Ordered steps for Builder. Effort estimate per step.

## Verification

- Checker result (`ansible-lint -c <instance>/gates/ansible-lint.yml <scope>`)
- Baseline recorded: yes / no
