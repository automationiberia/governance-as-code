# Slot 04 — Input

**What information reaches the agent, and how much?**

## What belongs here

Tools that shape what the agent reads: output compression, retrieval, memory.

**Not here:** Anything that changes what the agent is allowed to do (Guardrails).

## Admission criteria

Answer in the harness-adoption ADR (`type: harness-adoption`, `slot: input`):

| Question | Why it matters |
|----------|----------------|
| What does it touch: knowledge, actions, systems, data leaving the machine? | Data egress or model routing makes it a security decision |
| Project or user scope? | User-scope tools cannot be verified by the instance: `recommended` at most |
| How is it pinned (commit, release + checksum)? | No unpinned dependency enters L0 (GAC-0002) |
| What can it conflict with, and who wins? | Precedence must be explicit before adoption |
| How is it verified after install? | An adoption nobody can verify is documentation, not governance |
| How is it removed? | Every adoption must be reversible |

## Mechanism

`hook` + pinned binary — a pre-tool hook in the project settings; the binary is downloaded at a pinned release and its checksum verified.

## Verification

A probe command is rewritten as expected; the checker's output is **not** filtered (verified: `ansible-lint` passes through unchanged).

## Reference adoption in acme

| Entry | ADR | What |
|-------|-----|------|
| `rtk` | [ADR-0011](../examples/acme/adr/ADR-0011-adopt-rtk-input.md) | rtk OSS edition 1.1.0: compresses `git`, `ls`, … output; leaves `ansible-lint` untouched |

## Caution

An Input tool may rewrite commands: permission rules then see the rewritten command. Never allow-list the tool's own prefix (e.g. `rtk *`).
