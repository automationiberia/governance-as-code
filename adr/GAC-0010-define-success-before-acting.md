---
id: GAC-0010
title: Define success before acting
status: accepted
layer: method
type: evolution
date: 2026-11-05
---

# GAC-0010: Define success before acting

## Context

Until now the method answered "does it comply with the rules?" (gates) but
not "does it do what was asked?" nor "does it keep working?". Building and
validating the worked examples showed the cost of that gap:

| Evidence | What was missing |
|----------|------------------|
| EX-01: the modernized role failed (`append` without `groups`, wrong shadow field) after it was written | A test prepared before the implementation |
| EX-01: a behavior change was decided during the build and only flagged at the end, in the PR | A decision taken by a human before building |
| EX-01 characterization: the original's password policy never ran on Python 3 (its module does not import); the audit and the PR described what the code says, not what happens | The current behavior, observed before modernizing |
| R-DOC-001 and R-COLL-001 had three false positives/negatives, found by real content and by dogfooding | Fixtures written with the rule |
| Dogfooding: a clean Builder wrote a working role, but its Molecule scenario had two environment defects it could not see | Tests run where they are written, on a known platform |

The validation is recorded in
[examples/acme/gates/rules/tests](../examples/acme/gates/rules/tests/),
[EX-01 characterization](../examples/ex-01-modernize-ansible-manage-users/characterization/README.md)
and [dogfooding](../docs/validation/dogfooding-2026-11-05/README.md).

## Decision

1. **Before acting, each mode fixes what will count as success and makes it
   checkable.** The form depends on the use case:

   | Use case | Success is defined by |
   |----------|-----------------------|
   | Modernize existing content | Its **current behavior** — observed by running it (characterization) when possible, otherwise described from the code and confirmed by a human — plus the audit findings and the **accepted deviations** |
   | Create new content | **Acceptance criteria** |
   | Fix a bug | A **reproduction** of the bug |
   | Add or change an organization rule | **Examples** that must pass and must fail, which become the rule's **fixtures** |

2. For the Builder, that definition is a **success contract** that a human
   approves **before** building. In an unattended run, the Builder writes the
   contract with its assumptions, marks it *not approved*, and the result
   cannot be merged until a human approves it.
3. **How much is automated testing stays an organization decision**
   ([GAC-0009](GAC-0009-no-work-profiles.md)): where `TEST` rules apply, the
   contract becomes automated tests that run before the work is declared
   done; where none apply, the contract is verified lightly (syntax check, a
   run with assertions) — but it is still written.
4. **Organization lint rules are code**: every mechanical rule has fixtures,
   written before or with the rule, and the instance CI runs them.
5. **Tests run where they are written.** The instance declares the **test
   platform** (Execution slot): how disposable test hosts are created (driver,
   image, init, privileges, privilege escalation). Builders generate tests for
   that platform and run them; when they cannot, they say so explicitly
   ("written, not run") and the PR shows it.

## Consequences

- Important decisions (behavior changes, scope) move to the start and are
  taken by humans; the AI no longer discovers them halfway through.
- Defects are found by a prepared comparison or test, not by chance.
- Modes gain a step and templates (success contract; current behavior in the
  audit report; examples in ADRs); instances gain a test platform declaration
  and rule fixtures.
- Characterization needs a runtime where the original still runs; when that is
  impossible, its weaker form (described and confirmed) applies.
