# Audit report — ansible-manage-users (role `manage-users`)

| | |
|---|---|
| **Mode** | Auditor · Target: content |
| **Scope** | Repository `ansible-manage-users` @ `f1fe002`: role at the repository root (`defaults/`, `meta/`, `tasks/`, `library/chage`, `examples/`, `README.md`). `governance/` submodule excluded. |
| **Governance** | acme@2026.11 · method 0.1 · scope: role / prod (listed under `promotion_paths.prod`) |
| **Date** | 2026-11-21 |

Effective governance applied:

```text
Governance: acme@2026.11 · method 0.1 · scope: role / prod
L0: CoP good practices (fb5fcd6) + ansible-lint profile production (v26.10.1) apply where L1 is silent
L1/L2 rules:
  R-CODE-001 (ADR-0001, organization, block, mechanical): loop_control.loop_var = __<role>_<name>; never implicit item
  R-DOC-001  (ADR-0002, organization, block, mechanical): meta/argument_specs.yml with a main entry point for every public variable
  R-SEC-001  (ADR-0003, organization, advise, heuristic, locked): no default passwords/tokens/keys; required + no_log; values from vault
  R-CODE-002 (ADR-0004, organization, advise, heuristic): command/shell only when no module exists, commented gap, guards, changed_when
  R-COLL-001 (ADR-0005, organization, block, mechanical, locked): nothing from community.general in prod
  R-TEST-001 (ADR-0006, organization, advise, heuristic): automated idempotency test (run twice, second run changed=0)
Exceptions: none for this repository (EXC-001 is scoped to firewall_legacy)
Checker: ansible-lint -c governance/examples/acme/gates/ansible-lint.yml -i governance/examples/acme/gates/ansible-lint-ignore.txt
Test platform: podman · registry.access.redhat.com/ubi9/ubi:latest · become false
```

## Summary

| Severity | block | warn | advise |
|----------|-------|------|--------|
| Count | 13 | 1 | 11 |

By severity: **High 13** (block rules, or content fails to load), **Medium 2** (1 `warn` + R-SEC-001, a heuristic rule with security impact), **Low 10**.

| Source | Findings |
|--------|----------|
| L0 (community) | 21 |
| L1 (organization) | 4 |
| L2 (domain) | 0 |

Compliant: **R-COLL-001** (no `community.general` usage) and **R-CODE-002** (the role has no `command`/`shell` tasks today).

**The checker exits on its first finding.** On the original repository ansible-lint stops at `role-name` and reports nothing else. Everything else under lint findings comes from linting a temporary copy renamed `manage_users` (a scratch directory), as the Auditor procedure requires. That copy had **58 failures + 1 warning**, all of them hidden behind the role name.

**The role cannot run on a current ansible-core.** `include:` has been removed from ansible-core, so `tasks/main.yml` fails to load. The bundled `library/chage` module is Python 2-only, so it fails on any Python 3 target, which covers every supported EL release.

## Findings

Enforcement for L0 lint rules: `block` means the rule is fatal under the `production` profile, so the checker fails. `warn` means it is reported but not fatal. L0 CoP and ai-forge guidance is not gated (`advise`).

