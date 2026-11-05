# Success contract — modernize `manage-users` into `manage_users`

> Written after the fact: GAC-0010 postdates this example. In the method's
> order, this contract is approved **before** the Builder starts.

| | |
|---|---|
| **Kind** | modernize |
| **Repository** | `ex-01-modernize-ansible-manage-users` · classification: prod |
| **Governance** | acme@2026.11 |
| **Status** | approved by the architect (approval simulated in this example) |

## What must stay the same

Current behavior **observed** by running the original on ansible-core 2.15 in a
UBI 9 container ([characterization](../characterization/README.md)).

| # | Behavior today | Obtained | Check after the change | Result |
|---|----------------|----------|------------------------|--------|
| B1 | Creates the listed groups with their gid | observed | Same groups and gids | ✅ met |
| B2 | Creates the listed users with uid, primary group, secondary groups and comment | observed | Same passwd and group membership | ✅ met |
| B3 | A user without secondary groups gets none | observed | Same | ✅ met |
| B4 | Removes the users and groups in the removal lists | observed | Same | ✅ met |
| B5 | A second run changes nothing in what it manages | observed | Second run `changed=0` | ✅ met |

## Deviations — approved

| # | Today | After | Why | Approved |
|---|-------|-------|-----|----------|
| D1 | Each user's password defaults to its user name | No default: required input, `no_log` | R-SEC-001 (ADR-0003) | yes |
| D2 | The password policy **never runs** (the custom module does not import on Python 3) | Policy applied with `ansible.builtin.user`: no password aging, no account expiry, inactivity removed for existing users | Feature restored; R-CODE-002 | yes |
| D3 | — (policy never ran) | Users created in the run must change their password at first login (not re-forced on later runs) | Intent of `Force-chg-pwd`, made idempotent | yes |
| D4 | Role `manage-users`, unprefixed variables | Role `manage_users`, variables `manage_users_*` (migration table in the PR) | `lint:role-name`, `lint:var-naming`, CoP | yes — breaking |
| D5 | Custom `library/chage` module | Removed | R-CODE-002 | yes |
| D6 | No argument validation | `meta/argument_specs.yml` | R-DOC-001 | yes |

## Verification

| | |
|---|---|
| Process rules that apply | R-TEST-001 (prod repository) |
| B1–B5 | Characterization: original vs modernized on the same starting state — ✅ |
| D1–D3 | Same comparison, deviations as listed — ✅ |
| Idempotency (R-TEST-001) | [tests/test.yml](../after/tests/test.yml) on the test platform: run 1 `changed=6`, run 2 `changed=0`, check mode `changed=0` — ✅ |
| Test platform | podman, `ubi9/ubi`, no privilege escalation (ADR-0007) |
| Out of scope | Password hashing strategy for `update_password: always` (left as `on_create` default) |
