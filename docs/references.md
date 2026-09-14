# Primary technical sources

Reviewed while preparing the architecture on 2026-09-14. These links support specific vendor capabilities; they do not establish that AppOps has implemented or tested them. Architecture tradeoffs, policy defaults, limits, and acceptance targets are AppOps design decisions.

| Source | Capability used |
| --- | --- |
| [FastAPI application structure](https://fastapi.tiangolo.com/tutorial/bigger-applications/) | Modular HTTP routes and generated API boundary |
| [SQLAlchemy transactions](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html) | Explicit transaction management |
| [PostgreSQL row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html) | Row policies; owner/bypass caveats must be tested |
| [pgvector](https://github.com/pgvector/pgvector) | Exact/approximate search, hybrid retrieval and filtering tradeoffs |
| [Temporal Python SDK](https://docs.temporal.io/develop/python) | Workflow and activity implementation |
| [Temporal timers](https://docs.temporal.io/develop/python/workflows/timers) | Durable waiting |
| [Temporal messages](https://docs.temporal.io/develop/python/workflows/message-passing) | Signals, updates, and concurrency considerations |
| [Temporal activities](https://docs.temporal.io/activity-definition) | Retry and idempotency considerations |
| [Temporal deployment](https://docs.temporal.io/self-hosted-guide/deployment) | Self-hosted service requirements |
| [pdfplumber](https://github.com/jsvine/pdfplumber) | Native text/layout; image-position versus reconstruction distinction |
| [pypdfium2](https://pypdfium2.readthedocs.io/en/stable/python_api.html) | Page rendering and crop implementation |
| [python-docx](https://python-docx.readthedocs.io/en/latest/user/text.html) | DOCX text structure |
| [Qwen3 embedding model card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | Model dimensions and query instruction conventions |
| [OpenRouter selected model](https://openrouter.ai/openai/gpt-4.1-mini) | Initial chat-profile availability reference |
| [OpenRouter routing](https://openrouter.ai/docs/guides/routing/provider-selection) | Provider allowlisting and fallback controls |
| [OpenRouter data retention](https://openrouter.ai/docs/guides/features/zdr) | Endpoint retention controls, not blanket compliance proof |
| [Keycloak OIDC](https://www.keycloak.org/securing-apps/oidc-layers) | Identity protocol integration |
| [Next.js installation](https://nextjs.org/docs/app/getting-started/installation) | Web framework/tooling baseline |
| [Cloudflare R2 S3 compatibility](https://developers.cloudflare.com/r2/api/s3/api/) | Supported storage API subset |
| [Jira Cloud webhooks](https://developer.atlassian.com/cloud/jira/software/webhooks/) | Signed admin webhooks, retries, event identity |
| [JSM request API](https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-request/) | Public/internal comment and attachment semantics |
| [Telegram Bot API](https://core.telegram.org/bots/api) | Webhooks, message/media delivery |
| [Zalo Bot Platform](https://bot.zaloplatforms.com/) | Correct target product |
| [Zalo Bot documentation](https://docs.zaloplatforms.com/zalo-bot) | Bot-token API and channel capability reference |
| [Loki HTTP API](https://grafana.com/docs/loki/latest/reference/loki-http-api/) | Bounded source log queries |
| [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/) | Trace/span context and linkage |
| [Codex skills](https://developers.openai.com/codex/skills/) | Repository-local `.agents/skills` discovery |
| [AGENTS.md](https://developers.openai.com/codex/guides/agents-md/) | Project-level coding-agent instructions |
| [Agent Skills specification](https://agentskills.io/specification) | SKILL.md metadata and file format |

Revalidate endpoint behavior, authentication, model availability, dependency versions, licenses, and service limits during the relevant implementation/activation slice. Do not copy stale examples into production without a contract test.
