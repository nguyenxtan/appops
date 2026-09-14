# Module boundaries and target repository tree

## Repository rule

The foundation contains documentation, skills, and documentation checks only. The tree below is the **target implementation layout**, created incrementally by assigned slices. Do not add empty folders, placeholder services, fake endpoints, or dozens of unused packages to make the repository resemble this tree.

```text
appops/
  AGENTS.md
  README.md
  CONTRIBUTING.md
  SECURITY.md
  .agents/skills/<skill-name>/SKILL.md
  .github/workflows/
  apps/
    web/
      src/app/                 # routes and layouts
      src/features/            # application-specific UI features
      src/components/ui/       # reviewed primitive components
      src/lib/api/              # generated client adapter
      tests/
  backend/
    pyproject.toml
    uv.lock
    src/appops/
      bootstrap/                # dependency wiring only
      entrypoints/              # api, core worker, document worker, dispatcher, embeddings
      kernel/                   # IDs, clock protocols, domain errors; intentionally small
      modules/
        identity/
        registry/
        policy/
        knowledge/
        assistance/
        cases/
        automation/
        integrations/
        evidence/
        audit/
      infrastructure/           # connection factories, telemetry, process configuration
    migrations/
    tests/
      unit/
      integration/
      architecture/
      contracts/
      workflows/
  contracts/
    schemas/
    generated/                  # generated OpenAPI and TypeScript types after S0
  config/
    models/
    policies/                   # synthetic, inactive reference configurations
  deploy/
    compose/
    images/
    observability/
  tests/
    docs/
    skills/
    e2e/
    fixtures/synthetic/
  scripts/
  docs/
```

Use pnpm only for the web workspace; uv only for Python. Do not create a JavaScript package for each Python module. The web consumes API contracts, never imports backend persistence details, and never accesses PostgreSQL directly.

## Backend feature layout

Each nontrivial module uses:

```text
modules/<feature>/
  public.py                     # exported DTOs, protocols, facade
  domain/                       # entities, invariants, pure decisions
  application/                  # use cases and ports
  adapters/                     # repositories and provider implementations
  transport/                    # HTTP DTOs/routes or event handlers
```

Create subdirectories only when code exists. Small modules can begin with these as files. Avoid generic base repositories and inheritance frameworks that obscure one use case. `public.py` is the allowed inter-module import boundary; domain-to-domain access is limited to immutable types in the kernel.

Allowed dependency direction: transport/adapters -> application -> domain -> kernel. Bootstrap wires concrete adapters. Domain code MUST NOT import FastAPI, Pydantic transport models, SQLAlchemy, Temporal, boto3, model SDKs, or environment variables.

## Ownership

| Module | Owns | Exposes | Does not own |
| --- | --- | --- | --- |
| identity | Principals, sessions, external identity links | Principal resolution | Application permissions inferred from provider names |
| registry | Organizations, applications, environments, scoped memberships | Application context | Ticket or knowledge lifecycle |
| policy | Versioned policies, grants, action decisions, approvals | Deterministic authorization | Tool execution or model prompts |
| knowledge | Versions, sections, chunks, image links, publication bindings | Authorized retrieval and publication | Ticket closure or tool execution |
| assistance | Conversations, answers, AI runs, answer provenance | Bounded assistance use cases | Autonomous workflow state |
| cases | Internal case work state, external projection, case timeline | Case commands and read model | Jira's authoritative status |
| automation | Temporal workflows, scheduling intent, action orchestration | Durable coordination | Direct ownership of other modules' tables |
| integrations | Connector instances, inbox/outbox, delivery ledger, provider adapters | Authorized connector capabilities | Business resolution policy |
| evidence | Evidence objects, provenance links, scoped retrieval | Sanitized evidence references | Raw secrets or model hidden reasoning |
| audit | Append-only domain/security audit | Audit writer and authorized query | Debug log retention or system credentials |

Cross-module writes occur through application facades in a shared unit of work where atomicity is required. They never call a remote service while holding that transaction. Cross-module reads use explicit query ports or documented read models, not imports of another module's ORM model. Read-model joins are permitted only in dedicated adapters with an ownership entry and authorization tests.

## Workflow purity

Temporal workflow definitions live under `automation/adapters/temporal/workflows/`; registered activities invoke application use cases. Workflow definitions use Temporal's deterministic time/timers and serializable references. No direct SQL, filesystem, HTTP, model inference, or wall-clock reads inside workflow code.

The document worker imports the parsing subset and job contracts, not the business API bootstrap. Credential and dependency separation is validated in container tests. A shared repository is not permission to share all runtime secrets.

## Change and extraction rules

Add a connector under `integrations/adapters/<provider>/` with a capability declaration and contract tests. Add an application as registry/configuration data, not a fork. Add a procedure as reviewed knowledge plus separate action definitions; never derive production permissions from the document.

Extract a module into an independent service only with measured scaling, isolation, or ownership evidence, a data-ownership migration plan, and an ADR. Do not split simply because a module has grown to a certain file count.

## Enforcement targets

S0 installs import-linter rules for layer boundaries and forbidden domain imports. Each new module adds boundary tests and is prohibited from reading another module's private ORM classes. CI includes generated-contract drift, type checks, migration checks, and tests appropriate to the slice. See [engineering standards](../development/standards.md).
