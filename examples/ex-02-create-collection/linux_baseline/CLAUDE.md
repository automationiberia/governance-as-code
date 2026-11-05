# acme.linux_baseline

Baseline configuration for ACME production Linux hosts. Read [AGENTS.md](AGENTS.md) first: it points to the governance instance.

## Roles

- `login_banner` — Manage the login banner in /etc/motd, /etc/issue and /etc/issue.net

## Commands

- Checker: `ansible-lint -c ../../acme/gates/ansible-lint.yml` (from this directory, no paths)
- Build: `ansible-galaxy collection build`
- Sanity: `ansible-test sanity`
- Integration: `molecule test -s integration_login_banner` (from `extensions/`) — required by R-TEST-001 (prod repository)
- Changelog: `antsibull-changelog release`

## Rules

Red Hat CoP automation good practices, plus the ACME rules returned by the
`gac-governance` skill.
