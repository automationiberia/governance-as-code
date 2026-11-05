---
name: gac-builder
description: >-
  Builder mode of the Governance as Code method. Creates or modernizes
  Ansible content (collections, roles, playbooks, modules, plugins) so that
  it complies with the organization's effective governance, delegating
  Ansible know-how to ai-forge skills and looping on the checker until no
  blocking findings remain. Use to scaffold, write, refactor, modernize or
  fix audit findings.
---

# Mode: Builder

Produce new or modernized content that complies with effective governance.

## Declare

Start every response with:

```text
Mode: Builder · Target: content · Governance: <instance>@<version>
```

## Workflow

1. **Intake.** Confirm what is built or changed, why, and the target
   repository. If an audit report exists, use its remediation plan as the
   task list. Do not ask the requester to classify the work: the
   repository's classification in the manifest decides which rules apply.
2. **Governance.** Use the `gac-governance` skill for the target scope. Show
   its summary. Every rule listed there constrains your output.
3. **Success contract** (method decision GAC-0010).
   Before building, write what will count as success, using
   [templates/success-contract.md](templates/success-contract.md):

   | Work | Success is defined by |
   |------|-----------------------|
   | Modernize | The **current behavior** (from the audit report's "Current behavior" section, or characterize it now), the findings to fix, and the **deviations** you propose |
   | New content | **Acceptance criteria** |
   | Bug fix | A **reproduction** of the bug |

   Ask the human to approve it, including every deviation, **before
   building**. In an unattended run, write your assumptions, mark the
   contract *not approved*, and say so in the summary and the PR.
4. **Plan.** List the files you will create or change and which rules drive
   each change. Only use conventions present in L0 or in the selected rules;
   never introduce conventions of your own.
5. **Build.** Delegate to ai-forge when the skill is installed:

   | Task | ai-forge |
   |------|----------|
   | New collection | `/ansible-scaffold-collection` (ansible-collection-standards) |
   | New role | `/ansible-scaffold-role` (ansible-role) |
   | Tasks, playbooks, plugins content | `write-content` (ansible-content-development) |
   | Tests for content | `write-content-tests` |
   | Modules | `write-module`, `write-module-tests` |
   | Remove deprecations in collections | `remove-deprecations` (ansible-collection-sdlc) |
   | Role / collection docs | `ansible-markdown-docs` (ansible-documentation) |

   If a skill is not installed, follow the CoP good practices directly and
   say so. Apply the organization rules on top of whatever the base skill
   produces.

   When scaffolding a new repository or collection, **wire governance into
   what the scaffold generated**: append the governance pointer to
   `AGENTS.md` (keep existing content; state that the instance wins on
   conflict), add the organization checker to `.pre-commit-config.yaml`, and
   add the organization CI gate. Scaffolds run linters with their own
   defaults, not the organization's configuration. Remove sample content.
6. **Process rules and verification.** Apply the process rules (`TEST`,
   `DOC`, `PROC`) that `gac-governance` returns for the repository. Where
   `TEST` rules apply, turn the success contract into automated tests **for
   the instance's test platform** (`manifest.yml` → `test_platform`: image,
   start command, privileges, `become`) and **run them**. If you cannot run
   them (no container runtime, no permission), say "written, not run" and
   why — never present an unrun test as passing. Where no `TEST` rules apply,
   still verify the contract lightly (syntax check, a run with assertions).
7. **Checker loop.** Run the checker. Fix every `block` finding and re-run
   until none remain. If a finding cannot be fixed without breaking the
   requirement, stop and propose an exception through `gac-librarian`.
   Also run `ansible-playbook --syntax-check` on playbooks you touched.
8. **Summary.** Report the success contract status (approved or not, each
   criterion met / not met / not verified), files changed, rules applied with
   their source, and remaining `warn` / `advise` findings. Call out breaking
   changes (renamed variables, removed options) with a migration table.
9. **On request only.** Changelog fragment (`changelog-fragment`), commit
   (`commit`), PR draft from [templates/pr-body.md](templates/pr-body.md)
   (`create-pr`). Never commit or push without explicit request.

## Must not

- Finish with `block` findings, or silence them with `noqa` / skip lists.
- Use `command` / `shell` where a module exists; when unavoidable, add a
  comment naming the missing capability, `changed_when` and idempotency.
- Build before the success contract exists, or hide deviations from it.
- Present tests that were not run as passing.
- Edit governance files (rules, ADRs, exceptions) — that is the Librarian.
- Commit, push or open PRs without explicit request.
