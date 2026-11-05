# acme.linux_baseline.login_banner

Manages the login banner shown to users: the message of the day
(`/etc/motd`, after login) and the pre-login banners (`/etc/issue` for local
consoles, `/etc/issue.net` for network logins when sshd `Banner` points to
it). Every file gets the same text, preceded by an `ansible_managed` comment.

## Requirements

- ansible-core 2.16 or later.
- Privilege escalation when managing files under `/etc`.

## Role variables

Declared in [meta/argument_specs.yml](meta/argument_specs.yml) and validated
at runtime.

| Variable | Default | Description |
|----------|---------|-------------|
| `login_banner_text` | Generic "authorized use only" notice | Banner text — use the text approved by your legal or security team |
| `login_banner_motd_enabled` | `true` | Manage `login_banner_motd_path` |
| `login_banner_issue_enabled` | `true` | Manage `login_banner_issue_path` |
| `login_banner_issue_net_enabled` | `true` | Manage `login_banner_issue_net_path` |
| `login_banner_motd_path` | `/etc/motd` | Message of the day file |
| `login_banner_issue_path` | `/etc/issue` | Local pre-login banner file |
| `login_banner_issue_net_path` | `/etc/issue.net` | Network pre-login banner file |
| `login_banner_owner` / `login_banner_group` | `root` / `root` | File ownership |
| `login_banner_mode` | `"0644"` | File permissions |

This role does not change the sshd configuration; pointing sshd `Banner` to
`/etc/issue.net` is out of scope.

## Example

```yaml
- name: Apply the corporate login banner
  hosts: all
  become: true
  roles:
    - role: acme.linux_baseline.login_banner
      vars:
        login_banner_text: "{{ acme_legal_banner }}"
```

## Check mode and idempotency

Supports check mode. A second run with the same variables reports no
changes (verified by the `integration_login_banner` Molecule scenario, as
ACME R-TEST-001 requires for production repositories).

## License

GPL-3.0-or-later
