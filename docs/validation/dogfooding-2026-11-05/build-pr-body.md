## Summary

Modernize `roles/manage-users` as `roles/manage_users` so it complies with the
acme governance and the community baseline. This is a **breaking change**: the
role and all its variables are renamed (migration table below).

Before, the governance checker reported **66 failures and 1 warning**. Now it
reports **0 failures and 0 warnings**.

The human architect approved these decisions in advance:

1. Rename the role and add the `manage_users_` prefix to every variable.
2. No default password: it is a required input and `no_log`.
3. Keep the password policy feature, using `ansible.builtin.user` where a module exists.
4. List every behavior change for review (see **Behavior changes**).

What changed:

- `roles/manage-users` → `roles/manage_users` (`git mv`).
- New `meta/argument_specs.yml` that validates every public variable. The per-user
  `password` is `required: true, no_log: true`.
- All tasks rewritten: FQCN, YAML arguments, `loop` with
  `loop_control.loop_var: __manage_users_*`, `import_tasks` replaces the removed
  `include`, `| bool` conditions, role-prefixed task names and tags.
- Bundled `library/chage` module removed. It was Python 2 only
  (`except IOError, (errno, strerror)`, `dict.iteritems`), so the password policy
  could not run on Python 3 targets. Its features are now covered as follows:
  - min/max days and account expiry: `ansible.builtin.user`.
  - inactivity: `ansible.builtin.user`, guarded (see R-CODE-002).
  - "change password at next logon" (`chage -d 0`): no module offers it, so a
    guarded `ansible.builtin.command`.
- Fixed a non-idempotent password hash. `password_hash('sha512')` used a random
  salt, so `update_pwd: always` reported a change and rewrote every password on
  each run.
- README rewritten, with a variable reference and migration table. Examples no
  longer contain plain-text passwords.
- New Molecule scenario `molecule/default` with an `idempotence` step (R-TEST-001).

## Governance

| | |
|---|---|
| **Repository classification** | prod (`promotion_paths.prod`) |
| **Mode(s)** | Builder |
| **Governance** | acme@2026.11 (method 0.1) |

### Rules applied

| Rule | Source | How it was applied |
|------|--------|--------------------|
| R-CODE-001 | L1 ADR-0001 (block) | Every loop sets `loop_control.loop_var: __manage_users_<name>`. This includes the Molecule verify playbook inside the role. No implicit `item` remains. |
| R-DOC-001 | L1 ADR-0002 (block) | `meta/argument_specs.yml` `main` entry point documents every variable with type, default/required and description, including sub-options of the list elements. |
| R-COLL-001 | L1 ADR-0005 (block) | Only `ansible.builtin` is used. Nothing comes from `community.general`. |
| R-SEC-001 | L1 ADR-0003 (advise) | The old default `password: "{{ item.key }}"` (password = user name) is gone. `password` is required per user, `no_log: true` in the spec, `no_log: true` on the create task, and password-policy loops iterate over names only. Examples and tests use vault references or a runtime-generated password. |
| R-CODE-002 | L1 ADR-0004 (advise) | There is one `command` (`chage --lastday 0`). A comment names the missing capability, it is guarded by the shadow entry (only runs when the value is not already `0`) and has `changed_when: true`. `password_expire_account_disable` is guarded because `ansible.builtin.user` always passes `-f` to `usermod` and reports a change each time. |
| R-TEST-001 | L1 ADR-0006 (advise) | `molecule/default` runs converge, then `idempotence` (fails if the second run reports a change), then verify. **Written but not run in this session (podman unavailable).** |
| `lint:role-name` | L0 ansible-lint production | Role renamed to `manage_users`. |
| `lint:fqcn`, `lint:no-free-form`, `lint:yaml`, `lint:meta-no-tags`, `lint:jinja`, `lint:schema`, `lint:syntax-check` | L0 ansible-lint production | Fixed through the rewrite. |
| `cop:roles` (variable prefix, sub-task name prefix, role-prefixed tags, argument validation) | L0 CoP | Applied. |

### Exceptions used

none

### Remaining warnings

none (checker: `Passed: 0 failure(s), 0 warning(s)`, profile `production`)

## Migration table

| Before (`manage-users`) | After (`manage_users`) | Notes |
|-------------------------|------------------------|-------|
| role `manage-users` | role `manage_users` | |
| `addgroup` | `manage_users_addgroup` | |
| `adduser` | `manage_users_adduser` | |
| `chageuser` | `manage_users_chageuser` | |
| `delgroup` | `manage_users_delgroup` | |
| `deluser` | `manage_users_deluser` | |
| `groups_list` (dict `name: {gid}`) | `manage_users_groups_list` (list of `{name, gid}`) | dict → list |
| `users_list` (dict `name: {uid, group, groups, home, com}`) | `manage_users_users_list` (list of `{name, password, uid, group, groups, home, com}`) | dict → list; `password` per user, required |
| `groups_del_list` (dict) | `manage_users_groups_del_list` | list of names |
| `users_del_list` (dict) | `manage_users_users_del_list` | list of names |
| `password` (default `{{ item.key }}`) | `password` key in each user entry | no default |
| `shell` (implicit `/bin/bash`) | `manage_users_shell` | |
| `chg_pwd` | `manage_users_chg_pwd` | same values |
| `update_pwd` | `manage_users_update_pwd` | same values |
| `non_unique` | `manage_users_non_unique` | |
| `createhome` | `manage_users_createhome` | |
| `del_home` | `manage_users_del_home` | |
| tag `create groups` | `manage_users_create_groups` | |
| tag `delete groups` | `manage_users_delete_groups` | |
| tag `delete users` | `manage_users_delete_users` | |
| — | tags `manage_users_create_users`, `manage_users_password_policy` | new |
| `library/chage` | removed | |

