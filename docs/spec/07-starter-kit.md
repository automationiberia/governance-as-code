# 08 — Starter kit

> Status: draft v0.2

Reusable pieces provided by the method so an organization starts working on
day one. No organization rules are shipped, and no custom CLI or server is
built: the method relies on AI assistants and standard tools.

## Components

| Component | What it is | Location |
|-----------|------------|----------|
| **Mode module `gac-modes`** | Lola module with the Auditor, Builder, Librarian and Operator skills and the `/audit`, `/build`, `/librarian`, `/operate` commands | [starter-kit/gac-modes/](../../starter-kit/gac-modes/) |
| **Pointer** | `AGENTS.md` section for content repositories | [starter-kit/AGENTS.pointer.md](../../starter-kit/AGENTS.pointer.md) |
| **Gate definitions** | pre-commit configuration and CI workflow running the checker | [starter-kit/gates/](../../starter-kit/gates/) |
| **Setup** | Applies and verifies the instance's harness slots in a repository | [starter-kit/setup/](../../starter-kit/SETUP.md) |
| **Hooks** | Guardrail hook: the checker after every edit | [starter-kit/hooks/](../../starter-kit/hooks/gac_checker_on_edit.py) |
| **Templates** | ADR, rule, exception, manifest, audit report, PR body | [templates/](../../templates/) |

## The checker is ansible-lint

| Need | ansible-lint feature |
|------|----------------------|
| L0 rules | Built-in rules and ansible-lint profile (`production`, ...) |
| L1 tightening of L0 | `enable_list` (opt-in rules), stricter ansible-lint profile |
| L1 disabling of L0 | `skip_list`, each entry commented with its ADR |
| Organization rules (`mechanical`) | Custom rules in the instance, loaded with `rulesdir`; rule id = registry id; **also listed in `enable_list`** — with a profile set, ansible-lint unloads every rule outside the profile, including custom ones |
| `warn` enforcement | `warn_list` |
| Exceptions and baseline | Ignore file (`-i`, `--generate-ignore`), each entry commented with its `EXC-` id or baseline date |

Run the checker **without paths**, from the root of the content: passing a
role directory as an argument lints it as a single item and skips its files.

The instance configuration excludes `governance/` (`exclude_paths`): when the
instance lives inside the content repository, its rule fixtures — which fail
on purpose — must not be linted as content.

Organization rules that check a role as a whole are evaluated on the **role
directory** (`matchdir`), not on `tasks/main.yml`: ansible-lint skips every
other rule on a file with a syntax error, which would hide them on the roles
that most need them.

### Organization rules that need context

Rules scoped by promotion path or subject to exceptions read that context
**from the instance**, not from configuration copied into each repository:

- promotion path from `manifest.yml` — unlisted repositories are treated as
  prod (deny by default);
- exceptions from the exception register — scope, approval and **expiry** are
  enforced by the rule itself;
- repository identity from `GAC_REPOSITORY`, set by the CI platform (for
  example `github.event.repository.name`), never by repository content.

The ansible-lint ignore file is kept only for built-in rules. It cannot
express expiry and is shared by every repository using the instance, so the
Librarian and the instance CI review its entries (see [05-gates.md](05-gates.md)).

**Trust boundary.** A workflow file inside the content repository can be
edited by its developers. Making the gate non-bypassable requires
organization-level enforcement on the CI platform (for example required
workflows or rulesets), owned by the platform team.

## How an organization consumes it

```text
  content repository
  ├── AGENTS.md            ← pointer (tier 1)
  ├── .lola-req            ← ai-forge modules @ref · aap-skills @ref · gac-modes @method version
  ├── governance/          ← instance checkout or submodule @instance version
  ├── .pre-commit-config.yaml  ← ansible-lint -c governance/gates/ansible-lint.yml
  └── CI workflow          ← same command, required status check
```

## Versioning

- The starter kit follows the method version (semantic versioning).
- An instance pins the method version in its manifest.
- Breaking method changes require a GAC ADR and a migration note.
