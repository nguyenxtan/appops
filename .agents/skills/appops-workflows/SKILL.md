---
name: appops-workflows
description: Use when changing case states, Temporal workflows, durable timers, follow-up, retries, closure, or recovery behavior.
---

# Durable case behavior

Read [case workflows](../../../docs/architecture/case-workflows.md). Keep Jira facts, AppOps work state, and Temporal execution ownership distinct.

Use deterministic workflows and reference-only payloads; perform I/O through activities. Persist stable command IDs, inbox/outbox handoff, and action/delivery ledgers. At-least-once execution does not make remote writes exactly-once.

On ambiguous write outcomes, reconcile instead of blindly retrying. Start waiting only after confirmed delivery of a clear user request. Cancel stale generations on reply/takeover. No-response closure is not verified repair.

Test restart, duplicated/out-of-order events, deadline reply race, manual close/reopen, policy/calendar changes, outages, approval expiry, and history replay. Fresh provider state and current policy must guard every outward action, including overdue timers.