## Behavior changes (for review)

**Inputs and validation**

1. **Role name and variables renamed** (decision 1). Existing playbooks fail
   until they are migrated.
2. **Lists replace dicts.** `groups_list` and `users_list` become lists of dicts
   with a `name` key. The delete lists become plain lists of names.
3. **No default password** (decision 2). Before, a user created without
   `password` got **their own user name as password**. Now every entry in
   `manage_users_users_list` must set `password`, or the play fails in argument
   validation.
   - This also applies when only `manage_users_chageuser` is enabled, because it
     reads the same list.
4. **Per-user password replaces the global template.** Templates such as
   `"{{ item.key }}_suffix"` cannot work any more (`item` no longer exists). Put
   one vault value per user instead.
5. **Stricter validation.** Unknown keys in list entries (for example the old
   `pwd`) are rejected. `uid` and `gid` must be integers. `manage_users_chg_pwd`
   and `manage_users_update_pwd` must be one of their documented values.
6. **Boolean switches use `| bool`.** Before, `when: adduser == true` skipped
   string values such as `-e adduser=true`. Now strings like `"true"`/`"yes"`
   enable the function.
7. **Empty `groups`** (`""` or null) is now omitted instead of being passed to
   the user module.
8. **Group deletion no longer passes `gid`.** It had no effect on deletion.

**Passwords**

9. **Deterministic salt.** The SHA-512 salt is derived from
   `inventory_hostname` + user name, instead of a random salt on every run.
   This is what makes `manage_users_update_pwd: always` idempotent. The salt is
   unique per host and user but predictable. **Please confirm this is
   acceptable for security.**
10. **One-off change on first run after upgrade.** With `update_pwd: always`,
    every existing hash is rewritten once (new salt), so the run reports
    `changed`. `usermod -p` also sets the last-change date to today. With the
    `Force-*` policies the role then sets it back to `0` in the same run.
11. **No more password churn.** Before, `update_pwd: always` rewrote passwords on
    every run, and with `Force-chg-pwd` forced a new change at next logon on
    every run. Now that happens only when the given password differs from the
    stored one.

**Password policy**

12. **Bundled `chage` module removed** (decision 3). Aging, expiry and
    inactivity now use `ansible.builtin.user`, and "change at next logon" uses
    the `chage` binary. The resulting shadow fields are the same as before:
    `-I -1 -m 0 -M 99999 -E -1 [-d 0]`.
13. **Missing users fail with a clear message.** `manage_users_chageuser` on a
    user that does not exist fails through an `assert`, as the old module did.
    In check mode the assert is skipped.
14. **Check mode.** Before, the old module did not support check mode and its
    tasks were skipped. Now the policy tasks predict their changes, except the
    `chage -d 0` command, which is skipped.
15. **Policy tasks may create a missing home directory.** They run
    `ansible.builtin.user`, which creates a missing home directory when
    `manage_users_createhome: true`. Before, the policy step never touched home
    directories. **Please confirm.**
16. **Passwords stay out of the output.** The create-users task is `no_log`, and
    the policy loops iterate over names only.

**Tags and requirements**

17. **Tags renamed and added** (see migration table).
18. **Requirements raised.** `min_ansible_version` goes from 2.2 to 2.18
    (`password_expire_account_disable`). `passlib` is needed on the controller
    for `password_hash` on Python ≥ 3.13.
19. **Examples rewritten.** They now reference `vault_manage_users_passwords`
    instead of inline plain-text passwords.

## Verification

- [x] Checker passes (no `block` findings):
      `ansible-lint -c governance/gates/ansible-lint.yml -i governance/gates/ansible-lint-ignore.txt`
      → `Passed: 0 failure(s), 0 warning(s)`, profile `production`. This
      includes ansible-lint's syntax check of the example and Molecule playbooks.
- [ ] Tests required by `TEST` rules for this repository (R-TEST-001):
      the `molecule/default` scenario is written but **not run** (podman was not
      available). Before merge, run `cd roles/manage_users && molecule test` and
      paste the `idempotence` step output (second run, `changed=0`) here.
- [ ] Standalone `ansible-playbook --syntax-check` and a real converge were not
      run in this session (`ansible-playbook` was not permitted).
- [x] Approvals required by `PROC` rules for this repository: none apply.
- [ ] Architect review of behavior changes 9 (deterministic salt) and 15 (home
      directory creation by the policy tasks).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