| # | Rule | Source | Enforcement | Verifiability | Location | Finding | Suggested fix | Effort |
|---|------|--------|-------------|---------------|----------|---------|---------------|--------|
| 1 | lint:role-name | L0 lint | block | mechanical | `meta/main.yml:2` (repo dir `ansible-manage-users`) | The computed role name `silvinux.manage-users` is invalid (hyphen). ansible-lint aborts and hides every other finding. | Set `galaxy_info.role_name: manage_users` and `namespace:` in `meta/main.yml`. Update consumers to the new role name. | S |
| 2 | lint:schema[tasks] (`include` removed from ansible-core) | L0 lint / ansible-core | block | mechanical | `tasks/main.yml:2,5,8,11,14` | Uses `include:`, which has been removed from ansible-core. The role fails to load. | Use `ansible.builtin.include_tasks` (conditional) or `ansible.builtin.import_tasks`. | S |
| 3 | Python 2 target support removed (ansible-core ≥ 2.17 runs modules on Python 3 only) | L0 ansible-core | block (fails to run) | mechanical | `library/chage:142`, `:181`, `:224` | `except IOError, (errno, strerror):` is a SyntaxError in Python 3, and `dict.iteritems()` does not exist there. The module also uses a wildcard `module_utils` import. Every `chageuser` task fails on Python 3 hosts. | Remove the module and see #23. Do not port it. | M |
| 4 | R-CODE-001 | L1 ADR-0001 | block | mechanical | `tasks/addgroup.yml:2`, `adduser.yml:2`, `chageuser.yml:9,15,21`, `delgroup.yml:2`, `deluser.yml:2` | 7 loops use the implicit `item` (via `with_dict`) without `loop_control.loop_var`. | `loop: "{{ manage_users_x \| dict2items }}"` + `loop_control: {loop_var: __manage_users_user}` (or `_group`). | S |
| 5 | R-DOC-001 | L1 ADR-0002 | block | mechanical | `meta/` (no `argument_specs.yml`) | The role has no argument specs. Its public interface is undocumented and unvalidated. | Create `meta/argument_specs.yml` with a `main` entry point covering every public variable (type, required, default, description, choices for `chg_pwd`/`update_pwd`). | M |
| 6 | lint:no-free-form | L0 lint | block | mechanical | `tasks/addgroup.yml:2`, `adduser.yml:2`, `chageuser.yml:9,15,21`, `delgroup.yml:2`, `deluser.yml:2` | 7 tasks pass `key=value` strings to modules. In `addgroup`/`delgroup`/`adduser`/`deluser` this is a YAML scalar of `k=v` pairs under the module key. | Use YAML mappings for module arguments. | S |
| 7 | lint:fqcn[action-core] | L0 lint | block | mechanical | `tasks/addgroup.yml:3`, `adduser.yml:3`, `delgroup.yml:3`, `deluser.yml:3` | Bare module names `group`/`user`. | `ansible.builtin.group`, `ansible.builtin.user`. | S |
| 8 | lint:literal-compare | L0 lint | block | mechanical | `tasks/main.yml:2,5,8,11,14` | `when: deluser == true` etc. | `when: manage_users_deluser \| bool` (after the rename in #17). | S |
| 9 | lint:name[missing] | L0 lint | block | mechanical | `tasks/main.yml:2,5,8,11,14` | 5 unnamed include tasks. | Name them, e.g. `Include user deletion tasks`. | S |
| 10 | lint:schema[meta] | L0 lint | block | mechanical | `meta/main.yml:7` | `min_ansible_version: 2.2` is not a string and is obsolete. | Set `min_ansible_version: "2.16"` (or the instance's target core), quoted. | S |
| 11 | lint:meta-no-tags | L0 lint | block | mechanical | `meta/main.yml:18,19` | Galaxy tags `user-management`, `group-management` contain hyphens. | `usermanagement`, `groupmanagement`. | S |
| 12 | lint:yaml (comments ×4, truthy ×3, indentation ×2, trailing-spaces ×9) | L0 lint | block | mechanical | `defaults/main.yml:11-16,19`; `meta/main.yml:9,11`; `tasks/addgroup.yml:3-5`; `delgroup.yml:3-5`; `chageuser.yml:8,21,22` | Formatting: `###comment`, `yes`/`no` booleans, list indentation, trailing whitespace. | `true`/`false`, `# comment`, 2-space indented lists, strip trailing spaces. | S |
| 13 | lint:syntax-check[specific] | L0 lint | block | mechanical | `examples/example1.yml:8`, `examples/example2.yml:8` | The examples reference role `manage-users`, which cannot be resolved. Both example playbooks fail syntax check. | Reference the final FQCN/role name. Move the examples into README or `examples/` with a `roles_path` note. | S |
| 14 | lint:jinja[spacing] | L0 lint | warn | mechanical | `defaults/main.yml:10` | `{{item.key }}`. | Moot once #15 is fixed (the default is removed). | S |
| 15 | R-SEC-001 | L1 ADR-0003 (locked) | advise | heuristic | `defaults/main.yml:10`; `tasks/adduser.yml:2-8`; `examples/example1.yml:16`; `examples/example2.yml:27-34` | **Default password = username** (`password: "{{item.key }}"`). This is exactly the case ADR-0003 describes: every account gets a guessable credential unless the consumer overrides it. The `Create Users` task has no `no_log`, so passwords and hashes appear in output with `-v`. The examples ship predictable (`<user>_4ns1bl3`) and plaintext passwords. | Remove the default. Make the password a required per-user input declared in argument specs, sourced from Vault. Add `no_log: true` to the user task. Examples must use vaulted variables. | M |
| 16 | R-TEST-001 | L1 ADR-0006 | advise | heuristic | repository (no `molecule/` or `tests/`) | No automated idempotency test. Also, `password_hash('sha512')` without a fixed salt combined with `update_pwd: always` (`examples/example2.yml:22`) yields a new hash on every run, so the second run reports `changed`. | Add a Molecule scenario (podman, ubi9) with the `idempotence` step. Use a stable salt or accept pre-hashed passwords. | M |
| 17 | cop:roles/naming (variable prefix) | L0 CoP | advise | mechanical | `defaults/main.yml:3-19`; consumed vars `users_list`, `groups_list`, `users_del_list`, `groups_del_list`, `shell`, `password` | No role variable carries the role prefix. Generic names (`password`, `shell`, `adduser`) collide with other roles and inventory vars. | Prefix every public variable with `manage_users_` and internal ones with `__manage_users_`. | M |
| 18 | cop:roles/naming (tags) | L0 CoP | advise | mechanical | `tasks/addgroup.yml:8`, `adduser.yml` (none), `delgroup.yml:8`, `deluser.yml:8` | Tags contain spaces (`"delete groups"`), lack the role prefix and are applied inconsistently. | `manage_users_groups`, `manage_users_users`, … applied consistently. | S |
| 19 | cop:naming (task names) | L0 CoP | advise | mechanical | `tasks/chageuser.yml:9,15,21` | Task names are option labels (`Force-chg-pwd`) rather than imperative sentences with the sub-task prefix. | `chageuser \| Force password change at next login`, etc. | S |
| 20 | cop:module-usage (`loop` over `with_*`) | L0 CoP | advise | mechanical | all 7 loops (same lines as #4) | `with_dict` is legacy. | `loop:` + `dict2items` (done together with #4). | S |
| 21 | cop:roles/idempotency & check mode | L0 CoP | advise | heuristic | `library/chage:134`; `tasks/adduser.yml:8,13` | `chage` sets `supports_check_mode=False`, so its tasks are skipped in `--check` and show nothing. See #16 for the non-idempotent password hashing. | Covered by #16 and #23. | S |
| 22 | cop:documentation | L0 CoP | advise | heuristic | `README.md:8,14-29,37-39` | The README documents variables that do not exist (`loadlist`, `nonexpiring`, `showlists`). It omits real ones (`chageuser`, `del_home`, `users_list`, `groups_list`, `users_del_list`, `groups_del_list`) and claims Ansible 2.2. It has no inline example, idempotency statement or rollback notes. | Regenerate from argument specs with an example playbook, the idempotency designation and supported platforms. | S |
| 23 | ai-forge:authoring-priorities (prefer `ansible.builtin`; custom modules last resort) | L0 ai-forge (ansible-content-development) | advise | heuristic | `library/chage` | A vendored third-party module (GPLv3, no RETURN, untyped argspec) duplicates capabilities that `ansible.builtin.user` provides: `password_expire_max`, `password_expire_min`, `password_expire_warn`, `expires` (-1 removes), and on newer cores `password_expire_account_disable` (inactive days). Only "force change at next login" (`chage -d 0`) has no builtin equivalent. | Replace with `ansible.builtin.user` options. For `-d 0`, use one `ansible.builtin.command` task that complies with R-CODE-002 (gap comment, guard reading `getent shadow`, `changed_when`). Builder must confirm option availability against the target core. | M |
| 24 | cop:yaml (document start) | L0 CoP | advise | mechanical | `tasks/chageuser.yml:1` | Missing `---`. | Add `---`. | S |
| 25 | cop:playbook (fact gathering / privilege) | L0 CoP | advise | heuristic | `examples/example1.yml:3-6`, `examples/example2.yml:3-6` | The examples connect as `remote_user: root` with `become` commented out, and gather full facts the role never uses. | `become: true` with a non-root user. Set `gather_facts: false` unless facts are needed. | S |

### Deprecations (step 6) — cross-reference

| Construct | Where | Status | Finding |
|-----------|-------|--------|---------|
| `include:` | `tasks/main.yml` | Removed from ansible-core | #2 |
| Python 2 module code | `library/chage` | Python 2 targets unsupported in current cores | #3 |
| `with_dict` | 7 loops | Legacy, replaced by `loop` | #20 |
| `key=value` args in YAML tasks | 7 tasks | Discouraged | #6 |
| Bare module names | 4 tasks | Discouraged | #7 |
| `createhome` | `tasks/adduser.yml:15` | Alias of `create_home` (still accepted) | use canonical name with #6 |

## Current behavior

How obtained: **described** (from the code, not executed, at the requester's instruction "do not run it"). **To be confirmed by a human.**

| # | Behavior today | Notes |
|---|----------------|-------|
| B0 | On current ansible-core the role **does not load**: `include:` in `tasks/main.yml` is a parse error. | No host is changed. |
| B1 | On a core old enough to accept `include`, the order is fixed: delete users → delete groups → add groups → add users → chage. Each step is gated by a boolean (`deluser`, `delgroup`, `addgroup`, `adduser`, `chageuser`), and all default to `false`. | With the defaults the role is a no-op. |
| B2 | `addgroup`: creates each key of `groups_list` with an optional `gid`. `delgroup`: removes each key of `groups_del_list` (`gid` is passed but irrelevant). | |
| B3 | `adduser`: creates each key of `users_list` with mandatory `uid`, optional `group`, `groups` (append), `home`, `comment` (`com`), the role-wide `shell` (default `/bin/bash`), `createhome: yes` and `non_unique: no`. | Fails if a user lacks `uid`. |
| B4 | **The password defaults to the username**, hashed with sha512 and a random salt. `update_pwd` defaults to `on_create`, so existing users' passwords are not changed. With `update_pwd: always` the password is rehashed and reported `changed` on every run. | Security issue (#15) and idempotency issue (#16). |
| B5 | `deluser`: removes each key of `users_del_list`. Home directories are kept unless `del_home: true`. | |
| B6 | `chageuser`, mode chosen by `chg_pwd` (default `Force-chg-pwd`): **Force-chg-pwd** sets last change = 0 (forces a password change at next login). **Force-chg-pwd-Non-expiring** also sets inactive -1, min 0, max 99999 and expire -1. **Do-not-chg-pwd-Non-expiring** sets the aging values without forcing a change. | On Python 3 targets the bundled `chage` module **has never worked** (SyntaxError), so B6 does not happen today on EL8+. On Python 2 targets: idempotent while the shadow values are unchanged. Once a user changes their password, `Force-chg-pwd` forces a change again on the next run. |
| B7 | Not supported in check mode for the chage step (tasks skipped). | |

## Exceptions applied

| Exception | Rule | Scope | Expires |
|-----------|------|-------|---------|
| — | — | — | — |

None. No exception in `exceptions/register.yml` matches `ansible-manage-users`, and no remediation step requires one.

## Remediation plan

Ordered steps for the Builder. Each step should leave the checker greener than the previous one.

| Step | Action | Findings | Effort |
|------|--------|----------|--------|
| 1 | Fix the role identity: `role_name: manage_users` and `namespace` in `meta/main.yml`, valid galaxy tags, quoted `min_ansible_version`, platform list. Re-run the checker on the real repository to confirm it no longer aborts. | #1, #10, #11 | S |
| 2 | Define the interface: rename all public variables to `manage_users_*` and write `meta/argument_specs.yml` (`main` entry point: types, choices, defaults; passwords required, no default). | #5, #17, #15 (part) | M |
| 3 | Rewrite `tasks/main.yml` with named `ansible.builtin.include_tasks` and `\| bool` conditions. | #2, #8, #9 | S |
| 4 | Rewrite the group/user task files: FQCN, YAML-mapping arguments, `loop` + `dict2items` with `__manage_users_*` loop vars, prefixed tags, imperative names, `no_log: true` on the user task, canonical option names. | #4, #6, #7, #12, #18, #19, #20, #24, #15 (part) | M |
| 5 | Remove `library/chage`. Implement aging with `ansible.builtin.user` options. Implement "force change at next login" with one R-CODE-002-compliant `ansible.builtin.command` task (gap comment, guard on current `lastchg`, `changed_when`). | #3, #21, #23 | M |
| 6 | Make password handling idempotent: accept pre-hashed passwords or use a stable per-user salt. | #16 (part), B4 | S |
| 7 | Add a Molecule scenario (podman, `ubi9/ubi`, `become: false`) that creates groups/users, applies aging, deletes them and runs `idempotence`. Record the second-run result. | #16 | M |
| 8 | Fix the examples (vaulted passwords, `become`, no full facts, correct role name) and regenerate README from argument specs. | #13, #15 (part), #22, #25 | S |
| 9 | Run the checker from the repository root without paths until there are no blocking findings. | all | S |

**Deviations from current behavior these steps imply. Please accept or reject each:**

1. **D1: Role and variable names change** (`manage-users` → `manage_users`, `adduser` → `manage_users_adduser`, …). Every existing playbook that calls the role must be updated. Breaking change. Optionally, a compatibility shim could map old names for one release.
2. **D2: There is no default password.** Users without an explicit (vaulted) password cause argument-spec validation to fail, instead of silently getting `password = username` (B4).
3. **D3: Password aging starts working on Python 3 hosts.** Today `chageuser` fails there (B6), so enabling it after remediation will change shadow aging for real for the first time.
4. **D4: `update_pwd: always` stops reporting `changed` every run.** This holds only if a stable salt or pre-hashed input is adopted (step 6). Consumers passing plaintext may need to switch to hashes.
5. **D5: Re-forcing a password change.** With `Force-chg-pwd`, today every run after a user changes their password forces a new change (on Python 2 hosts). Builder must choose: (a) keep this behavior, or (b) force only on account creation (recommended, idempotent). Please choose.
6. **D6: Tags renamed** (`"create groups"` → `manage_users_groups`, …). Any `--tags` usage must be updated.

Do you accept D1–D4 and D6, and which option do you choose for D5?

## Verification

- Checker on the original repository (`ansible-lint -c governance/examples/acme/gates/ansible-lint.yml -i governance/examples/acme/gates/ansible-lint-ignore.txt`, run from the repo root): **aborted** on `role-name` and reported nothing else.
- Checker on the temporary copy renamed `manage_users` (same command, from the copy root): **58 failures, 1 warning** across 10 files, under profile `production` (ansible-lint 26.10.1). Of these, R-CODE-001 ×7 and R-DOC-001 ×1 are organization rules. R-COLL-001 reported 0.
- The role was **not executed**, at the requester's instruction.
- The Python 3 incompatibility in `library/chage` was established by reading the code (Python 2-only syntax on line 142). No interpreter was run.
- Baseline recorded: **no**.
