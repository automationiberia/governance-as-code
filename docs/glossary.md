# Glossary

| Term | Definition |
|------|------------|
| **ADR** | Architecture Decision Record. In an instance, the only mechanism to create, change or remove organization rules and slot adoptions. |
| **Base** | A community source consumed at L0 (e.g. CoP good practices, ai-forge, aap-skills). Pinned, never forked. |
| **Channel** | Anything that applies effective governance: AI harness components, pre-commit, CI, EE build, Hub publishing, AAP runtime controls. Channels consume; they never decide. |
| **Delta** | What an organization does differently from, or in addition to, the community baseline. L1 contains only the delta. |
| **Effective governance** | The result of resolving all layers by precedence for a given scope (organization, domain, project). |
| **Enforcement level** | `advise`, `warn` or `block`. |
| **Exception** | An L3 record that suspends a rule within a limited scope until an expiry date. |
| **Fixture** | A minimal example repository a rule must pass or fail; organization lint rules are tested with fixtures from their ADR's examples. |
| **Gate** | A channel that can block a result: pre-commit, CI, EE build, Hub publishing, AAP runtime. Gates are the guarantee of compliance. |
| **Harness** | Everything around an AI model that shapes how it works, organized in slots. |
| **Instance** | One organization's application of the method: its manifest, ADRs, rule registry, exception register and gates. |
| **Instance manifest** | Declares the bases and versions an instance consumes, its layers, and what is plugged into each slot. |
| **Layer** | A source of authority: L0 Community, L1 Organization, L2 Domain (optional), L3 Project. |
| **Librarian** | AI working mode that drafts ADRs and rule changes when standards or upstream bases evolve. Never approves. |
| **Auditor** | AI working mode that reviews existing content against effective governance and reports debt. |
| **Builder** | AI working mode that produces new content under effective governance. |
| **Locked rule** | An L1 rule (red line) that lower layers cannot relax. Only its owner can grant exceptions. |
| **Method ADR** | A decision about the method itself (`GAC-NNNN`). Lives in this repository. Never contains organization rules. |
| **Organization ADR** | A decision of one organization (`ADR-NNNN`). Lives in that organization's instance. |
| **Repository classification** | How the instance manifest classifies each content repository: its promotion path (`prod`, `nonprod`; unlisted = prod) and optional objective attributes such as `criticality`. Decided by governance, never by the requester; it scopes which rules apply, including process rules. |
| **Rule** | A single, machine-readable registry entry derived from an accepted ADR. The only source channels read. |
| **Slot** | A fixed extension point of the harness: Knowledge, Capabilities, Integrations, Input, Output, Guardrails, Execution, Evolution. |
| **Characterization** | Running existing content before changing it and recording what it actually does, so a modernization can prove what it preserves and what it deliberately changes. |
| **Checker** | ansible-lint run with the instance configuration (L0 rules and ansible-lint profile, organization rules, exceptions). The same command is used by developers, AI modes, pre-commit and CI. |
| **Baseline** | A recorded list of existing violations, tolerated during a rule's warn period and burned down by a date. |
| **Mode** | How the method is used: Auditor, Builder, Librarian, Operator. Common to all organizations. |
| **Operator** | AI working mode that operates live AAP through the AAP MCP Server; read-only first. |
| **Starter kit** | Reusable method tooling: the `gac-modes` Lola module, the AGENTS.md pointer, gate definitions and templates. |
| **Success contract** | What will count as success for a Builder task — current behavior and deviations, acceptance criteria, or a bug reproduction — approved by a human before building (GAC-0010). |
| **Target** | What a mode acts on: content (Git) or platform (live AAP). |
| **Test platform** | The instance's declaration of how disposable test hosts are created (runtime, image, start command, privileges, privilege escalation); part of the Execution slot. |
| **Verifiability** | How a rule can be checked: `mechanical`, `heuristic` or `process`. |
