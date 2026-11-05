<!-- Verbatim final output of the clean Claude Code session running /build -->

Mode: Builder · Target: content · Governance: acme@2026.11

I rebuilt `roles/manage-users` as `roles/manage_users`. The governance checker now passes with no findings, down from 66 failures and 1 warning. The idempotency test is written but not run (no podman), and the role itself was never executed here, because `ansible-playbook` isn't allowed in this session. Nothing is committed; the rename is staged with `git mv`.

**Governance applied** (scope: role in a prod repo; no exceptions apply to this repo; no process rules beyond R-TEST-001):

| Rule | Level | How it was applied |
|---|---|---|
| R-CODE-001 (ADR-0001) | block | Every loop uses a `__manage_users_*` variable. This includes the Molecule verify playbook, since it sits inside the role. |
| R-DOC-001 (ADR-0002) | block | New `meta/argument_specs.yml` describes every variable, including the fields of each user and group entry. |
| R-COLL-001 (ADR-0005) | block | Only `ansible.builtin` modules are used. |
| R-SEC-001 (ADR-0003) | advise | The old default made each user's password their own user name. Now every user entry needs a `password` (required, `no_log`). Examples use vault references, and the test generates its password at run time. |
| R-CODE-002 (ADR-0004) | advise | There is one `command` task, `chage --lastday 0` ("change password at next logon"), because no module offers it. It has a comment naming the gap, only runs when the value isn't already 0, and sets `changed_when`. |
| R-TEST-001 (ADR-0006) | advise | `molecule/default` runs the role twice; the second run must report no changes. Not run. |

**What changed in the role:**
- **Removed the bundled `chage` module.** It was Python 2 only, so the password policy couldn't work on modern hosts. Aging and expiry now use `ansible.builtin.user`.
- **Guarded one `ansible.builtin.user` setting.** In ansible-core 2.22, `password_expire_account_disable` reports a change on every run, so it only runs when there's actually something to change.
- **Fixed an idempotency bug.** The old password hash used a random salt, so `update_pwd: always` changed every password on every run. The salt is now derived from the host name and user name, so the hash is the same between runs.
- **Rewrote tasks, README and examples.** Tasks use full module names and `import_tasks` instead of the removed `include`. The README includes the migration table. The examples no longer contain plain-text passwords.

**Breaking change:** the role and all its variables are renamed. `users_list` and `groups_list` change from dicts to lists, and the delete lists become plain lists of names. The full migration table is in the README and in `reports/pr-body.md`.

**Behavior changes:** all 19 are listed in `reports/pr-body.md`. Two need your architect's decision:
- **#9:** the new salt is unique per host and user but predictable. Please confirm that's acceptable for security.
- **#15:** the password-policy step can now create a missing home directory when `manage_users_createhome: true`. Before, it never touched home directories.

**Still to do before merge:**
- Run `cd roles/manage_users && molecule test` and paste the second-run output (`changed=0`) into the PR, as R-TEST-001 asks.
- Run a real converge or `ansible-playbook --syntax-check`; the only syntax check so far is the one built into the checker.
- No changelog fragment was created, since there's no `changelogs/` directory.
- Delete `governance/gates/rules/__pycache__/`, which my checker runs left behind. I wasn't allowed to remove it.
