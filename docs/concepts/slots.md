# Slots — what is governed in the harness

The **harness** is everything around an AI model that shapes how it works:
what it knows, what it can do, what it can touch, what it sees, how it
answers, what it is prevented from doing, where it runs and how the whole
system improves.

A **slot** is a fixed extension point of the harness. Slots do not change;
what is plugged into them does. When a new tool appears, the question is not
*"how do we fit this into our governance?"* but *"which slot does it plug
into?"*

## The eight slots

| # | Slot | Question it answers | Examples today |
|---|------|---------------------|----------------|
| 1 | **Knowledge** | What does the agent know? | CoP good practices, organization rules, ADRs, internal docs |
| 2 | **Capabilities** | What does the agent know how to do? | ai-forge skills and commands, aap-skills, organization skills |
| 3 | **Integrations** | Which systems can the agent touch? | AAP MCP Server, ticketing or CMDB MCP servers |
| 4 | **Input** | What information reaches the agent, and how much? | Output compression of tool results, retrieval, memory |
| 5 | **Output** | How does the agent communicate? | Conversational style, artifact templates (ADR, audit report, PR body) |
| 6 | **Guardrails** | What is the agent prevented from doing or checked on while it works? | Pre/post tool hooks, command policies, permissions, secret scanning |
| 7 | **Execution** | Where does the agent run, with which credentials? | Local IDE, remote dev workspaces, sandboxed containers |
| 8 | **Evolution** | How does the system improve over time? | Auditor findings, Librarian proposals, metrics, agent evaluations |

## Slots and layers form a matrix

Layers apply to every slot, not only to rules. Each cell is decided by the
layer that owns it, and resolved by [precedence](precedence.md).

```text
                 Knowledge     Capabilities    Input          Output              Guardrails
  L0 Community   CoP           ai-forge,       —              —                   —
                               aap-skills
  L1 Org         + naming      + only enable   + adopt an     + concise style;    + denylist
                 delta         ansible-role    output         templates win       hook
                                               compressor
  L3 Project     (inherits)    (inherits)      (inherits)     (inherits)          + scoped
                                                                                  exception
  ─────────────────────────────────────────────────────────────────────────────────────────
  = Effective harness for the project
```

Catalog with admission criteria, mechanisms and verification: [slots/](../../slots/README.md).
Reference adoption of all eight: [EX-04](../../examples/ex-04-harness-slots/README.md).

## Gates are not a slot

Gates (pre-commit, CI, execution environment build, Automation Hub publishing,
AAP runtime controls) live **outside** the harness, in a trusted zone the
agent cannot bypass. They verify results regardless of how those results were
produced — by an agent, by a human, or by both.

See [GAC-0006](../../adr/GAC-0006-gates-are-the-guarantee.md).

## Plugging in something new

1. **Classify** — which slot does it belong to? If it fits none, that is a
   signal to revise the slot model through a method ADR, not to improvise.
2. **Decide** — an ADR in the right layer states what is adopted, with which
   configuration, and what wins on conflict.
3. **Declare** — add it to that layer's instance manifest, pinned to a
   version.
4. **Verify** — if it affects the produced content, a gate checks the result.
   If it only affects how the agent works (e.g. Output style), no gate is
   needed.

The bases do not change and the model does not change. Only the content of
one slot in one layer changes.

## Rules for every slot

- What is plugged into a slot is **guidance or capability**, never the proof
  of compliance. Proof comes from gates.
- Tools installed on a user's machine cannot be verified by the instance;
  they may be `recommended`, never a compliance requirement.
- Artifact templates owned by the organization take precedence over generic
  Output styles.
- Anything that sends data outside the developer's environment or changes
  which model is used is a security decision at L1.
