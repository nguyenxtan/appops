# Integration contracts

## Adapter model

Adapters implement versioned ports, not provider-specific business policy. Each connector declares provider/edition, capability versions, authentication mode, scopes, audience rules, supported content types, query limits, timeouts, retry behavior, health probe, reconciliation strategy, and idempotency limitations.

Canonical capabilities include `ticket.read`, `ticket.comment.public`, `ticket.comment.internal`, `ticket.transition`, `channel.message.send`, `channel.media.send`, `diagnostics.logs.read`, and `application.status.read`. A missing capability means unavailable, not 'try the nearest endpoint'. Existing integrations do not need to be enabled for the architecture or local tests to work.

Each integration operates in one of DISABLED, READ_ONLY, DRAFT_ONLY, or APPROVED_AUTOMATION modes. The default is DISABLED. Credentials, scope mapping, contract tests, and owner-approved activation are required before progressing.

## Jira

### Selected first adapter

Implement **Jira Cloud REST API v3**, with a separate Jira Service Management capability layer for customer requests and public/internal comment semantics. This is an implementation target, not an assertion that the user's Jira runs in Cloud. Jira Data Center needs an edition-specific adapter and contract test suite; do not send Cloud payloads to an unknown edition.

Use an organization-owned dedicated integration account with an approved, least-privilege scoped API token in the first single-organization adapter. Store the credential as a secret reference. Do not use the product owner's personal administrator token. OAuth 2.0 can be added as a credential adapter without changing ticket policy; it is not required for the first internal deployment. The selected authentication method must be confirmed supported for the target account and endpoint before activation.

Configure an explicit mapping of Jira project/request type to AppOps application, environment, priority, audience, status transitions, and permitted actors. Missing mappings block automated writes. The application name inferred from text is only a suggestion.

### Intake and synchronization

For the selected Cloud admin-webhook mode, require a configured signing secret, validate `X-Hub-Signature` over the exact raw body using an allowed algorithm and constant-time comparison, then apply body limits and schema validation. Provider documentation also describes `X-Atlassian-Webhook-Identifier` for deduplicating retried Cloud deliveries. Verify the actual registration mode supports these semantics during connector acceptance; unsupported authentication modes are not silently accepted.

Acknowledge only after durable inbox/outbox commit, then fetch relevant ticket facts through the authorized API. Signed payloads can still be stale or repeated. Preserve event identity and perform bounded, cursor-based reconciliation every five minutes for configured project scope with an overlap window. Periodically reconcile active cases even without events. Do not scan every historical ticket on every timer.

### Replies, attachments, and transitions

Use the JSM request-comment API for its explicit `public` boolean when JSM is installed and allowed. Public replies and internal notes are distinct actions and permissions. For Jira without JSM, configure tested issue-comment visibility behavior; if private semantics cannot be guaranteed, disable internal notes rather than send them publicly.

Represent content as a validated internal message model. Adapters render ADF, plain text, or provider-specific content as required. Attach only approved media allowed for the destination audience. Do not assume a Markdown image URL is equivalent to an uploaded attachment.

Read available transitions and required fields for the specific ticket. A global numeric 'close transition' is forbidden. The external status is updated locally only after a confirming provider read. Ticket closure policy is owned by [case workflows](case-workflows.md), not the adapter.

### Deduplication and uncertain effects

A local action has a stable ID, content hash, destination, and delivery ledger. When supported, write an operation marker in a provider property or safe metadata and persist the returned comment/transition identity. If a request times out after delivery may have occurred, reconcile using remote IDs/properties and an attributable bounded search. If uniqueness cannot be established, mark `UNKNOWN_OUTCOME` and ask an operator. Never claim a provider without idempotency support is exactly-once.

Ignore confirmed AppOps-originated comments as new assistance triggers while still consuming them as delivery evidence. A bot should not respond to its own response forever.

## Telegram

Implement the official Bot API through the shared HTTP adapter. Authenticate webhooks with the configured Telegram secret-token header; deduplicate `update_id`. Link the sender to a verified AppOps principal before private support. Initial mode is private direct chat; group content requires separate membership/audience enforcement.

Support text, source links, and approved image delivery using the documented photo/file methods. Separate long text from bounded media captions. Persist provider message IDs and use chunked delivery records for multi-message answers. Split failures must not cause all already-delivered parts to be resent. Scrub bot tokens embedded in request URLs from telemetry.

## Zalo

The selected product is **Zalo Bot Platform at bot.zaloplatforms.com**, not an assumed Zalo Official Account API. Its official overview documents bot-token endpoints and webhooks and describes image support. Implement a dedicated adapter; do not assume Telegram method names, schemas, limits, or group behavior apply.

Before enablement, record the actual account plan, supported message/media endpoints, webhook authentication, retry behavior, user/recipient limits, and successful sandbox tests. The initial acceptance requires a real text reply and an approved screenshot sent to a test recipient. An unavailable media capability produces an explicit authorized source-link fallback and remains a failing image-delivery acceptance gate, not a claim of full support.

Where a webhook mode lacks a verifiable origin, disable sensitive automated intake or use an approved authenticated integration gateway with a documented trust model. A secret URL alone is not equivalent to signed payload verification. Connector restrictions may block this channel without blocking web or Jira development.

## Diagnostics: Grafana, Loki, and application APIs

Distinguish AppOps' own telemetry from diagnostics of the 15 supported applications. Grafana is a visualization/integration surface; log retrieval must target the configured source, initially Loki's HTTP API, not scrape a dashboard screenshot.

`diagnostics.logs.read` accepts an approved query template ID, application, environment, time window, and bounded parameters such as request ID. The adapter enforces label scope and escapes parameters; the model cannot supply arbitrary LogQL. Initial limits: 30-minute window, 200 returned lines, 256 KiB sanitized result, 10-second query timeout, two concurrent queries per application. Raising a limit requires policy.

Return evidence with source system, query template/version, parameters hash, exact time range, truncation flag, capture time, and sanitized excerpts. Separate observed facts from hypotheses. 'No matching log' does not prove no incident occurred.

Application status connectors are explicitly mapped, read-only APIs. Database diagnostics are a later capability limited to approved parameterized views/queries with read-only credentials. No generic production SQL executor. Service mutation connectors remain disabled until the controlled-action slice and application-specific runbooks pass acceptance.

## Transport and error contract

Use bounded connect/read/total deadlines, limited response size, certificate validation, endpoint allowlists, and per-connector concurrency. Respect provider retry headers and circuit-break on repeated authentication/rate failures. Normalize failures as AUTHENTICATION_FAILED, PERMISSION_DENIED, RATE_LIMITED, TIMEOUT, INVALID_RESPONSE, CAPABILITY_UNAVAILABLE, UNKNOWN_OUTCOME, or TRANSIENT_UNAVAILABLE.

Safe reads may retry with exponential backoff and jitter. Writes follow the action ledger and provider-specific reconciliation; generic HTTP retry middleware must not repeat them. Live write tests use a designated sandbox and explicit authorization, never an arbitrary production ticket.

See [primary sources](../references.md) for provider documentation verified while authoring this design.
