# 06 — Gates

> Status: draft v0.1

Gates prove compliance ([GAC-0006](../../adr/GAC-0006-gates-are-the-guarantee.md)).
They run outside the AI harness and cover all content repositories, including
those that deliver to production.

## The checker

One checker, used everywhere: by developers, by AI modes, by pre-commit, by
CI and by builds. Same input, same result.

```text
  content ──▶ ┌──────────────────────────────────────────────┐
              │ 1. ansible-lint (L0 rules, L1-chosen profile) │
              │ 2. organization checks (from the registry)    │
              │ 3. file policies: requirements.yml, galaxy.yml,│
              │    execution-environment.yml                   │
              │ 4. apply exceptions (scope + expiry)           │
              │ 5. apply baseline (known debt → reported, not  │
              │    blocking, during warn period)               │
              └───────────────────────┬──────────────────────┘
                                      ▼
            findings: rule id · ADR · layer · file:line · enforcement · ai_hint
```

Findings always carry the rule id and ADR, so humans and agents know where a
rule comes from and how to comply.

## Where gates run

| Gate | Checks | Blocks | Can be bypassed by the developer |
|------|--------|--------|----------------------------------|
| pre-commit | Checker on changed files | Commit (locally) | Yes — early feedback only |
| CI (PR) | Checker on the repository; governance version pinned | Merge (required status check) | No |
| EE build | `EE` and `COLL` rules on the EE definition | Image build | No |
| Hub publish | Collection dependencies and metadata | Publication | No |
| AAP runtime | Approved EEs, RBAC | Job execution | No |
| Instance CI | The governance repo itself: schemas, ADR ↔ rule consistency, expired exceptions | Governance merge | No |

## Enforcement transitions

```text
  rule accepted ──▶ warn ──(block_from date)──▶ block
                     │
                     └─ baseline recorded: existing violations are listed,
                        new violations are reported; at block_from,
                        only baselined items still pass, and the baseline
                        has its own burn-down date
```

## Requirements for an instance

- CI gates are **required status checks** on protected branches.
- Every content repository, including production delivery, runs the CI gate.
- The governance version used by gates is pinned and upgraded deliberately.
- No `continue-on-error` or `|| true` on `block` rules.

## Instance CI checks

| Check | Fails when |
|-------|-----------|
| Rule fixtures | An organization lint rule does not pass its fixtures (examples from its ADR that must pass and must fail) — [GAC-0010](../../adr/GAC-0010-define-success-before-acting.md) |
| Schema validation | Manifest, rules, exceptions or ADR frontmatter are invalid |
| ADR ↔ rule consistency | A rule references a non-accepted ADR; an accepted ADR has no rules and is not marked process-only |
| Exception validity | Missing owner or expiry; exception to a locked rule without rule-owner approval |
| Expiry watch | Exceptions expiring within 30 days (warning) |
| Restating L0 | Optional heuristic: L1 documents copying L0 text |
