# ADR-0004: Deterministic policy and controlled actions

Date: 2026-09-14. Status: Selected baseline; implementation not started.

## Context

Operations can expose sensitive data or change production. Model suggestions are not authority.

## Decision

Use typed, versioned domain policies. Separate grants, procedures, actions, approvals, execution, and audience checks. Default deny; automatic sending/closure remain disabled until approved.

## Alternatives

Prompt-only safety cannot enforce access. Broad administrator connectors grant excessive capability. An external policy service is unnecessary initially.

## Consequences

Bind and expire approvals. Authorize reads/comments too. Require takeover, pause, execution guards, and audit. Separate no-response from verified resolution. See [security](../architecture/security.md).
