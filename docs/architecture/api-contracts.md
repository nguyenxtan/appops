# HTTP, event, and side-effect contracts

## HTTP conventions

Prefix business routes with `/api/v1`. JSON uses snake_case, UUID IDs, and RFC3339 UTC timestamps. Validate strict request schemas and deny unknown security-critical fields. Use cursor pagination, default 25 and maximum 100. Authentication and authorization run before resource-specific payload disclosure.

Mutating commands accept `Idempotency-Key`; scope keys to organization, principal, route, and canonical request hash. Reuse with a different hash returns 409. Optimistic updates use `If-Match` with the aggregate version and return 409 on conflict. A 202 means durable acceptance, not completed execution. Return a `Location` for the job/action resource.

Errors use a stable structure: `code`, `message`, `request_id`, `retryable`, and optional safe field errors. Never return tokens, raw SQL, stack traces, or an existence distinction that leaks inaccessible resources.

## Endpoint ownership

| Method and route | Owner | Contract |
| --- | --- | --- |
| GET /health/live | bootstrap | Process is alive; no dependency calls |
| GET /health/ready | bootstrap | Database/schema reachable; report degraded optional dependencies separately |
| GET /api/v1/session | identity | Current principal and safe capability summary |
| GET /api/v1/applications | registry | Only authorized applications |
| POST /api/v1/applications | registry | Authorized administration; audited |
| GET /api/v1/applications/{id}/environments | registry | Authorized environment scope |
| POST /api/v1/documents | knowledge | Reserve document/version and bounded upload |
| POST /api/v1/document-versions/{id}/complete-upload | knowledge | Validate stored object and enqueue ingestion; 202 |
| GET /api/v1/ingestion-jobs/{id} | knowledge | Stage, measurable progress, warnings, review state |
| GET /api/v1/document-versions/{id}/review | knowledge | Source blocks, crops, and candidate associations |
| PATCH /api/v1/document-versions/{id}/review | knowledge | Versioned reviewer edits; never auto-publish |
| POST /api/v1/document-versions/{id}/publish | knowledge | Publication command with approval and version guard |
| POST /api/v1/conversations | assistance | Create scoped conversation |
| POST /api/v1/conversations/{id}/messages | assistance | Durable message acceptance and response job |
| GET /api/v1/conversations/{id}/events | assistance | Authenticated SSE, ordered event IDs and resumable reads |
| GET /api/v1/answers/{id} | assistance | Structured answer after current authorization check |
| GET /api/v1/media/{id} | knowledge/evidence | Authenticated bytes; never a public file URL |
| POST /api/v1/cases | cases | Explicit internal support case |
| GET /api/v1/cases | cases | Scoped operator queue |
| GET /api/v1/cases/{id}/timeline | cases | Authorized evidence and activity read model |
| POST /api/v1/cases/{id}/commands | cases | Whitelisted typed commands, not arbitrary state assignment |
| POST /api/v1/actions | policy/automation | Create a bounded proposed action |
| POST /api/v1/actions/{id}/approval | policy | Approve/reject exact version/input; no execution in handler |
| GET /api/v1/actions/{id} | automation | Decision, delivery state, verification, evidence |
| POST /api/v1/automation-controls | policy | Pause/resume authorized scope; audited |
| POST /api/v1/feedback | assistance | Linked answer/case feedback |
| POST /webhooks/v1/{provider}/{connector_id} | integrations | Provider-specific verification and durable inbox commit |

These are target routes, not implemented endpoints. S0 generates the initial OpenAPI from actual identity/registry routes; each later slice adds and tests its routes. Do not publish a fake complete OpenAPI implementation or generate clients for endpoints that do not exist.

SSE is a presentation stream, not the durable event bus. An SSE disconnect cannot cancel a committed ticket workflow. Persist message/event IDs; authorize each resumed stream and scope its cursor to the conversation.

## Domain event envelope

Every event has `event_id`, `event_type`, `schema_version`, `organization_id`, `aggregate_type`, `aggregate_id`, `aggregate_version`, `occurred_at`, `actor_ref`, `correlation_id`, `causation_id`, optional `traceparent`, and bounded `data` consisting primarily of record references.

Example event types: `knowledge.ingestion_requested.v1`, `knowledge.published.v1`, `case.external_facts_changed.v1`, `case.wait_cycle_started.v1`, `action.approval_recorded.v1`, `delivery.reconciliation_requested.v1`. `event_id` provides deduplication; `correlation_id` groups work; neither is a credential.

An event schema change is additive within a version or introduces a new version. Consumers reject unsupported versions into a visible quarantine/dead-letter state. Do not silently discard an unknown event. Inbox/outbox tables are the initial delivery mechanism; a future broker consumes the same governed envelope.

## Case command contract

Allowed commands are `assign`, `request_user_action`, `record_evidence`, `propose_resolution`, `pause_automation`, `resume_automation`, `escalate`, `request_close`, and `reopen`. Each is a distinct typed payload and domain handler. No generic `set_state` command bypasses transition guards. External synchronization uses a separate trusted command with verified provider facts and connector identity.

## Action contract

A proposed action contains `definition_id`, `definition_version`, `case_id` when required, `application_id`, `environment_id`, `target_ref`, `bounded_inputs`, `input_hash`, `evidence_refs`, and `idempotency_key`. The server supplies identity, policy decision, and current timestamps; clients cannot choose `approved=true`, executor credentials, or a lower risk class.

Action lifecycle: `PROPOSED -> DENIED | AWAITING_APPROVAL | READY -> EXECUTING -> SUCCEEDED | FAILED | UNKNOWN_OUTCOME`. Expired/revoked authorization produces `CANCELLED`. SUCCEEDED requires a verified execution result and postcondition, not a successful model response.

## Reliable outbound delivery

Reserve a delivery and action audit in one transaction; commit; call the external API; record a confirmed result in a new transaction. A process crash between remote success and local recording creates uncertainty. Reconciliation resolves it by checking provider state/operation markers. Without proof, automated resending is forbidden.

All provider calls carry a bounded timeout and safe trace context where supported. Do not put case content, user email, or credentials in tracing headers. Record side-effect-specific attempts separately from transport retries.

## Contract testing

Test request validation, error privacy, unauthorized access, pagination scope, duplicate idempotency keys with changed inputs, concurrency conflicts, webhook duplicates/signatures, SSE reconnection authorization, generated OpenAPI drift, and remote delivery uncertainty. Provider fixtures are synthetic and versioned. Live connector acceptance remains a separate evidence class.
