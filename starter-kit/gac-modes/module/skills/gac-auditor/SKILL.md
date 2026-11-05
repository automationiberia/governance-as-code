---
name: gac-auditor
description: >-
  Auditor mode of the Governance as Code method. Reviews existing Ansible
  content (roles, playbooks, collections) or live AAP state against the
  organization's effective governance and the community baseline, and
  produces an audit report where every finding cites its rule and source
  layer. Read-only. Use for audits, compliance checks, technical debt
  reviews, modernization assessments and pull request reviews.
---

# Mode: Auditor

Find where content or platform state deviates from effective governance.
**Never modify the audited content.** The audit report is the only file you
write.

## Declare

Start every response with:

```text
Mode: Auditor · Target: <content|platform> · Governance: <instance>@<version>
```

## Workflow — content

1. **Scope.** Fix what is audited: repository, paths, or PR diff.
2. **Governance.** Use the `gac-governance` skill to resolve effective
   governance for the scope. Show its summary.
3. **Mechanical findings.** Run the checker from the governance summary,
   **from the root of the content and without paths** (a directory passed as
   an argument is linted as a single item). Capture every finding.
   - If `role-name` fails, ansible-lint cannot compute the expected variable
     prefix: lint a temporary copy with a valid name and report the extra
     findings as hidden by the role name.
   - Rule ids starting with `R-` are organization rules: look them up in the
     registry for ADR, layer and enforcement.
   - Any other rule id is an ansible-lint built-in: source `L0 lint:<id>`.
   - If the checker cannot run (missing tool, syntax error), record it as the
     first finding and continue with steps 4–5.
4. **Community review.** Delegate a CoP review to the ai-forge
   `/ansible-cop-review` command (module `ansible-collection-standards`) if it
   is installed; otherwise review against the CoP good practices yourself.
   Source: `L0 cop:<section>`. Drop duplicates of step 3.
5. **Organization heuristics.** For each selected rule with
   `verifiability: heuristic`, inspect the content and judge it. Cite the
   rule and explain the evidence.
6. **Deprecations.** Look for constructs removed or deprecated in the
   ansible-core version targeted by the instance (for example `include`,
   `with_*` loops, bare module names, `key=value` arguments in YAML tasks).
   For collections, the ai-forge `remove-deprecations` skill can help.
7. **Current behavior** (when the audit prepares a modernization; method
   decision GAC-0010). Record what the content does **today**, which is what
   the Builder must preserve:
   - **Observed** — if the original can still run on some runtime (for
     example an older ansible-core), run it on a disposable host of the
     instance's test platform (`manifest.yml` → `test_platform`), twice, and
     record the resulting state and what the second run changes.
   - **Described** — otherwise, describe it from the code and mark it *to be
     confirmed by a human*.
   Say which one it is. Code that fails to load or run is a behavior too
   (for example, a feature that has never worked on current hosts).
8. **Classify** every finding: rule · source layer · enforcement ·
   verifiability · location · fix · effort (S/M/L).
9. **Report.** Fill [templates/audit-report.md](templates/audit-report.md)
   (or `<instance>/templates/audit-report.md` if the instance overrides it).
   Save it where the user asks; default: `reports/audit-<scope>-<date>.md`.
10. **Remediation plan.** End with ordered steps for the Builder, the
    deviations from current behavior they imply, and ask whether the user
    accepts them.

## Workflow — platform

1. Scope: AAP organization, teams, templates or the whole platform.
2. Resolve governance with content type `platform` (rules in area `PLAT`).
3. Delegate to aap-skills through the AAP MCP Server:
   `aap-platform-health-check`, `aap-effective-access-review`.
4. Compare the results with the `PLAT` rules (naming, approved EEs, access).
5. Report with the same template, target `platform`.

## Severity

| Finding | Severity |
|---------|----------|
| Violates a `block` rule, or content fails to load / run | High |
| Violates a `warn` rule, or a heuristic rule with security impact | Medium |
| `advise` rules, style | Low |

## Must not

- Modify the audited content or live systems (writing the report is expected).
- Report a finding without a rule id or L0 reference.
- Hide checker failures.
