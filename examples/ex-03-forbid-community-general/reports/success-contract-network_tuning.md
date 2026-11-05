# Success contract — playbook `type_linux_network_tuning` (network_tuning)

> Written after the fact: GAC-0010 postdates this example.

| | |
|---|---|
| **Kind** | new content |
| **Repository** | `network_tuning` · classification: prod |
| **Governance** | acme@2026.11 |
| **Status** | approved by the network team lead (approval simulated in this example) |

## Acceptance criteria

| # | Given | When | Then | Result |
|---|-------|------|------|--------|
| A1 | A RHEL host with firewalld | The playbook runs | The `https` service is allowed, permanently and immediately | ⚠️ not verified |
| A2 | A RHEL host | The playbook runs | `net.core.somaxconn = 4096` and `net.ipv4.tcp_syncookies = 1`, persisted | ⚠️ not verified |
| A3 | — | The checker runs | Nothing from `community.general` (R-COLL-001), no `block` findings | ✅ met (after the first draft was blocked) |
| A4 | — | `ansible-playbook --syntax-check` | Passes | ✅ met |

## Verification

| | |
|---|---|
| Process rules that apply | none for playbooks — R-TEST-001 covers roles and collections |
| How | Light verification: checker and syntax check |
| Why A1–A2 are not verified | The test platform (unprivileged UBI 9 container, ADR-0007) runs neither firewalld nor kernel parameter changes. They need a VM or a privileged host — a gap for the Librarian: either extend the test platform or accept that playbook behavior is verified only in a pre-production environment |
