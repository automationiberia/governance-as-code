---
id: ADR-0007
title: Test platform for automated tests
status: accepted
layer: organization
domain: null
type: harness-adoption
slot: execution
date: 2026-11-05
approvers: [automation-lead]
supersedes: null
superseded_by: null
acts_on:
  - action: add
    target: null
rules: []
---

# ADR-0007: Test platform for automated tests

## Context

[GAC-0010](../../../adr/GAC-0010-define-success-before-acting.md) requires
tests to run where they are written, on a platform the instance declares. In
dogfooding, a Builder wrote a Molecule scenario for an image without systemd
and with `become` but no `sudo`: the role was correct, the scenario could not
start. R-TEST-001 (ADR-0006) needs a platform every team uses the same way.

## Decision

Adopt, in the **Execution** slot, the test platform declared in
`manifest.yml` → `test_platform`:

- Disposable hosts are **podman containers** from
  `registry.access.redhat.com/ubi9/ubi`, started with `sleep infinity`,
  unprivileged, no init system.
- Tests connect as root: **no privilege escalation** (`ansible_become: false`).
- Molecule uses the podman driver (`molecule-plugins[podman]`); plain
  playbook tests use the `containers.podman.podman` connection.
- Content that needs systemd services declares it in its success contract and
  uses the `init` variant listed in the manifest.

## Consequences

- Generated scenarios match the platform and run on any workstation or CI
  runner with podman.
- This is a slot adoption, not a rule: it has no lint check. The Builder
  reports "written, not run" when podman is not available.
