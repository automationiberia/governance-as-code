# Audit report — roles/manage-users

| | |
|---|---|
| **Mode** | Auditor · Target: content |
| **Scope** | `before/roles/manage-users` ([silvinux/ansible-manage-users@f1fe002](https://github.com/silvinux/ansible-manage-users/tree/f1fe002eef914234f43d2637604a60e8a663ab8d)) |
| **Governance** | acme@2026.11 · method 0.1 · scope: role / prod |
| **Date** | 2026-11-04 |

## Effective governance used

```text
Governance: acme@2026.11 · method 0.1 · scope: role / prod
L0: CoP good practices + ansible-lint profile production apply where L1 is silent
L1 rules:
  R-CODE-001 (ADR-0001, L1, block, mechanical): loop_control.loop_var = __<role>_<name>; never implicit item
  R-DOC-001  (ADR-0002, L1, block, mechanical): meta/argument_specs.yml with every public variable
  R-SEC-001  (ADR-0003, L1, advise, heuristic, locked): no default credentials; required + no_log, from a vault
  R-CODE-002 (ADR-0004, L1, advise, heuristic): command/shell only without a module; comment the gap; idempotent
  R-TEST-001 (ADR-0006, L1, advise, heuristic): prod roles have an automated idempotency test
Exceptions: none
Checker: ansible-lint -c ../../acme/gates/ansible-lint.yml
```

## Summary

15 grouped findings: **high** 1–6 (role does not load, guessable passwords,
blocking organization rules) · **medium** 7–12 · **low** 13–15.

| Source | Occurrences |
|--------|-------------|
| L0 — ansible-lint | 52 (+11 hidden, see note) |
| L0 — CoP review | 3 |
| L1 — acme | R-CODE-001 ×7, R-DOC-001 ×1, R-SEC-001 ×1, R-CODE-002 ×1, R-TEST-001 ×1 |

Raw checker output: [checker-before.txt](checker-before.txt) (60 lines).

> **Note.** The invalid role name stops ansible-lint from computing the
> expected variable prefix. Linting a copy renamed to `manage_users` reveals
> **11 more** `var-naming[no-role-prefix]` findings (every variable in
> `defaults/main.yml`).

## Findings

| # | Rule | Source | Enf. | Verif. | Location | Finding | Fix | Effort |
|---|------|--------|------|--------|----------|---------|-----|--------|
| 1 | `deprecated-module`, `schema[tasks]` | L0 lint | block | mech. | `tasks/main.yml` ×5 | `include` was removed in ansible-core 2.16: **the role does not load** on any supported version | `ansible.builtin.import_tasks` | S |
| 2 | R-SEC-001 | L1 ADR-0003 (locked) | advise | heur. | `defaults/main.yml:10` | Default `password: "{{ item.key }}"` sets **each user's password to its user name** | No default; required input from a vault, `no_log` | S |
| 3 | `role-name` | L0 lint, `cop:roles/naming` | block | mech. | role directory | `manage-users` has a dash; hides other checks | Rename to `manage_users` | S |
| 4 | R-DOC-001 | L1 ADR-0002 (tightens `cop:roles/argument-validation`) | block | mech. | `meta/` | No `argument_specs.yml` | Add argument specs for every public variable | M |
| 5 | R-CODE-001 | L1 ADR-0001 (tightens `lint:loop-var-prefix`) | block | mech. | `tasks/*.yml` ×7 | Implicit `item` in every loop (`with_dict`) | `loop` + `dict2items` + `loop_var: __manage_users_*` | S |
| 6 | R-CODE-002 / `cop:roles/idempotency` | L1 ADR-0004 + L0 | advise | heur. | `library/chage`, `tasks/chageuser.yml` | Unmaintained custom module (2016). By reading the code, `Force-chg-pwd` resets the last change date on every run. **Characterization showed the module does not even import on Python 3** (Python 2 syntax): the password policy has not been applied on any modern host | Use `ansible.builtin.user` aging options; `command` only where no module exists, guarded and commented. Decide whether to enforce a policy that, in practice, does not exist today | M |
| 7 | `var-naming[no-role-prefix]` | L0 lint, `cop:roles/naming-parameters` | block | mech. | `defaults/main.yml` ×11 (hidden) | Variables without role prefix (`adduser`, `password`, `users_list`, ...) | Prefix with `manage_users_` (breaking: migration table) | M |
| 8 | `no-free-form` | L0 lint | block | mech. | `tasks/*.yml` ×7 | `key=value` arguments | YAML arguments | S |
| 9 | `fqcn` | L0 lint | block | mech. | `tasks/*.yml` ×4 | `user`, `group` without FQCN | `ansible.builtin.*` | S |
| 10 | `name[missing]`, `literal-compare` | L0 lint | block | mech. | `tasks/main.yml` ×5 each | Unnamed includes; `== true` | Name tasks; `\| bool` | S |
| 11 | `schema[meta]`, `meta-no-tags` | L0 lint | block | mech. | `meta/main.yml` | `min_ansible_version: 2.2` (number, obsolete); invalid galaxy tags | `"2.16"`; valid tags | S |
| 12 | `syntax-check`, R-TEST-001 | L0 lint + L1 ADR-0006 | block / advise | mech. / heur. | `examples/*.yml` ×2 | Examples reference a role that cannot be resolved; no automated idempotency test | Replace with a test playbook run twice (second run `changed=0`) | M |
| 13 | `cop:roles/prefix-task-names` | L0 CoP | advise | heur. | `tasks/*.yml` | Sub-task files without task name prefix | `<file> \| <task>` | S |
| 14 | `cop:roles/naming-parameters` (tags) | L0 CoP | advise | heur. | `tasks/*.yml` | Tags with spaces, not prefixed (`"create groups"`) | `manage_users_<action>` | S |
| 15 | `yaml`, `jinja[spacing]` | L0 lint | block/warn | mech. | ×19 | Trailing spaces, comments, truthy `yes`/`no`, indentation | Reformat | S |

## Exceptions applied

None.

## Remediation plan

1. Rename the role to `manage_users`; re-run the checker to surface hidden findings.
2. Replace `include` with `ansible.builtin.import_tasks`; name tasks; use `| bool`.
3. Rewrite tasks with FQCN, YAML arguments, `loop` + `dict2items`, `loop_var: __manage_users_*`, prefixed task names and tags.
4. Prefix every public variable with `manage_users_`; document the migration.
5. Remove the default password; require it (argument specs, `no_log`).
6. Replace `library/chage` with `ansible.builtin.user` aging options. For the two capabilities without a module (force change at next login, remove inactivity period) use guarded, commented `command` tasks; force change only for users created in the run (**behavior change — needs approval**).
7. Add `meta/argument_specs.yml`; update `meta/main.yml`.
8. Replace `examples/` with a test playbook run twice (R-TEST-001: the repository is prod).

Repository classification: **prod** (from the acme manifest) — R-TEST-001 applies.

## Verification

- Checker: 60 findings (+11 hidden by finding 3).
- Baseline recorded: no (role is being remediated, not baselined).
