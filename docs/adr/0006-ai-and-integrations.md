# ADR-0006: AI and provider isolation

Date: 2026-09-14. Status: Selected baseline; implementation not started.

## Context

Channels, ticket products, models, and diagnostics evolve independently and must not own policy.

## Decision

Use typed ports and capability manifests. Start local embeddings and an approved OpenRouter profile. Jira Cloud is the first implementation adapter; the user's edition remains an activation input. Telegram and Zalo Bot Platform use separate adapters.

## Alternatives

Provider SDKs throughout domain code obstruct upgrades/privacy. Treating every Jira/Zalo product as one API hides incompatibility. Unbounded agent frameworks are not required for registered tools and RAG.

## Consequences

Require explicit provider modes, permissions, contract tests, and live acceptance. No silent fallback. New adapters still need engineering and tests. See [integrations](../architecture/integrations.md) and [AI runtime](../architecture/ai-runtime.md).
