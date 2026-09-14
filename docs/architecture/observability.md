# Observability and operational traceability

## Two different concerns

AppOps must observe its own health and preserve evidence for the applications it supports. An AppOps log is not automatically a log of the user's business application. Connecting a Grafana dashboard does not create missing instrumentation in the target application.

Use OpenTelemetry for request/activity traces, Prometheus for metrics, Loki for sanitized logs, Tempo for traces, and Grafana for dashboards. Do not add Langfuse/LangSmith to the baseline merely to duplicate tracing. AI-run metadata and evaluations are stored explicitly; a specialized AI observability tool needs an ADR.

## Identity and linkage

Every request gets `request_id` and a short-lived distributed trace. Every durable workflow has `workflow_id` and `run_id`. Business investigation links use `case_id`, `action_id`, `answer_id`, `evidence_id`, and `correlation_id`.

A ticket lasting weeks is not one perpetually open trace. Each event/activity has its own spans, with span links and stable business IDs joining the history. Propagate W3C trace context across supported boundaries; do not fabricate continuity when a target system does not emit compatible IDs.

Store target request IDs, application/environment, deployment version where available, and exact evidence time ranges. Label inferred relations as inferred. The initial relationship graph is PostgreSQL links/read models, not a mandatory graph database.

## Evidence versus telemetry versus audit

| Record | Purpose | Content |
| --- | --- | --- |
| Telemetry | Debug latency/failures and capacity | Sanitized attributes; sampled traces |
| Evidence | Explain a diagnosis/action | Scoped source captures, query templates, hashes, citations |
| Audit | Account for authorized changes | Actor, decision, resource, policy, outcome, timestamp |

Audit is persisted transactionally with state changes, not only through best-effort logging. Export failure does not erase the authoritative record. Telemetry may be sampled; approval, policy, side-effect, and closure audit must not be sampled away.

Record concise evidence-based decision summaries and explicit uncertainty. Do not require or store model hidden chain-of-thought. An operator must see the evidence, applicable rule, action, and verified outcome.

## Required metrics

API errors/latency; authentication failures; denied operations; inbox/outbox oldest age; workflow queue latency; overdue wait cycles; duplicate suppression; unknown delivery outcomes; connector last reconciliation; unauthorized closure attempts; media mismatch; retrieval no-evidence/conflict rate; model latency/tokens/cost; ingestion failures; DB/storage capacity; backup age; restore-test age.

Use bounded labels such as operation, outcome, provider, and environment. Ticket IDs, emails, query text, and request IDs belong in authorized traces/evidence, not metric labels.

## Initial alerts

Alert on any unknown write outcome, audit persistence failure, unexpected closure compensation, denied privileged execution, suspected secret leakage, or workflow replay incompatibility. Alert when oldest outbox work exceeds five minutes or active-case reconciliation is stale beyond ten minutes. These are pilot thresholds, not a contracted SLA.

Alerts identify the affected connector/application without exposing ticket content. The alert channel must not depend solely on the failing connector.

## Operations timeline

Show intake, identity/application mapping, source versions, diagnosis, evidence, assigned user/ops work, exact approval, execution attempts, verification, public/internal messages, deadlines, pauses, escalation, and closure reason. Current access policy applies to this timeline as well as chat.

Maintain a sanitized export for incident review. Retention and revocation follow [security](security.md). A hash or append-only DB permission is useful integrity evidence, not proof that a privileged administrator cannot alter history.
