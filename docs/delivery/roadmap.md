# Implementation roadmap

## Delivery rule

Every slice delivers tested behavior, a usable path, updated canonical docs, and an evidence report. No slice can claim later capabilities. Application/tenant isolation, audit, and version-aware design are foundation requirements, not a late hardening phase.

| Slice | Deliverable | Dependencies | Exit gate |
| --- | --- | --- | --- |
| S0 | Runnable web/API; locked builds; real local OIDC; application registry; scoped DB/migrations; baseline telemetry; Temporal smoke | This documentation baseline | Clean install/build; authenticated app list; denial tests; DB-down readiness; durable smoke; no external writes |
| S1 | Internal case core; deterministic policy; action/approval records; inbox/outbox; durable case waits; operator timeline/pause | S0 | State/authorization/race tests with real PostgreSQL/Temporal; synthetic case survives restart |
| S2 | Native PDF/DOCX ingestion; review; publication; hybrid retrieval; grounded web answers and correct images; actor badges | S0-S1 | Knowledge/media evaluation; 15-application isolation; safe provider degradation |
| S3 | Jira Cloud adapter; edition/capability preflight; draft replies; approved communication; follow-up/closure policies | S1-S2 | Live sandbox evidence; public/internal separation; timer/race suite; owner activation per project |
| S4 | Telegram and specified Zalo Bot Platform channels; verified identity links; approved media delivery | S2-S3 | Each provider's actual text/media/auth/retry acceptance; partial delivery recovery |
| S5 | Read-only Loki and application diagnostics; linked evidence and uncertainty; internal/user audience separation | S1-S3 | Scope/query limits; real sandbox diagnostics; no raw confidential leakage |
| S6 | Selected approved operational actions; runbook binding; verification; compensation; controlled automation | S3-S5 | Application-specific risk review, approval/race tests, kill-switch drill, postcondition proof |

The first useful internal knowledge release is S2. S3 introduces actual Jira workflow behavior. S6 does not mean unrestricted autonomous operations; only specifically accepted actions are enabled.

## Scope boundaries

S0-S2 can develop entirely with synthetic fixtures and approved local dependencies. A disabled hosted-model profile still permits source search. External credentials are not required to write a connector contract; they are required to claim it works live.

S3 must confirm the actual Jira edition. If it is Data Center, add a dedicated edition adapter before activation while preserving the core contracts. This is a bounded connector change, not silent Cloud compatibility.

## PR discipline

Use small sub-PRs when a slice exceeds a coherent review unit. Preserve a single canonical slice plan and status. Do not mix deployment, provider enablement, or production data import into a feature PR by default. One agent implements; an independent technical review is requested when available; the owner reviews product/operational outcomes.

Before a slice begins, create its execution plan from the relevant architecture and acceptance rows. Only [S0](s0-foundation.md) is planned task-by-task in this foundation. Later plans must use actual code interfaces, not speculative files that may no longer match implementation.
