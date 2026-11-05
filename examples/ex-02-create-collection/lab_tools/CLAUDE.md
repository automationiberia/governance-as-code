# acme.lab_tools

Tools for ACME lab and development hosts. Read [AGENTS.md](AGENTS.md) first: it points to the governance instance.

## Roles

- `troubleshooting_packages` — Install troubleshooting packages on lab and development hosts

## Commands

- Checker: `ansible-lint -c ../../acme/gates/ansible-lint.yml` (from this directory, no paths)
- Build: `ansible-galaxy collection build`
- Sanity: `ansible-test sanity`
- No integration tests (nonprod repository: R-TEST-001 does not apply)
- Changelog: `antsibull-changelog release`

## Rules

Red Hat CoP automation good practices, plus the ACME rules returned by the
`gac-governance` skill.
