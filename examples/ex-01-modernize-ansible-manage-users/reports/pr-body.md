## Summary

Modernize `manage-users` into `manage_users` so it loads on supported
ansible-core versions and complies with ACME governance. Remediates every
finding in [audit-before.md](audit-before.md).

**Breaking change:** role and variable names change (migration below).

## Governance

| | |
|---|---|
| **Repository classification** | prod |
| **Mode(s)** | Auditor → Builder |
| **Governance** | acme@2026.11 |

### Success contract

[success-contract.md](success-contract.md) — approved (simulated in this example).

| Item | Status |
|------|--------|
| B1–B5 — preserved behavior (characterization) | met |
| D1–D6 — deviations | approved |

### Rules applied

| Rule | Source | How it was applied |
|------|--------|--------------------|
| R-CODE-001 | L1 ADR-0001 | All loops use `loop` + `dict2items` with `loop_var: __manage_users_*` |
| R-DOC-001 | L1 ADR-0002 | `meta/argument_specs.yml` declares all 16 public variables |
| R-SEC-001 | L1 ADR-0003 (locked) | No default password; `manage_users_password` (or per-user `password`) is required, `no_log`, enforced by an assert |
| R-CODE-002 | L1 ADR-0004 | `library/chage` removed. `ansible.builtin.user` handles password aging and expiry. Two `command` tasks remain where no module exists (`chage -d 0`, idempotent `chage -I -1`), each commented and guarded |
| `role-name`, `var-naming` | L0 lint / CoP | Role `manage_users`; all variables prefixed `manage_users_` |
| `deprecated-module` | L0 lint | `include` → `ansible.builtin.import_tasks` |
| `fqcn`, `no-free-form`, `name`, `literal-compare` | L0 lint | FQCN, YAML arguments, named tasks, `\| bool` |
| `cop:roles/prefix-task-names`, tags | L0 CoP | `<file> \| <task>` names; tags `manage_users_<action>` |
| R-TEST-001 | L1 ADR-0006 (tightens `cop:roles/idempotency`) | [tests/test.yml](../after/tests/test.yml) run twice: second run and check mode report `changed=0` |

### Exceptions used

None.

### Remaining warnings

None.

### Migration

| Before | After |
|--------|-------|
| role `manage-users` | role `manage_users` |
| `adduser` / `addgroup` / `deluser` / `delgroup` / `chageuser` | `manage_users_add_users` / `_add_groups` / `_delete_users` / `_delete_groups` / `_set_password_policy` |
| `users_list` / `users_del_list` | `manage_users_users` / `manage_users_users_absent` (same dict format) |
| `groups_list` / `groups_del_list` | `manage_users_groups` / `manage_users_groups_absent` |
| `password` (default: user name) | `manage_users_password` (**no default**) or per-user `password` key |
| `shell` | per-user `shell` key or `manage_users_default_shell` |
| `chg_pwd`: `Force-chg-pwd` / `Force-chg-pwd-Non-expiring` / `Do-not-chg-pwd-Non-expiring` | `manage_users_password_policy`: `force_change` / `force_change_non_expiring` / `non_expiring` |
| `update_pwd`, `non_unique`, `createhome`, `del_home` | `manage_users_update_password`, `_non_unique`, `_create_home`, `_remove_home` |

### Behavior changes — need reviewer approval

1. **The password policy is applied for the first time.** The original's
   custom `chage` module fails to import on Python 3, so its policy never ran
   on modern hosts ([characterization](../characterization/README.md)). With
   the modernized role, existing users lose their inactivity period (e.g.
   `orainfra`: 30 days → none) and users created in the run must change their
   password at first login. Forced change applies only to users created in
   the run (the original code, had it run, would have re-forced it on every
   run).
2. **No default password.** The role fails fast if a new user has no password.
3. `append` is used only when `groups` is given (ansible-core rejects
   `append` without `groups`; found during testing, not by the audit).

## Verification

- [x] Checker passes — `ansible-lint -c ../../acme/gates/ansible-lint.yml`: 0 findings (ansible-lint profile `production`)
- [x] Tests required by `TEST` rules (R-TEST-001) — [tests/test.yml](../after/tests/test.yml) on a UBI 9 container: run 1 `changed=6`, run 2 `changed=0`, check mode `changed=0`
- [x] Characterization — same uid, gid, groups, comments, group and user creation/removal as the original; deviations limited to the approved list above ([results](../characterization/README.md))
- [ ] Approvals required by `PROC` rules — none for this repository; 1 reviewer; behavior changes above
