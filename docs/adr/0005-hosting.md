# ADR-0005: Pilot hosting, identity, and telemetry

Date: 2026-09-14. Status: Selected baseline; implementation not started.

## Context

An operator-owned platform needs reproducible deployment and recovery, not a speculative dependency list.

## Decision

Use Ubuntu/Docker Compose, Caddy, Keycloak OIDC, PostgreSQL, private R2, and OpenTelemetry/Grafana. Hosted Temporal uses persistent infrastructure. No Workers-only or Kubernetes baseline.

## Alternatives

Serverless-only hosting does not fit the selected persistent workers without redesign. Kubernetes adds cluster operation before workload evidence exists.

## Consequences

A single host is not HA. Capacity, backup, restore, isolation, and approvals are release gates. Storage data approval is separate from Git approval. See [deployment](../architecture/deployment.md).
