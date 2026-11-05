# Layers — who decides

A **layer** is a source of authority. Layers are stacked: a higher layer may
add to, override, disable or tighten what a lower layer says. A lower layer
never sees or changes a higher one.

```text
  L3  Project        ← exceptions only
  L2  Domain         ← optional
  L1  Organization   ← the organization's decisions
  L0  Community      ← the baseline, consumed as-is
```

## L0 — Community

The baseline everybody starts from.

| Examples | CoP Automation Good Practices, ai-forge, aap-skills, any community tool adopted into a slot |
|---|---|
| **Owned by** | Upstream maintainers |
| **May** | Provide rules, skills, knowledge and tools |
| **May not** | Be edited, forked or patched by an instance |
| **How it is consumed** | Pinned to a specific version (commit, tag or release). Upgrading is a deliberate L1 decision. |

When L1 says nothing about a topic, L0 applies.

## L1 — Organization

The organization's own governance. This is where Governance as Code does its
real work.

| Examples | Naming conventions, collection allow/deny lists, playbook procedure, approval flows, which community tools are adopted |
|---|---|
| **Owned by** | The organization's automation governance (e.g. automation lead + stakeholders per decision type) |
| **May** | Add rules, override L0, disable L0 rules, mark rules as **locked** (red lines), adopt or reject tools for any slot |
| **May not** | Restate L0 content. L1 contains only the **delta** ([GAC-0003](../../adr/GAC-0003-organization-layer-is-a-delta.md)). |
| **Change mechanism** | Organization ADRs → rule registry entries |

## L2 — Domain (optional)

A subdivision of the organization with legitimately different needs.

| Examples | Network automation team, Windows platform team, a regulated business unit |
|---|---|
| **Owned by** | The domain's lead, within L1 limits |
| **May** | Add rules, tighten L1 rules, choose among options L1 allows |
| **May not** | Relax a **locked** L1 rule |
| **Change mechanism** | Domain ADRs, reviewed by L1 |

Most organizations start without L2. Add it only when a domain repeatedly
needs the same exceptions.

## L3 — Project

A single repository or initiative.

| Examples | `firewall-legacy` needs one forbidden module until a migration ends |
|---|---|
| **Owned by** | The project owner |
| **May** | Request **exceptions**: scoped, justified, with an owner and an expiry date |
| **May not** | Create new rules. If a project needs a rule, it is proposed to L1 or L2. |
| **Change mechanism** | Exception register entries; exceptions to locked rules require approval from the rule owner in L1 |

## Why layers and not a single standard

- The community moves on its own pace; pinning it at L0 keeps upgrades
  deliberate and auditable.
- Organizations differ; L1 captures only what is different, so it stays small
  and its intent stays visible.
- Projects have real constraints; L3 exceptions make them explicit and
  temporary instead of silent and permanent.

See [precedence.md](precedence.md) for how layers are resolved.
