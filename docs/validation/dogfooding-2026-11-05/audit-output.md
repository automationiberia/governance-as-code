<!-- Verbatim final output of the clean Claude Code session running /audit -->

Mode: Auditor · Target: content · Governance: acme@2026.11

# Audit report: `roles/manage-users`

| | |
|---|---|
| **Scope** | `roles/manage-users` (repository `ex-01-modernize-ansible-manage-users`) |
| **Governance** | acme@2026.11 · method 0.1 · scope: role / **prod** (the manifest lists this repo under `promotion_paths.prod`) |
| **Date** | 2026-11-05 |

**The role can't load or run on current Ansible**, and it breaks both organization rules that are set to block:
- **Can't load:** `tasks/main.yml` uses `include`, which ansible-core has removed.
- **Can't run on Python 3:** `library/chage` is written in Python 2.
- **Blocking rules broken:** R-CODE-001 (7 loops) and R-DOC-001 (no argument specs).
- **Security:** each user's password defaults to their username.

### Effective governance

```text
L0: CoP good practices + ansible-lint profile production apply where L1 is silent
L1 rules (all 6 apply; every ADR is accepted):
  R-CODE-001 (ADR-0001, block, mechanical): loop_var __<role>_<name>, never implicit item
  R-DOC-001  (ADR-0002, block, mechanical): meta/argument_specs.yml for every public variable
  R-SEC-001  (ADR-0003, advise, heuristic, locked): no default passwords/tokens/keys; required + no_log + vault
  R-CODE-002 (ADR-0004, advise, heuristic): command/shell only with a comment naming the gap, a guard and changed_when
  R-COLL-001 (ADR-0005, block, mechanical, locked): nothing from community.general in prod
  R-TEST-001 (ADR-0006, advise, heuristic): automated idempotency test (Molecule idempotence or a double run)
Exceptions: none apply (EXC-001 covers firewall_legacy only; ignore file is empty)
Checker: ansible-lint -c governance/gates/ansible-lint.yml -i governance/gates/ansible-lint-ignore.txt
```

### Summary

| Severity | High | Medium | Low |
|---|---|---|---|
| Findings | 4 | 7 | 11 |

| Source | Findings |
|---|---|
| L1 organization | 4 (R-CODE-001, R-DOC-001, R-SEC-001, R-TEST-001) |
| L0 community (lint / CoP / ansible-core) | 18 |

Checker result: **failed**, 87 violations repo-wide. About 70 are in `roles/manage-users`; the rest come from `governance/` itself (finding 12).

### Findings

