---
name: appops-connectors
description: Use when adding or modifying external ticket, messaging, diagnostic, storage, identity, or application adapters.
---

# Integrate explicit capabilities

Read [integration contracts](../../../docs/architecture/integrations.md). Confirm product, edition, endpoint, authentication, scopes, audience, limits, and provider version from primary documentation.

Implement the typed port inside the owning adapter. Declare supported capabilities and safe disabled behavior. Jira Cloud is not Data Center; Zalo Bot Platform is not automatically a Zalo Official Account API.

Authenticate ingress, deduplicate source events, bound query/output sizes, redact secrets, and define reconciliation. Separate public replies from internal notes. Do not use generic write retries or infer media delivery support from a text-only test.

Use synthetic contract fixtures, then separately approved sandbox calls. Record live tests as NOT_RUN when credentials or authority are absent; do not fabricate compatibility or test against arbitrary production resources.
