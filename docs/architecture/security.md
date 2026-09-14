# Security, policy, and human control

## Trust boundaries

Untrusted inputs include ticket bodies, attachments, guides, log lines, webhook payloads, model output, and connector results. They cannot define tools, privileges, destinations, approval rules, or system prompts. An instruction embedded in a PDF or Jira comment is data, not an operator command.

The public ingress, browser, backend, document worker, model provider, connector targets, storage, and identity provider are separate trust boundaries. The public Git repository is not an operational knowledge store.

## Identity and sessions

Use Keycloak OpenID Connect authorization-code flow with PKCE, state, and nonce; Authlib handles protocol processing in the API. Use an opaque HttpOnly, Secure, SameSite=Lax browser session cookie backed by a hashed session record. Mutating requests require CSRF protection and origin checks. Do not store access tokens in browser localStorage or use unverified identity headers from the web console.

Validate issuer, audience, signature, expiry, and allowed algorithms. Key rotation and logout/revocation must be tested. Local fake identities are permitted only in a clearly isolated test fixture, never as a deployed 'dev login'.

Telegram/Zalo identity linking requires a one-use, five-minute token initiated by an authenticated user. Bind external account, connector instance, organization, and principal. Names, phone numbers, email text in a message, and LLM guesses cannot establish identity. Group channels are disabled for private operational content in the first release.

## Authorization decision

A deterministic policy evaluator receives principal, initiating actor, executing service identity, organization, application, environment, resource classification, destination audience, action definition/version, current state, and relevant approval. It returns `ALLOW`, `DENY`, or `REQUIRE_APPROVAL` with reason codes and policy version.

The evaluator is a typed Python domain module, not natural-language policy interpretation and not a separate policy service in the baseline. Policies are schema-validated, reviewed versions. Default deny applies when any required attribute is unknown. LLM confidence cannot bypass it.

Effective permission is the intersection of the allowed workflow, service identity capability, application/environment policy, and the initiating context. A service may collect restricted diagnostics under its own approved role, but that does not entitle the requesting user to receive the raw results. Evaluate outbound audience separately and produce a reviewed/sanitized user explanation or internal note.

Roles include END_USER, OPS_L1, OPS_L2, APPLICATION_ADMIN, DEVELOPER, DBA, INFRA, SECURITY, VENDOR, KNOWLEDGE_APPROVER, and PLATFORM_ADMIN. Platform administration is not an automatic right to every application's private content. Do not claim the customer application's live permissions are known unless its connector supplies verified entitlement data; otherwise use approved AppOps grants and label the limitation.

## Action classes and defaults

| Class | Examples | Default execution rule |
| --- | --- | --- |
| READ | Approved log template, status lookup | Scoped permission, query bounds, output classification required |
| COMMUNICATE | Jira comment, user reminder, image attachment | Audience check and delivery ledger; external automatic sending starts disabled |
| MUTATE_REVERSIBLE | Approved scoped retry | Human approval in first operational-action release; later policy may allow specific proven actions |
| MUTATE_DESTRUCTIVE | Delete or overwrite operational data | Disabled in baseline |
| PRIVILEGED | Access grant, secrets, unrestricted shell | Disabled in baseline; separate security design required |

An operation is not low risk because it is called 'retry' or 'refresh'. A retry can duplicate a shipment, payment, or downstream job. Risk classification includes business effects, blast radius, reversibility, rate, environment, and verification coverage.

## Approval binding

Persist the exact action definition/version, target resource, environment, canonical input hash, initiator, executor, policy version, evidence IDs, approver, decision, and expiry. Default expiry for an operational approval is 30 minutes. A policy can shorten this; it cannot silently remove approval.

Approver permission is checked both at approval and execution. Changed parameters, target version, policy, risk, or evidence freshness invalidate the approval. Approval is single-use, consumed transactionally with action reservation. High-impact operations prohibit self-approval and require the configured separation of duties.

State must be revalidated immediately before execution. Where a provider supports conditional writes, use them. Otherwise document the remaining race and compensation; do not pretend local locks protect an external system.

## Execution safety

The model receives capability descriptions, never credentials. Only registered adapter functions execute. Network destinations come from administrator-approved connector configuration. Reject private/link-local/metadata destinations for user-supplied URLs; validate DNS and redirects to prevent server-side request forgery. Do not fetch arbitrary ticket URLs automatically.

Apply per-tool input bounds, rate/concurrency limits, timeouts, operation ledger, and postcondition checks. READ actions can also expose secrets or cause load; enforce time windows, rows, output size, and query allowlists. No arbitrary SQL, LogQL, shell, or user-defined code execution.

Global, organization, application, connector, and individual-case pause controls are mandatory. A pause prevents newly authorized side effects and blocks queued actions at the execution guard. It cannot undo already-sent operations; uncertain in-flight effects remain visible for reconciliation.

## Privacy and AI egress

Initial classifications: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED. All imported documents default to INTERNAL until reviewed. Only PUBLIC or explicitly approved/redacted INTERNAL context can leave for a hosted chat model. CONFIDENTIAL and RESTRICTED content stays in local retrieval unless the owner approves a separate compliant processing profile.

Hosted AI is disabled until the organization approves provider, retention policy, routing, budgets, and content classes. Use OpenRouter provider allowlisting, no fallback, and required data-policy constraints. Provider ZDR settings do not remove AppOps' own storage/telemetry obligations and are not proof of an organizational compliance requirement.

Store application secrets as mounted runtime secrets. OAuth tokens that must rotate dynamically may be envelope-encrypted in `credential_records` with authenticated encryption and a key stored separately from PostgreSQL. Never put encryption keys in the same database or image. Redact token-bearing Telegram/Zalo URL paths, Authorization headers, signed URLs, and session cookies from access logs and traces.

## Knowledge and media delivery

Recheck authorization when delivering an answer, opening a source, downloading an image, or sending a ticket comment. Use opaque object IDs through the authenticated API; do not persist public URLs in answers. The hosted storage adapter uses private objects. Temporary capabilities are short-lived and scoped to one object/operation. Deleting a capability or revoking future access cannot retract a screenshot already sent to an external messaging platform.

Do not attach unredacted screenshots or raw logs to public Jira comments. Internal JSM notes and customer-visible replies have separate capabilities. Unknown visibility fails closed.

## Retention baseline

These are proposed technical defaults requiring owner approval before real data ingestion: sanitized telemetry 30 days; quarantined raw webhook payloads 7 days; diagnostic evidence 30 days; conversations 90 days; case/audit records 365 days; active published knowledge until retired. Retention and legal holds are configurable by classification and source.

Erasure removes indices, revokes access, schedules object deletion, and records a minimized audit tombstone. Explain backup expiry separately. Do not promise immediate deletion from third-party message history or provider systems outside AppOps control.

## Required abuse tests

Cross-application retrieval and media access; stale/revoked entitlement; prompt injection in a guide or log; fake approval in a comment; mismatched action hash; public/internal Jira confusion; external identity spoofing; SSRF; malformed/oversized document; path traversal; leaked URL token; mass tool invocation; stale action after kill switch; model requesting an unregistered tool; operator role attempting a production mutation without approval.
