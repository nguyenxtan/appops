---
name: appops-observability
description: Use when adding or changing traces, audit, evidence, metrics, redaction, retention, or operational investigation links.
---

# Make outcomes explainable

Read [observability](../../../docs/architecture/observability.md). Separate telemetry, evidence, and audit. Persist mandatory audit with the state change; do not rely on sampled logs.

Link short request/activity traces with case/action/evidence IDs. Do not keep one multi-week span open or invent a target system's missing correlation ID. Mark inferred relations and unverified hypotheses.

Record source/version, query bounds, approval, action outcome, and verification. Store concise evidence-based summaries, not hidden model reasoning. Scrub prompts, headers, token-bearing URLs, personal data, and raw confidential logs by default.

Keep metric labels bounded. Test redaction, audit-write failure behavior, evidence authorization, retention, and timeline completeness. An observed log pattern supports a hypothesis; it does not alone prove root cause.
