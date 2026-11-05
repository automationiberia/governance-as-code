# 11 — Worked examples

> Status: draft v0.5 — EX-01 to EX-04 are implemented under
> [examples/](../../examples/); the others are definitions.

All examples use the reference instance **acme**.

## EX-01 — Modernize `ansible-manage-users`

Source: [silvinux/ansible-manage-users](https://github.com/silvinux/ansible-manage-users)
(a copy exists in the first attempt's delivery collection).

**Use case:** UC-04 · **Modes:** Auditor → Builder · **Repository:** prod

Expected audit findings (observed in the current code):

| Finding | Where | Source |
|---------|-------|--------|
| `with_dict` loops (9 tasks) | `tasks/*.yml` | L0 `cop:` loops / modern `loop` |
| Modules without FQCN (`user`, `group`) | `tasks/adduser.yml`, `tasks/addgroup.yml`, ... | L0 `lint:fqcn` |
| Role name with hyphens | role directory | L0 `lint:role-name` |
| Variables without role prefix (`users_list`, `groups_list`) | `defaults/`, `tasks/` | L0 `cop:roles/variable-prefix` |
| Obsolete metadata (`min_ansible_version: 2.2`) | `meta/main.yml` | L0 |
| Custom `library/chage` module (2016) | `library/` | L1 `R-CODE-002` — replaced by `ansible.builtin.user`; two capabilities without a module remain as guarded `command` tasks |
| Password defaults to the user name | `defaults/main.yml` | **L1** acme `R-SEC-001` (ADR-0003) |
| `include` removed in ansible-core 2.16 | `tasks/main.yml` | L0 `lint:deprecated-module` — the role does not load |
| No `meta/argument_specs.yml` | — | L0 `cop:roles/argument-validation` recommends it; **L1** acme `R-DOC-001` (ADR-0002) makes it blocking (`tighten`) |

Expected result: modernized role, checker green, PR draft listing every rule
applied with its source, audit report before and after.

## EX-02 — Create collections with governance wired into the scaffold

**Use case:** UC-01 · **Mode:** Builder

Two collections scaffolded with ai-forge / ansible-creator, with the
organization's pointer, checker hook and CI gate added to what the scaffold
generates. The repository classification decides the difference:
`linux_baseline` is prod, so `R-TEST-001` requires an idempotency test
(Molecule); `lab_tools` is nonprod, so it does not. Gates are the same for
both. Implemented in
[examples/ex-02-create-collection](../../examples/ex-02-create-collection/).

## EX-03 — `community.general` forbidden in production

**Use cases:** UC-08, UC-09 · **Modes:** Librarian, Builder

End to end: need → ADR-0005 → `R-COLL-001` → agent sees it →
checker blocks a violation → project `firewall_legacy` gets `EXC-001` →
gate honors it until expiry. Implemented in
[examples/ex-03-forbid-community-general](../../examples/ex-03-forbid-community-general/).

## EX-04 — Adopt a tool into a slot

**Use case:** UC-10 · **Mode:** Librarian

One real adoption in each of the eight slots, each with a harness-adoption
ADR, applied and verified by the setup and in a fresh assistant session.
Implemented in [examples/ex-04-harness-slots](../../examples/ex-04-harness-slots/).

## EX-05 — Onboard an organization with existing conventions

**Use case:** UC-12 · **Modes:** Librarian, Auditor

Starting from a sample "existing standards" document, show which items become
ADRs (real deltas) and which are discarded (restating L0).
