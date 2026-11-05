# acme.lab_tools.troubleshooting_packages

Installs troubleshooting packages on lab and development hosts.

| Variable | Default | Description |
|----------|---------|-------------|
| `troubleshooting_packages_list` | `[strace, tcpdump, lsof, bind-utils]` | Packages to install |

```yaml
- name: Lab hosts
  hosts: lab
  become: true
  roles:
    - role: acme.lab_tools.troubleshooting_packages
```
