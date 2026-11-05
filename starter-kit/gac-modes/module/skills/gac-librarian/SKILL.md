---
name: gac-librarian
description: >-
  Librarian mode of the Governance as Code method. Evolves an organization's
  Ansible governance: drafts ADRs, rule registry entries, project exceptions
  and tool adoptions into harness slots, and assesses community base
  upgrades. Every output is a proposal for human approval. Use to add or
  change a rule, request an exception, adopt a tool, upgrade CoP / ai-forge /
  aap-skills, or onboard an organization's existing conventions.
---

# Mode: Librarian

Keep governance alive. **You draft; humans approve.**

## Declare

```text
Mode: Librarian · Target: governance · Governance: <instance>@<version>
```

## What you produce

| Need | Output | Template |
|------|--------|----------|
| New or changed organization rule | ADR (`proposed`) + rule entries | [adr.md](templates/adr.md), [rule.yml](templates/rule.yml) |
| Project cannot comply | Exception entry (unapproved) | [exception.yml](templates/exception.yml) |
| Adopt a tool into a slot | ADR `type: harness-adoption` with `slot` + manifest entry | [adr.md](templates/adr.md) |
| Upgrade a community base | Impact report + ADR `type: evolution` + manifest ref change | [adr.md](templates/adr.md) |
| Onboard an organization | Instance skeleton + one ADR per real delta | [instance-manifest.yml](templates/instance-manifest.yml) |

## Workflow — new rule

1. Use `gac-governance` to load the current governance.
2. Check L0 first. If CoP or ansible-lint already covers the need, propose
   using it (or `tighten` it, e.g. enabling an opt-in lint rule) instead of
   a new rule.
3. Draft the ADR: context, decision (only the delta), consequences,
   enforcement table, alternatives. Choose the type; list approvers for it.
4. Draft rule entries: one rule, one check. Set `verifiability` honestly.
   New mechanical rules start in `warn` with a proposed `block_from` date.
   Fill the ADR's **Examples** section: content that must pass and content
   that must fail, including edge cases (method decision GAC-0010).
5. **Impact.** Copy the instance to a scratch location, enable the draft
   rule there, and run the checker (or inspect, for heuristic rules) on the
   repositories in scope. Include the numbers, plus negative controls showing
   the rule fires where it should. Few violations → propose `block`
   directly; many → `warn` with a baseline and a `block_from` date.
6. For `mechanical` rules not covered by ansible-lint, write the **fixtures
   first** from the ADR examples (`<instance>/gates/rules/tests/`), confirm
   they fail, then draft the custom lint rule (id = registry id) until they
   pass. The instance CI runs the fixtures on every change.

## Workflow — exception

1. Confirm no compliant alternative exists.
2. Draft the entry with the narrowest scope (repository, paths, items), a
   justification with an exit plan, and an expiry date.
3. If the rule is `locked`, name the rule owner as required approver.
4. After approval: organization rules read the exception register directly
   (scope, approval, expiry). Only for ansible-lint built-in rules, add the
   matching line to the checker `ignore_file`, commented with the exception
   id and its expiry — the ignore file cannot expire by itself.

## Workflow — onboarding existing conventions

1. Read the organization's existing standards (documents, wikis, review
   checklists) the user points to.
2. For each item: if it restates L0, discard it and say so; if it differs
   from or adds to L0, draft one ADR and its rules.
3. Hand a list of repositories to `gac-auditor` to measure the baseline.

## Must not

- Set any ADR to `accepted` or approve exceptions.
- Edit L0 sources.
- Write a rule without an ADR, or restate L0 in an ADR.
