# Slot 03 — Integrations

**Which systems can the agent touch?**

## What belongs here

MCP servers and other connectors to live systems: AAP, ticketing, CMDB.

**Not here:** Direct API calls or CLIs invoked by the agent outside an approved connector.

## Admission criteria

Answer in the harness-adoption ADR (`type: harness-adoption`, `slot: integrations`):

| Question | Why it matters |
|----------|----------------|
| What does it touch: knowledge, actions, systems, data leaving the machine? | Data egress or model routing makes it a security decision |
| Project or user scope? | User-scope tools cannot be verified by the instance: `recommended` at most |
| How is it pinned (commit, release + checksum)? | No unpinned dependency enters L0 (GAC-0002) |
| What can it conflict with, and who wins? | Precedence must be explicit before adoption |
| How is it verified after install? | An adoption nobody can verify is documentation, not governance |
| How is it removed? | Every adoption must be reversible |

## Mechanism

`mcp-server` — registered in the assistant's project configuration; credentials come from environment variables, never from the repository; read-only first.

## Verification

The server is registered with the expected endpoint. Connectivity can only be checked when an endpoint and credentials are configured.

## Reference adoption in acme

| Entry | ADR | What |
|-------|-----|------|
| `aap-mcp-server` | [ADR-0010](../examples/acme/adr/ADR-0010-aap-mcp-server.md) | AAP MCP Server, system monitoring toolset, token from `AAP_MCP_TOKEN` (read-only user) |

## Caution

Any write capability is a security decision; RBAC in the target system is the real limit, the agent's instructions are not.
