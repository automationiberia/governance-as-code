---
id: ADR-0011
title: "Adopt rtk (OSS edition) to reduce command output"
status: accepted
layer: organization
domain: null
type: harness-adoption
slot: input
date: 2026-11-05
approvers: [automation-lead, security]
supersedes: null
superseded_by: null
acts_on:
  - action: add
    target: null
rules: []
---

# ADR-0011: Adopt rtk (OSS edition) to reduce command output

> Approval simulated in this example. Admission criteria: [slot catalog](../../../slots/README.md).

## Context

Agents read long command outputs (git, ls, tests). Smaller context is cheaper and keeps the agent focused.

## Decision

Adopt **rtk 1.1.0, OSS edition (Apache-2.0)** in the **Input** slot, as a project-level pre-tool hook, binary pinned by release and SHA-256. The proxy daemon (`rtk-proxy`) is **not** adopted: it would route model traffic.

## Admission

| Criterion | Answer |
|-----------|--------|
| Touches | Rewrites shell commands to compress their output; no data leaves the machine (telemetry off by default, not enabled) |
| Scope | Project hook (rtk's own installer only supports user scope for Claude Code; the same hook is declared per project) |
| Pinning | Release v1.1.0, SHA-256 `4dec94a6…8a3e` |
| Conflicts | Permission rules see the rewritten command (`rtk git …`): never allow-list `rtk *`. The checker output must stay complete — verified: `ansible-lint` is not rewritten |
| Verification | A probe `git status` is rewritten to `rtk git status` |
| Removal | Remove the entry; the hook and binary are dropped on the next setup |

## Consequences

- Applied and verified by `gac-setup` (manifest `slots.input`).
- Status `recommended`: teams opt in.
