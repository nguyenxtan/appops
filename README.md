# AppOps

Software operations support and controlled automation for multiple business applications.

AppOps starts with source-grounded user guidance and correctly linked screenshots. Its core is designed to add Jira case handling, durable follow-up, read-only diagnostics, human approvals, and bounded operational actions without replacing the knowledge or channel layers.

## Status

**Architecture foundation only. Application runtime, deployment, live integrations, and production acceptance are not implemented.** Documentation describes the target system, not capabilities already delivered. See [delivery status](docs/status.md).

## Start here

- Product owner: [Vietnamese architecture summary](docs/vi/overview.md) and [scope](docs/product/scope.md).
- Engineer: [architecture](docs/architecture/overview.md), [module boundaries and target tree](docs/architecture/module-boundaries.md), then [delivery roadmap](docs/delivery/roadmap.md).
- Coding agent: [AGENTS.md](AGENTS.md), [skill routing](docs/development/agent-skills.md), then the explicitly assigned slice.
- Operator: [deployment](docs/architecture/deployment.md), [runbooks](docs/operations/runbooks.md), and [go-live gates](docs/operations/go-live.md).
- Complete navigation: [documentation index](docs/README.md).

## Selected foundation

| Concern | Decision |
| --- | --- |
| System shape | Modular monolith, explicit ports/adapters, independently runnable API and worker processes |
| Web console | Next.js 16, React 19, TypeScript, Tailwind CSS 4, shadcn/ui |
| Backend | Python 3.12, FastAPI, Pydantic 2, SQLAlchemy 2, Alembic, psycopg 3 |
| Durable work | Temporal Python SDK; PostgreSQL transactional inbox/outbox |
| Business and retrieval data | PostgreSQL 17, pgvector 0.8 line, native full-text search |
| Documents | pdfplumber, pypdfium2, python-docx; OCR disabled in the first release |
| AI | Local Qwen3-Embedding-0.6B; OpenRouter chat adapter with approved provider routing |
| Identity | Keycloak through OpenID Connect; application-scoped authorization in AppOps |
| Files | Private Cloudflare R2 in hosted environments; filesystem adapter for local development |
| Telemetry | OpenTelemetry, Grafana, Loki, Tempo, Prometheus |
| Packaging | Docker images; Docker Compose for local and single-host pilot deployments |

This is not a commitment that the complete stack has been compatibility-tested. Exact dependency locks and image digests are produced and tested in S0; model evaluation is an S2 release gate.

## Repository checks

The documentation foundation uses only the Python standard library:

```sh
python3 -m unittest discover -s tests/docs -v
python3 scripts/check_docs.py
git diff --check
```

These checks validate repository documentation conventions. They do not prove application functionality, security, model quality, or agent compliance.

## Data handling

This repository is public. Commit synthetic examples only. Never commit internal manuals, original screenshots, Jira exports, production logs, credentials, or personal data. Real operational content belongs in approved private storage with access control.

No software license has been selected on the owner's behalf. Review licensing before redistribution; dependency licenses are a separate release concern.
