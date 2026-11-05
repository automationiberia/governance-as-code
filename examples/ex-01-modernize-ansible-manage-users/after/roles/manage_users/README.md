# manage_users

Add and remove local users and groups, and set the password aging policy.
Each action runs only when its switch is enabled.

Modernized from [silvinux/ansible-manage-users](https://github.com/silvinux/ansible-manage-users)
under the ACME governance — see the
[EX-01 walkthrough](../../../README.md).

## Requirements

- ansible-core 2.16 or later.
- Privilege escalation on the managed hosts (user management needs root).

## Role variables

The interface is declared in [meta/argument_specs.yml](meta/argument_specs.yml)
and validated at runtime.

| Variable | Default | Description |
|----------|---------|-------------|
| `manage_users_delete_users` | `false` | Remove users in `manage_users_users_absent` |
| `manage_users_delete_groups` | `false` | Remove groups in `manage_users_groups_absent` |
| `manage_users_add_groups` | `false` | Create groups in `manage_users_groups` |
| `manage_users_add_users` | `false` | Create users in `manage_users_users` |
| `manage_users_set_password_policy` | `false` | Apply `manage_users_password_policy` to `manage_users_users` |
| `manage_users_groups` | `{}` | `name: {gid}` |
| `manage_users_groups_absent` | `{}` | `name: {}` |
| `manage_users_users` | `{}` | `name: {uid, group, groups, home, com, shell, password}` — all keys optional |
| `manage_users_users_absent` | `{}` | `name: {}` |
| `manage_users_password` | — (**no default**) | Initial password for users without a `password` key. From a vault |
| `manage_users_default_shell` | `/bin/bash` | Shell for users without a `shell` key |
| `manage_users_update_password` | `on_create` | `on_create` or `always` |
| `manage_users_create_home` | `true` | Create home directories |
| `manage_users_non_unique` | `false` | Allow non-unique UIDs |
| `manage_users_remove_home` | `false` | Remove home directories on user removal |
| `manage_users_password_policy` | `force_change` | `force_change`, `force_change_non_expiring` or `non_expiring` |

Password policies:

| Policy | Effect |
|--------|--------|
| `force_change` | Users **created in this run** must change their password at next login |
| `force_change_non_expiring` | As above, plus no password aging (min 0, max 99999), no inactivity period, no account expiry |
| `non_expiring` | No password aging, no inactivity period, no account expiry |

## Example

```yaml
- name: Oracle accounts
  hosts: db_servers
  become: true
  roles:
    - role: manage_users
      vars:
        manage_users_add_groups: true
        manage_users_add_users: true
        manage_users_set_password_policy: true
        manage_users_password_policy: force_change_non_expiring
        manage_users_password: "{{ vault_oracle_initial_password }}"
        manage_users_groups:
          oinstall: {gid: 1200}
          dba: {gid: 1205}
        manage_users_users:
          oracle: {uid: 9000, group: 1200, groups: "1205", com: "User Oracle"}
```

## Testing

[tests/test.yml](../../tests/test.yml) creates, modifies and removes users on a
disposable host; run it twice — the second run must report `changed=0`.

## License

GPL-3.0-only (as the original role).
