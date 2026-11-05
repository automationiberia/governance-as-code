# Slot 06 — Guardrails

**What is the agent prevented from doing, or checked on, while it works?**

## What belongs here

Hooks that check or block actions, permission policies, secret scanning.

**Not here:** The proof of compliance — that is the gates (GAC-0006). Guardrails give earlier feedback; they do not replace CI.

## Admission criteria

Answer in the harness-adoption ADR (`type: harness-adoption`, `slot: guardrails`):

| Question | Why it matters |
|----------|----------------|
| What does it touch: knowledge, actions, systems, data leaving the machine? | Data egress or model routing makes it a security decision |
| Project or user scope? | User-scope tools cannot be verified by the instance: `recommended` at most |
| How is it pinned (commit, release + checksum)? | No unpinned dependency enters L0 (GAC-0002) |
| What can it conflict with, and who wins? | Precedence must be explicit before adoption |
| How is it verified after install? | An adoption nobody can verify is documentation, not governance |
| How is it removed? | Every adoption must be reversible |

## Mechanism

`hook` — a post-tool hook in the project settings that runs the same checker as CI.

## Verification

The hook is registered; the setup probes it; tests cover clean files, violations and ignored paths.

## Reference adoption in acme

| Entry | ADR | What |
|-------|-----|------|
| `checker-on-edit` | [ADR-0013](../examples/acme/adr/ADR-0013-checker-on-edit-hook.md) | After every edit of Ansible content, the checker runs and the agent sees the findings of that file |

## Caution

Hooks run on the developer's machine and can be disabled there: they are guidance, never the guarantee.
