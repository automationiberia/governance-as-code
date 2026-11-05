# Governance as Code — modes

Common working modes for developing Ansible content and operating AAP under
an organization's governance. Organization rules are data in a governance
instance; these modes read them, they never contain them.

## When to use

| Need | Skill | Command |
|------|-------|---------|
| Which rules apply here? | `gac-governance` | — |
| Audit content or AAP state | `gac-auditor` | `/audit` |
| Create or modernize content | `gac-builder` | `/build` |
| Add a rule, request an exception, adopt a tool, upgrade a base | `gac-librarian` | `/librarian` |
| Check jobs, diagnose failures | `gac-operator` | `/operate` |

## Requirements

- A governance instance, referenced from the repository's `AGENTS.md`.
- ai-forge modules (recommended) for Ansible know-how; aap-skills and the AAP
  MCP Server for platform work.
- ansible-lint, to run the checker.

## Always

- Declare the mode at the start of each response.
- Resolve governance before acting; run the checker before finishing.
- Never decide rules; propose them through the Librarian.
