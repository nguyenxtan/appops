# ADR-0002: Durable work and authoritative records

Date: 2026-09-14. Status: Selected baseline; implementation not started.

## Context

Follow-up spans days, survives restarts, and reacts to human replies and provider races.

## Decision

Temporal owns execution/timers. PostgreSQL inbox/outbox provides durable handoff and owns AppOps records. Jira owns external facts. Action ledgers and reconciliation handle at-least-once delivery.

## Alternatives

Local timers lose state. Redis queues require us to implement long waits, workflow upgrades, and recovery ourselves. LangGraph persistence does not replace this cross-day orchestration boundary.

## Consequences

Temporal adds persistence and replay testing. It does not guarantee exactly-once external effects. Unknown results require reconciliation. See [case workflows](../architecture/case-workflows.md).
