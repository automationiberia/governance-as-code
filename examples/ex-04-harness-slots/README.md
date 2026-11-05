# EX-04 — All eight harness slots, adopted and verified

**Use case:** UC-10 Adopt a tool into a slot · **Modes:** Librarian (ADRs),
setup · **Governance:** [acme](../acme/)

Until this example the slots existed only on paper: 2 of 8 were adopted and
the setup ignored them. Now every slot has one real adoption in acme — each
with a harness-adoption ADR, pinned, applied by `gac-setup.sh` and verified in a
clean repository and in a fresh AI assistant session.

## The adoptions

| Slot | Entry | ADR | Status | Mechanism | Verified by |
|------|-------|-----|--------|-----------|-------------|
| Knowledge | `community-baseline`, `organization-governance` | [ADR-0008](../acme/adr/ADR-0008-knowledge-sources.md) | required | reference | bases and paths exist; the agent resolved the 6 rules and the repository classification |
| Capabilities | `gac-modes`, `ai-forge` (5 modules), **`aap-skills`** | [ADR-0001](../acme/adr/ADR-0001-adopt-community-baseline.md), [ADR-0009](../acme/adr/ADR-0009-adopt-aap-skills.md) | required | lola-module | expected skills installed (5 + 6 sampled + 5) |
| Integrations | `aap-mcp-server` | [ADR-0010](../acme/adr/ADR-0010-aap-mcp-server.md) | recommended | mcp-server | registered; loaded by the assistant (`failed` to connect: no AAP endpoint — expected) |
| Input | `rtk` (OSS 1.1.0, checksum-verified) | [ADR-0011](../acme/adr/ADR-0011-adopt-rtk-input.md) | recommended | hook + binary | probe `git status` rewritten; the agent's `git status` came back compressed; `ansible-lint` not rewritten |
| Output | `artifact-templates`, `i-have-adhd` | [ADR-0012](../acme/adr/ADR-0012-output-style-and-templates.md) | required / recommended | reference / lola-module | templates exist; style skill installed; precedence "templates win" in `gac-governance` |
| Guardrails | `checker-on-edit` | [ADR-0013](../acme/adr/ADR-0013-checker-on-edit-hook.md) | required | hook | 5 tests; **fired live**: the agent wrote forbidden content, got R-COLL-001 at once and fixed it |
| Execution | `test-platform` | [ADR-0007](../acme/adr/ADR-0007-test-platform.md) | required | test-platform | podman available, UBI 9 image present |
| Evolution | `exception-watch` | [ADR-0014](../acme/adr/ADR-0014-exception-watch.md) | required | instance-check | 7 tests; passes on today's register; runs in the instance CI |

Evidence: [setup output](evidence/setup-output.txt) · [live session](evidence/live-session.md) ·
[demo-repo](demo-repo/README.md) to run the guardrail by hand (seconds).
Catalog with admission criteria: [slots/](../../slots/README.md).

## The guardrail, live

In a fresh Claude Code session, the agent was asked to write a task using
`community.general.ufw` (as a test). Right after the write, the hook answered:

```text
Governance checker: 1 finding(s) in roles/firewall/tasks/main.yml (rule ids starting with R- come from the organization's ADRs):
roles/firewall/tasks/main.yml:3: R-COLL-001: 'community.general.ufw' is forbidden in production content (ACME ADR-0005, repository 'ex-01-modernize-ansible-manage-users'). Use ansible.builtin, ansible.posix or certified collections, or request an exception.
Fix them before continuing, or propose an exception with /librarian.
```

The agent rewrote it with `ansible.posix.firewalld`, added the argument specs
R-DOC-001 requires, and used the `__firewall_` loop prefix of R-CODE-001.

## What building it taught the method

| Finding | Change |
|---------|--------|
| Lola installed aap-skills' **developer tool** instead of its five platform skills; the install "succeeded" | Lola entries declare `module_content` and `expect_skills`; the setup fails when an expected skill is missing |
| Lola could not register i-have-adhd (its `.cursor/` mirror looked like a module) | Same `module_content` option |
| rtk only installs its Claude Code hook globally (user scope) | The same hook is declared per project, so the instance governs it |
| rtk rewrites commands: permission rules see `rtk <cmd>` | Admission condition in ADR-0011: never allow-list `rtk *` |
| rtk advised the agent to run `rtk init -g` (global config) | `RTK_SUPPRESS_HOOK_WARNING` set in the project settings by the setup |
| The checker linted Lola's `.lola/` copies | Excluded in the acme checker configuration |
| The checker output must reach the agent intact | Verified: rtk leaves `ansible-lint` unchanged |
| The setup writes absolute local paths in `.claude/settings.json` | Documented: per-person files, not committed |

## Limits — stated, not hidden

- **Integrations** is configured, not exercised: no AAP endpoint was available.
- **Hooks and MCP registration** are implemented for Claude Code only; other
  assistants get the Lola modules and a "not supported yet" line.
- Hooks are guidance on the developer's machine and can be disabled; the CI
  gate remains the proof.

## Reproduce

```bash
# From the method checkout, on a content repository with the acme instance at governance/
starter-kit/setup/gac-setup.sh --instance <repo>/governance --repo <repo> --with-recommended
```

The last line must read `Slots active: 8/8`.
