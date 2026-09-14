# ADR-0001: Modular monolith and Python backend

Date: 2026-09-14. Status: Selected baseline; implementation not started.

## Context

Multiple applications need document processing, support, and controlled operations with clear ownership, without business-microservice overhead.

## Decision

Use one Python backend package with feature modules, ports/adapters, and separate process entry points. FastAPI serves HTTP; Next.js serves the console. Python consolidates parsing, model integration, and workflow activities.

## Alternatives

NestJS plus Python parsing adds cross-language service contracts immediately. A microservice-per-agent design duplicates state/policy and complicates recovery. Neither is selected.

## Consequences

Enforce imports and ownership in CI. Separate credentials/resources despite shared source. Future extraction needs measured evidence and a data migration. See [boundaries](../architecture/module-boundaries.md).
