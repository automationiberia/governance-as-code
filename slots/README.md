# Slot catalog

Eight fixed extension points of the AI harness ([concept](../docs/concepts/slots.md), [GAC-0005](../adr/GAC-0005-harness-slots.md)).
Every tool enters a slot through an ADR in the owning layer and an entry in the instance manifest;
`gac-setup` applies and verifies every entry ([SETUP](../starter-kit/SETUP.md)).

| # | Slot | Question | Mechanism | Reference adoption (acme) |
|---|------|----------|-----------|---------------------------|
| 01 | [Knowledge](01-knowledge.md) | What does the agent know? | `reference` | `community-baseline`, `organization-governance` |
| 02 | [Capabilities](02-capabilities.md) | What does the agent know how to do? | `lola-module` | `gac-modes`, `ai-forge`, `aap-skills` |
| 03 | [Integrations](03-integrations.md) | Which systems can the agent touch? | `mcp-server` | `aap-mcp-server` |
| 04 | [Input](04-input.md) | What information reaches the agent, and how much? | `hook` + pinned binary | `rtk` |
| 05 | [Output](05-output.md) | How does the agent communicate? | `reference` + `lola-module` | `artifact-templates`, `i-have-adhd` |
| 06 | [Guardrails](06-guardrails.md) | What is the agent prevented from doing, or checked on, while it works? | `hook` | `checker-on-edit` |
| 07 | [Execution](07-execution.md) | Where does the agent run, and with which credentials? | `test-platform` | `test-platform` |
| 08 | [Evolution](08-evolution.md) | How does the system improve over time? | `instance-check` | `exception-watch` |

Evidence that all eight are applied and verified in a clean repository: [EX-04](../examples/ex-04-harness-slots/README.md).
