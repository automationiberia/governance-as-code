# Success contract — role `troubleshooting_packages`

> Written after the fact: GAC-0010 postdates this example.

| | |
|---|---|
| **Kind** | new content |
| **Repository** | `lab_tools` · classification: nonprod |
| **Governance** | acme@2026.11 |
| **Status** | approved by the lab team lead (approval simulated in this example) |

## Acceptance criteria

| # | Given | When | Then | Result |
|---|-------|------|------|--------|
| A1 | A lab host | The role runs with the default list | `strace`, `tcpdump`, `lsof`, `bind-utils` are installed | ✅ met — one run with an assertion, on the test platform (`ubi9/ubi`) |
| A2 | — | The checker runs | No `block` findings | ✅ met |

## Verification

| | |
|---|---|
| Process rules that apply | none — nonprod repository: R-TEST-001 does not apply |
| How | Light verification (GAC-0010): one run with an assertion; no automated test kept in the repository |
| Test platform | podman, `ubi9/ubi`, no privilege escalation (ADR-0007) |
