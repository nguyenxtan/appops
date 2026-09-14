# S0 foundation implementation plan

For coding agents: read root AGENTS.md and use repository skills `appops-start`, `appops-design`, `appops-tdd`, `appops-security`, and `appops-verification` as applicable. Do not implement later slices.

**Goal:** an authenticated local web/API foundation that lists only authorized applications, has tested persistence/health, and proves the chosen workflow dependency can run a durable smoke workflow.

**Architecture:** [overview](../architecture/overview.md), [boundaries](../architecture/module-boundaries.md), and [security](../architecture/security.md).

**Not included:** document ingestion, chatbot answers, production hosting, Jira comments, Telegram/Zalo messages, automatic closure, or operational tools.

All file paths below are target files. Commands become executable only after the corresponding task creates their manifests/configuration. Never report them as available beforehand.

## Task 1: reproducible tooling and test boundary

Create `backend/pyproject.toml`, `backend/uv.lock`, `apps/web/package.json`, root `package.json`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`, and version configuration. Resolve and lock the selected technology lines from official registries. Record exact versions and clean-install evidence; do not invent patches or handwrite a pretend lockfile.

Create `backend/tests/architecture/test_domain_imports.py` before domain implementation. It must reject a temporary domain module importing FastAPI, SQLAlchemy, Temporal, boto3, or a network library, then accept a pure module. Add Ruff, mypy, import-linter, pytest, TypeScript strict mode, and frontend test configuration.

Run the failing architecture test, implement the check, rerun. Clean-install commands: `uv sync --project backend --frozen` and `pnpm install --frozen-lockfile`. No model downloads or external credential use in this task.

## Task 2: explicit scope and registry domain

Create `backend/src/appops/kernel/ids.py`, `kernel/errors.py`, `modules/registry/domain/application.py`, `modules/registry/application/list_applications.py`, and its repository protocol. Public signature: `ListApplications.execute(context: PrincipalContext, query: ApplicationQuery) -> ApplicationPage`. The immutable context contains organization ID, principal ID, and verified scope references, not a trusted list supplied by the browser.

Create `backend/tests/unit/registry/test_list_applications.py`. Required behaviors: unknown identity denied; missing organization denied; only granted applications returned; empty grants yield no entries; application from another organization cannot be accessed by ID. Domain tests do not import ORM or HTTP classes.

Example assertion contract:

```python
assert {item.id for item in result.items} == {granted_application_id}
assert foreign_application_id not in {item.id for item in result.items}
```

The test fixture must create both records and distinct grants; asserting against an already-filtered mock is insufficient. Run red, implement the use case, run green, then inspect dependency direction.

## Task 3: real PostgreSQL transactions and migrations

Create initial Alembic migrations for organizations, principals, sessions, applications, environments, memberships, audit records, and required composite constraints. Create `backend/src/appops/infrastructure/database.py` and registry persistence adapters. Runtime role is not owner/BYPASSRLS. Trusted organization context is transaction-local.

Create `backend/tests/integration/test_scope_isolation.py` and `test_migrations.py` first. Use actual PostgreSQL 17 with pgvector available. Test unset scope, foreign scope, pooled connection reuse, unauthorized insert/update, rollback, missing audit insert, optimistic conflicts, and clean-database migration. Test startup rejects an unexpected schema version.

Run `uv run --project backend pytest backend/tests/integration -q`. A SQLite substitute cannot satisfy this gate. Do not alter any remote database.

## Task 4: OIDC session and actual HTTP routes

Create API bootstrap, identity routes, session adapter, and registry routes. Auth routes: `GET /auth/login`, `GET /auth/callback`, `POST /auth/logout`. Business routes: `GET /api/v1/session`, `GET /api/v1/applications`, `GET /api/v1/applications/{id}/environments`. Health routes follow the API contract.

Use Keycloak authorization-code flow with PKCE/state/nonce and an opaque secure session. Local realm/client setup uses synthetic users and non-production secrets outside Git. Tests cover invalid state/nonce/issuer/audience, expired/revoked session, CSRF rejection, logout, 401 versus non-leaking denied resource behavior, and successful scoped application listing.

Generate OpenAPI from these real routes. It must not contain invented future support/Jira endpoints. `/health/live` stays 200 while an optional model is disabled; `/health/ready` returns 503 if the required database/schema is unavailable. Keep diagnostic detail private.

## Task 5: minimal usable console

Create `apps/web/src/app/layout.tsx`, login/session handling, `src/features/applications/`, and generated-client integration. Render a login flow, authorized application/environment selector, empty-state support home, and clear 'knowledge support not implemented' state. No fake chat response or working-looking disabled automation.

Create Playwright tests for login, app selection, logout, denied deep link, keyboard navigation, and failed dependency state before implementation. Validate server-generated permissions; UI filtering alone is not a security test. Run web typecheck, lint, test, and build scripts plus the targeted Playwright suite.

## Task 6: Temporal and process baseline

Create `deploy/compose/compose.local.yaml`, image definitions, worker entrypoints, and `backend/tests/workflows/test_durable_smoke.py`. The local profile includes PostgreSQL, Keycloak, and a local Temporal test/development service with synthetic scope. Configure distinct core/document namespace names and private access; persistent pilot deployment is not part of this task.

The smoke workflow waits on a durable timer, receives a signal, and returns a reference-only result. Test worker restart while waiting and history replay. It performs no Jira, model, storage-provider, or production operation. Record SDK/server versions and compatibility evidence.

## Task 7: CI and handoff

Add code CI with scoped jobs, locked install, Python checks, web build, architecture tests, real-dependency integration tests, generated-contract drift, and container smoke. Preserve the cheap documentation workflow. Do not add a deployment workflow yet.

Run focused tests first, then the full S0 suite. Review code against requirement IDs R03/R10/R12/R13/R15. Update status with concrete implemented paths and NOT_RUN items. Open a PR with exact commit, commands, results, and limitations. Do not merge/deploy automatically.

## Exit evidence

A clean checkout can install/build. A real local OIDC login lists only permitted applications. Database isolation and failure readiness tests pass. The workflow smoke survives restart. No provider credentials or private data were committed; no external write occurred. Future module folders are not created empty merely to match a diagram.
