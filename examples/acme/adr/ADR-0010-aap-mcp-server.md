---
id: ADR-0010
title: "Register the AAP MCP Server, read-only first"
status: accepted
layer: organization
domain: null
type: harness-adoption
slot: integrations
date: 2026-11-05
approvers: [automation-lead, security, operations]
supersedes: null
superseded_by: null
acts_on:
  - action: add
    target: null
rules: []
---

# ADR-0010: Register the AAP MCP Server, read-only first

> Approval simulated in this example. Admission criteria: [slot catalog](../../../slots/README.md).

## Context

aap-skills act only through the AAP MCP Server. The Operator mode starts read-only.

## Decision

Register the AAP MCP Server in the **Integrations** slot, using the system monitoring toolset. Endpoint and token come from `AAP_MCP_URL` and `AAP_MCP_TOKEN`; the token belongs to a **read-only** AAP user. Status `recommended` until each team has an endpoint.

## Admission

| Criterion | Answer |
|-----------|--------|
| Touches | Live AAP through MCP; data leaves the machine to the AAP endpoint |
| Scope | Project configuration; credentials per user (environment) |
| Pinning | Server version is the AAP deployment's; client config versioned in the repository |
| Conflicts | Writes: forbidden by the read-only token, whatever the agent is told |
| Verification | Server registered; connectivity checked only when an endpoint is configured |
| Removal | Remove the entry and the `.mcp.json` server |

## Consequences

- Applied and verified by `gac-setup` (manifest `slots.integrations`).
- RBAC on the token is the real limit; the Operator's read-only instruction is guidance.
