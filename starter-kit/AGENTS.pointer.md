## Governance as Code

This repository is governed by the **<instance>** governance instance.

| | |
|---|---|
| Instance | `<path to instance checkout, e.g. governance/>` |
| Version | `<instance ref>` |
| Method | Governance as Code `<method version>` |

Before any technical work:

1. Pick a mode: `/audit` (review), `/build` (create or modernize),
   `/librarian` (change governance), `/operate` (AAP). Declare it.
2. Resolve effective governance with the `gac-governance` skill. Apply only
   the rules it returns, plus the community baseline.
3. Run the checker before claiming a task is done, from the repository root
   and without paths:
   `ansible-lint -c <instance>/gates/ansible-lint.yml -i <instance>/gates/ansible-lint-ignore.txt`
4. Never decide rules. If governance blocks the task, propose an exception
   or an ADR with `/librarian`.
5. Never commit, push or change live systems without explicit request.
