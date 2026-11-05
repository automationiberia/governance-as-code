<!--# cspell: ignore SSOT CMDB -->
# AGENTS.md

Ensure that all practices and instructions described by
<https://raw.githubusercontent.com/ansible/ansible-creator/refs/heads/main/docs/agents.md>
are followed.

## Governance as Code

This repository is governed by the **acme** governance instance. Repository classification: **prod** (from the instance manifest).

On conflict with the ansible-creator guidance above, the governance instance wins (it resolves precedence between community bases and ACME decisions).

| | |
|---|---|
| Instance | `../../acme/` (in a real repository: a `governance/` submodule) |
| Version | `2026.11` |
| Method | Governance as Code `0.1` |

Before any technical work:

1. Pick a mode: `/audit` (review), `/build` (create or modernize),
   `/librarian` (change governance), `/operate` (AAP). Declare it.
2. Resolve effective governance with the `gac-governance` skill. Apply only
   the rules it returns, plus the community baseline.
3. Run the checker before claiming a task is done, from the repository root
   and without paths:
   `ansible-lint -c ../../acme/gates/ansible-lint.yml -i ../../acme/gates/ansible-lint-ignore.txt`
4. Never decide rules. If governance blocks the task, propose an exception
   or an ADR with `/librarian`.
5. Never commit, push or change live systems without explicit request.
