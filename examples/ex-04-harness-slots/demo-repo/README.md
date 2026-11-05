# Guardrail demo repository

A minimal content repository for the live guardrail demo
([presentation/demo-script.md](../../../presentation/demo-script.md), part D).
`roles/firewall/tasks/main.yml` breaks ACME rule R-COLL-001 on purpose; the
repository is not classified in the acme manifest, so it is treated as
production (deny by default).
