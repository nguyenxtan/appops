# Documentation index

Architecture baseline: **2026-09-14, v1**. The owner delegated technology and architecture selection. Documents specify a target; [status](status.md) records delivery evidence separately.

## Product

- [Scope and requirement register](product/scope.md)
- [Operations console and user journeys](product/console.md)
- [Vietnamese overview and glossary](vi/overview.md)

## Architecture

- [System overview and technology decisions](architecture/overview.md)
- [Module boundaries and target repository tree](architecture/module-boundaries.md)
- [Relational data model](architecture/data-model.md)
- [Knowledge ingestion, retrieval, and screenshot provenance](architecture/knowledge.md)
- [Isolated document-worker contract](architecture/document-worker-contract.md)
- [Case lifecycle and durable ticket workflows](architecture/case-workflows.md)
- [Integration contracts and provider behavior](architecture/integrations.md)
- [Authorization, approvals, privacy, and threat model](architecture/security.md)
- [AI runtime and model routing](architecture/ai-runtime.md)
- [API, events, and side-effect contracts](architecture/api-contracts.md)
- [Traceability and observability](architecture/observability.md)
- [Deployment and recovery](architecture/deployment.md)

## Decisions

- [ADR-0001: modular monolith and Python backend](adr/0001-system-shape.md)
- [ADR-0002: Temporal, record ownership, and delivery semantics](adr/0002-durable-work.md)
- [ADR-0003: native document ingestion and PostgreSQL retrieval](adr/0003-knowledge.md)
- [ADR-0004: deterministic authorization and controlled actions](adr/0004-policy.md)
- [ADR-0005: hosting, identity, and observability](adr/0005-hosting.md)
- [ADR-0006: provider isolation and AI boundaries](adr/0006-ai-and-integrations.md)

## Engineering and delivery

- [Engineering standards](development/standards.md)
- [Repository skills and routing](development/agent-skills.md)
- [Acceptance matrix](testing/acceptance.md)
- [Implementation roadmap](delivery/roadmap.md)
- [S0 implementation plan](delivery/s0-foundation.md)
- [Operations runbooks](operations/runbooks.md)
- [Go-live gates and environment prerequisites](operations/go-live.md)
- [Primary technical sources](references.md)

## Reading conventions

`MUST` is a release-blocking requirement; `SHOULD` requires a documented exception. Values labelled **initial target** are engineering assumptions to benchmark, not measured capacity or contracted service levels. Provider-specific facts are linked in the source register. Synthetic examples do not assert facts about any real application.

Only this index, ADRs, and the owning architecture documents define the baseline. Delivery plans explain sequence; they do not silently change requirements.
