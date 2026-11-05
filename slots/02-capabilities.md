# Slot 02 — Capabilities

**What does the agent know how to do?**

## What belongs here

Skills, commands and agents: the method's modes and community skill libraries.

**Not here:** Organization rules (they are data, read through Knowledge); tools that change what the agent sees (Input).

## Admission criteria

Answer in the harness-adoption ADR (`type: harness-adoption`, `slot: capabilities`):

| Question | Why it matters |
|----------|----------------|
| What does it touch: knowledge, actions, systems, data leaving the machine? | Data egress or model routing makes it a security decision |
| Project or user scope? | User-scope tools cannot be verified by the instance: `recommended` at most |
| How is it pinned (commit, release + checksum)? | No unpinned dependency enters L0 (GAC-0002) |
| What can it conflict with, and who wins? | Precedence must be explicit before adoption |
| How is it verified after install? | An adoption nobody can verify is documentation, not governance |
| How is it removed? | Every adoption must be reversible |

## Mechanism

`lola-module` — installed with Lola in each assistant's format, pinned to a commit; `module_content` selects the right directory; `expect_skills` lists what must end up installed.

## Verification

Every expected skill is present after install. *Installed without error is not installed the right thing*: aap-skills first installed its developer tool instead of its five platform skills.

## Reference adoption in acme

| Entry | ADR | What |
|-------|-----|------|
| `gac-modes` | [ADR-0001](../examples/acme/adr/ADR-0001-adopt-community-baseline.md) | Auditor, Builder, Librarian, Operator, gac-governance |
| `ai-forge` | [ADR-0001](../examples/acme/adr/ADR-0001-adopt-community-baseline.md) | 5 modules: standards, role, content development, documentation, SDLC |
| `aap-skills` | [ADR-0009](../examples/acme/adr/ADR-0009-adopt-aap-skills.md) | 5 platform skills (health, access, upgrade readiness, supportability, topology) |

## Caution

Skills from different sources may overlap; the instance decides which modules to enable (`modules`) rather than installing everything.
