# Isolated document-worker contract

This document refines the process boundary in [overview](overview.md) and the stages in [knowledge](knowledge.md). It does not introduce another business service.

## Durable handoff across namespaces

Core and document workers use different Temporal namespaces per environment. A cross-namespace job is not implemented as a child workflow that assumes a shared namespace.

A core activity uses a narrowly authorized Temporal client to start `DocumentParseWorkflow` in the document namespace with stable workflow ID `parse/<organization_id>/<document_version_id>/<parser_profile>`. Starting again with the same identity must join/inspect the existing execution according to the configured reuse policy, not produce another publication candidate. The activity durably records the external workflow reference in the ingestion job.

Core activities inspect the parse result using bounded polling and heartbeats, or a reference-only completion event through an authenticated internal endpoint. The default implementation is bounded activity polling with heartbeats. On retry, reconnect to the recorded workflow rather than start an unrelated job. The core ingestion workflow owns the 15-minute total ingestion budget and cancellation handling.

The parse workflow receives only job/version IDs, parser profile, admission limits, and opaque source/output references. It produces a manifest reference and stage diagnostics. The document worker cannot publish knowledge or write business tables.

## File access without business credentials

The document worker has a dedicated workload identity limited to its document namespace and a private file-capability endpoint. This identity cannot call business APIs or request arbitrary object keys. The core capability endpoint validates the worker identity, active assigned job, source/output ownership, and job state before granting a short-lived single-object read or reserved-prefix write capability.

Do not place signed storage URLs, passwords, OAuth tokens, or long-lived storage keys in Temporal history or logs. The worker exchanges the opaque reference for a fresh capability only inside an activity and keeps it in process memory. Expired capability renewal rechecks the current job; cancelled jobs lose renewal rights. File capabilities are not a substitute for document-parser sandboxing or output validation.

## Manifest validation

The manifest includes schema version, job/document/version/profile IDs, source SHA-256, page/block count, extracted text references, normalized source anchors, rendered crop references and dimensions, and completeness warnings. Core validates IDs against the reserved job, object-prefix ownership, size/count bounds, hashes, coordinate range, and schema before indexing.

Never trust a returned storage path, URL, application ID, role label, or publication instruction supplied by a parser. Reject unexpected objects and retain a sanitized error. Oversized results stay in private storage rather than workflow payloads.

## Acceptance

Test worker restart, duplicate start, timeout/cancellation, expired capability, wrong job/object reference, forged manifest ownership, invalid crop coordinates, missing pages, parser attempting business API access, and failure after object write but before result recording. Orphan temporary outputs are reclaimed by a scoped retention job; publication remains an explicit reviewed core command.