| # | Sev | Rule | Source · enforcement · verifiability | Location | Finding | Fix | Effort |
|---|---|---|---|---|---|---|---|
| 1 | High | `lint:syntax-check[specific]` | L0 lint · gate · mechanical | `tasks/main.yml:2,5,8,11,14` | `include` was removed from ansible-core, so the role fails to load. The syntax error also stops processing of `main.yml`, which hides other findings (see #4). | Use `ansible.builtin.include_tasks` and `when: manage_users_<flag> \| bool` | S |
| 2 | High | Removed/deprecated construct: Python 3 only | L0 ansible-core · mechanical | `library/chage:139` (`except IOError, (errno, strerror)`), `:184` (`iteritems`), bare `import *` | The vendored module is Python 2 code, so it raises a SyntaxError on any Python 3 target. Every `chageuser` task fails. It also has no check mode. | Remove `library/`. Use `ansible.builtin.user` options (`password_expire_max/min/warn`, `password_expire_account_disable`, `expires`). Only "force change at next logon" (`chage -d 0`) has no module; do that with `ansible.builtin.command` under R-CODE-002. | M |
| 3 | High | **R-CODE-001** | L1 ADR-0001 · block · mechanical | `addgroup.yml:7`, `adduser.yml:17`, `chageuser.yml:11,17,23`, `delgroup.yml:7`, `deluser.yml:7` | 7 loops use the implicit `item` variable | `loop_control.loop_var: __manage_users_<name>` | S |
| 4 | High | **R-DOC-001** | L1 ADR-0002 · block · mechanical | `meta/` | There is no `meta/argument_specs.yml`. **The checker misses this:** the rule only inspects `tasks/main.yml`, and that file stops at the syntax error in #1. Confirmed by reading `gates/rules/r_doc_001.py`. | Add a `main` entry point covering every public variable, with types, `choices` for `chg_pwd`/`update_pwd`, and `required` for credentials | M |
| 5 | Medium | **R-SEC-001** | L1 ADR-0003 · advise · heuristic · security | `defaults/main.yml:10` | `password: "{{item.key }}"`, so every account's password equals its username unless the consumer overrides it. This is exactly the case ADR-0003 forbids. | No default; required in argument specs; values from vault; `no_log` | S |
| 6 | Medium | `cop:security` / `lint:no-log-password` | L0 · heuristic | `adduser.yml:17`, `examples/example2.yml` | The loop goes over `users_list`, whose items carry plaintext `pwd`. Ansible prints each loop item in the task output, so the passwords end up in logs. | `loop_control.label: "{{ __manage_users_user.key }}"`; `no_log` on credential tasks | S |
| 7 | Medium | `cop:security` (no secrets in code) | L0 · heuristic | `examples/example2.yml:27-33`, `examples/example1.yml:16` | Plaintext passwords are committed in the examples, and example1 uses a guessable username-based pattern | Use vault placeholders (`"{{ vault_... }}"`) | S |
| 8 | Medium | `cop:roles/idempotency` | L0 · heuristic | `adduser.yml:9` | `password_hash('sha512')` without a salt produces a new hash on every run. With `update_pwd: always` (example2), every user is changed on every run and the password-change date is reset. ADR-0006 cites this exact incident. | Take a pre-hashed value from vault, or pass a stable per-user salt; default to `update_password: on_create` | S |
| 9 | Medium | `lint:role-name` | L0 lint · gate · mechanical | `roles/manage-users` | `manage-users` doesn't match `^[a-z][a-z0-9_]*$`. Because of this, ansible-lint can't compute the `__{role}_` prefix (the error message shows the regex unexpanded) and skips `var-naming[no-role-prefix]`. | Rename to `manage_users` and update the examples. This is a breaking change for consumers. | S |
| 10 | Medium | `lint:var-naming[no-role-prefix]` / `cop:roles/naming` | L0 · mechanical (hidden by #9) | `defaults/main.yml` | Variables have generic, unprefixed names (`password`, `shell`, `adduser`, `non_unique`, …) that can collide with play variables. Not checker-verified: the name-check was hidden and my throwaway copy was blocked. | Prefix every variable with `manage_users_`. Breaking: plan a 2.0 version. | M |
| 11 | Medium | `cop:roles/check-mode` | L0 · heuristic | `library/chage` | The module sets `supports_check_mode=False`, so the role can't run with `--check` | Fixed by #2 | — |
| 12 | Medium | Checker scope (governance gate) | instance gate config | `governance/gates/ansible-lint.yml` | There is no `exclude_paths` for `governance/`, so its fixtures, `test_rules.py` and `exceptions/register.yml` produce 17 R-COLL-001 hits plus syntax and galaxy errors. The checker can never pass in this repo, whatever the role does. | **For the Librarian, not the Builder:** add `exclude_paths: [governance/]` to the gate config, with an ADR reference | S |
| 13 | Low | **R-TEST-001** | L1 ADR-0006 · advise · heuristic | role | There is no Molecule scenario or integration test, so idempotency is unverified (and #8 shows it's broken) | Add `molecule/default` with the `idempotence` step, and show the second-run result in the PR | M |
| 14 | Low | `lint:fqcn[action-core]` | L0 lint · gate | `addgroup.yml:3`, `adduser.yml:3`, `delgroup.yml:3`, `deluser.yml:3`, `chage` | Short module names | Use `ansible.builtin.*` | S |
| 15 | Low | `lint:no-free-form` (deprecated `key=value`) | L0 lint · gate | 7 tasks | `key=value` arguments inside YAML tasks | Use YAML mappings | S |
| 16 | Low | Deprecation: `with_*` loops | L0 cop | all task files | `with_dict` | `loop: "{{ x \| dict2items }}"` | S |
| 17 | Low | `lint:literal-compare` | L0 · hidden by #1 | `tasks/main.yml` | `when: deluser == true` | `\| bool` | S |
| 18 | Low | `cop:tags` | L0 | `addgroup.yml:8`, `delgroup.yml:8`, `deluser.yml:8` | Tags contain spaces (`"create groups"`) | Use snake_case tags with the role prefix | S |
| 19 | Low | `lint:schema[meta]`, `meta-no-tags`, `yaml[indentation]` | L0 lint · gate | `meta/main.yml` | `min_ansible_version: 2.2` is a number, not a string, and outdated; tags contain hyphens; platform `EL: all` | Set a string min version for a current core release, valid tags, explicit EL versions | S |
| 20 | Low | `lint:yaml[*]`, `jinja[spacing]`, `name[play]` | L0 lint · gate | defaults, examples, tasks (~45) | Formatting problems; plays have no names | Reformat | S |
| 21 | Low | `cop:roles/documentation` | L0 | `README.md` | README is stale: it documents variables that don't exist (`loadlist`, `showlists`, `nonexpiring`), omits `chageuser`/`del_home`, and says Ansible 2.2 | Regenerate from the argument specs | S |
| 22 | Low | `cop:task-naming` | L0 | `chageuser.yml` | Task names are mode codes (`Force-chg-pwd`) rather than descriptions | Use descriptive names | S |

### Organization heuristics
- **R-SEC-001: violated** (#5).
- **R-TEST-001: violated** (#13).
- **R-CODE-002: compliant for now.** There are no `command`/`shell` tasks. The vendored `chage` module wraps the binary, though, and once it's removed, the `chage -d 0` task must carry a comment naming the gap ("no module sets lastday"), a guard (check the shadow entry first) and `changed_when`.
- **R-COLL-001: compliant.** Nothing from `community.general` is used. The Builder must keep it that way; community.general has no chage module anyway.

### Exceptions applied
None.

## Remediation plan for the Builder

0. **Prerequisite (Librarian):** exclude `governance/` from the gate config (#12). Without it, "checker passes" can't be shown. S
1. Rename the role to `manage_users` and update the examples (#9). S
2. Fix `tasks/main.yml`: `include_tasks` and `| bool` (#1, #17). S
3. Remove `library/chage`. Move password aging to `ansible.builtin.user` options. Keep one guarded, commented `command: chage -d 0` for "force change at next logon" under R-CODE-002 (#2, #11). M
4. Define the interface: `manage_users_*` variables and `meta/argument_specs.yml`, with the password **required, no default, `no_log`** and `choices` for the modes (#4, #5, #10). M
5. Rewrite the tasks: FQCN, YAML arguments, `loop` + `dict2items`, `loop_var: __manage_users_*`, `label`, pre-hashed or stable-salt passwords, sensible tags and names (#3, #6, #8, #14–16, #18, #22). M
6. Examples: vault placeholders, named plays, `become` (#7, #20). S
7. Fix `meta/main.yml` and regenerate the README (#19, #21). S
8. Add a Molecule scenario with `idempotence` and capture the second run (#13). M
9. Run the checker until there are no blocking findings, and record the result. Steps 1 and 4 rename the role and its variables, which breaks existing consumers; release it as a major version (2.0) with migration notes.

I didn't save this report anywhere, because you asked for no file changes. The skill's default location is `reports/audit-manage-users-2026-11-05.md`.

Do you accept this plan for `/build`? And should step 0 go to `/librarian` first?
