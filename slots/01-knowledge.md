# Slot 01 — Knowledge

**What does the agent know?**

## What belongs here

Reference material the agent reads to decide: community good practices, the organization's decisions and rules, internal standards and documentation.

**Not here:** Prompts or skills that *do* things (Capabilities); live data from systems (Integrations).

## Admission criteria

Answer in the harness-adoption ADR (`type: harness-adoption`, `slot: knowledge`):

| Question | Why it matters |
|----------|----------------|
| What does it touch: knowledge, actions, systems, data leaving the machine? | Data egress or model routing makes it a security decision |
| Project or user scope? | User-scope tools cannot be verified by the instance: `recommended` at most |
| How is it pinned (commit, release + checksum)? | No unpinned dependency enters L0 (GAC-0002) |
| What can it conflict with, and who wins? | Precedence must be explicit before adoption |
| How is it verified after install? | An adoption nobody can verify is documentation, not governance |
| How is it removed? | Every adoption must be reversible |

## Mechanism

`reference` — the source exists, is pinned (bases) or versioned (instance paths), and is reachable from the repository pointer.

## Verification

The referenced bases and paths exist; `gac-governance` resolves them for a task.

## Reference adoption in acme

| Entry | ADR | What |
|-------|-----|------|
| `community-baseline` | [ADR-0008](../examples/acme/adr/ADR-0008-knowledge-sources.md) | CoP good practices + ansible-lint profile, pinned in `bases` |
| `organization-governance` | [ADR-0008](../examples/acme/adr/ADR-0008-knowledge-sources.md) | manifest, ADRs, rules, exceptions of the instance |

## Caution

Knowledge is never copied into skills or prompts (GAC-0004): it is read where it lives.
