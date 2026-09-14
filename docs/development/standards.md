# Engineering standards

## Design discipline

Implement the assigned slice, not the entire roadmap. Prefer explicit use cases and small cohesive modules over generic abstraction frameworks. A module owns its writes; a use case coordinates through public interfaces. No domain behavior in controllers, ORM callbacks, UI components, workflow signal handlers, or prompt text.

Use immutable value objects for IDs, scope, actor context, and action parameters. Validate transport inputs at the boundary; enforce business invariants in the domain. Type annotations are required for public Python functions; TypeScript strict mode is required. Do not disable type/lint checks globally to finish a slice.

## Naming and structure

Python identifiers use snake_case; classes use PascalCase. HTTP/JSON fields use snake_case. React components use PascalCase and features use kebab-case directories. Keep provider names inside adapters except explicit provider configuration/contracts. Avoid `utils.py`, `helpers.ts`, generic `BaseService`, and untyped JSON passing across modules.

File length is a review signal, not a mechanical architecture metric. A file above 400 logical lines requires a cohesion review, not arbitrary splitting. Document exceptional complexity next to its owning use case. Do not introduce empty interfaces or unused factories solely to imitate clean architecture.

## Tests before behavior

Write a behavior-focused failing test; observe the intended failure; implement the smallest passing change; refactor; run related tests. A test must fail when the relevant production behavior is broken, not merely assert that a mock was called.

Use real PostgreSQL for RLS, constraints, transactions, and migrations. Use a real Temporal test service for timers/signals/replay, with time skipping. Use provider mocks for contract/error behavior, then separately approved live acceptance. Use synthetic documents that include image/section ambiguity.

Core invariants and negative authorization paths are mandatory. The initial coverage floor is 90% branch coverage for domain/policy modules and 80% backend aggregate coverage, but coverage cannot replace scenario completeness. Exclusions need a documented reason and reviewer approval.

## Dependency management

One `uv.lock` under backend and a pnpm workspace lock for web. Pin runtime image digests. S0 records exact tool/runtime versions and a clean install. Upgrade dependencies through a reviewed PR with compatibility, security, and licensing evidence. Do not vendor third-party skill collections or frameworks without need and license review.

## CI targets

The current foundation has documentation checks only. S0 introduces:

- Python: Ruff, formatting check, mypy, import-linter, pytest, migration smoke, and dependency audit.
- Web: lint, TypeScript, component tests, production build, and Playwright critical journeys.
- Contracts: regenerate OpenAPI/types from actual implemented routes and fail on drift.
- Containers: build, scan, and smoke-test health/configuration without deployment.

Later slices add workflow replay, provider contracts, RAG evaluation, and action-race tests. Keep docs-only CI inexpensive and avoid full model downloads on documentation changes. Cache dependencies by lockfile; never cache credentials or private documents. Use minimal GitHub permissions and pin third-party actions to reviewed commit SHAs.

## Transactions and errors

One explicit unit of work per command/activity. Transaction-local scope, optimistic versions, and bounded locks. Commit business state, audit, and outbox atomically where required. No network call inside an open DB transaction. Preserve domain error codes and translate them at the boundary; never return raw exception traces.

External writes have a ledger and reconciliation contract. Retry is operation-specific. Timeouts and unknown outcomes are different from definite failure. Do not mask an unavailable dependency with fabricated success.

## Review and delivery

Review against requirements first, then code quality/security. Product-owner review covers workflows, usability, and operational policy; it is not a substitute for technical review. When an independent reviewer is unavailable, report that limitation rather than call self-review independent.

Use conventional commit prefixes. One PR per coherent slice or smaller validated concern. No force push, auto-merge, deploy, paid resource creation, or production mutation without authorization. Update canonical docs and [status](../status.md) in the same change that alters behavior.
