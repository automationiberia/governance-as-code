---
id: GAC-0008
title: Separate modes from targets; add Operator, read-only first
status: accepted
layer: method
type: evolution
date: 2026-11-04
---

# GAC-0008: Separate modes from targets; add Operator, read-only first

## Context

The first attempt combined content modes (Auditor, Builder, Librarian) with
"platform areas" (Audit, Operate, Build, Maintain), which overlapped. One of
the three community bases, aap-skills, operates live AAP through the AAP MCP
Server and needs a clear place in the method.

## Decision

1. A **mode** is what is done; a **target** is what it is done on.
2. Targets: **content** (Git) and **platform** (live AAP). The Librarian works
   on governance itself.
3. Modes: Auditor (content, platform), Builder (content; platform later as
   configuration as code), Operator (platform), Librarian (governance).
4. Operator starts **read-only**. Any write requires explicit human
   confirmation and RBAC, and goes only through the AAP MCP Server.
5. Implementation order: Auditor and Builder on content → Librarian →
   Auditor on platform → Operator → Builder on platform.

## Consequences

- aap-skills has a defined consumer (Auditor on platform, Operator).
- Organization rules apply to platform objects too (`PLAT` area).
- Platform writes carry higher risk and are deliberately deferred.
