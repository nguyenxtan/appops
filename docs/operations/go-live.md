# Go-live gates and environment inputs

## Inputs requiring real environment facts

| Input | Required before | Safe state while missing |
| --- | --- | --- |
| Organization/application inventory and owners | Real-user onboarding | Synthetic local registry only |
| DEV/UAT/PROD mapping and permissions | Private records or operational actions | Deny unknown scope |
| Jira edition/product/project/transition mappings | Jira activation | Connector disabled |
| Verified integration identity and least-privilege scopes | Any live connector | No authenticated provider calls |
| Approved document/data classification and storage destination | Real-file ingestion | Synthetic fixtures only |
| Hosted model/provider/data-retention and budget approval | Real hosted inference | Local retrieval only |
| Follow-up calendar, exclusions, wording, and closure authority | Auto-follow-up/closure | Policy disabled |
| Approved messaging recipients, identity linking, plan limits | Telegram/Zalo activation | No private outbound content |
| AppOps host/domain/TLS/backup ownership | Hosted pilot | No deployment |
| On-call/incident owner and private reporting route | Operational acceptance | Not production-ready |

These are configuration and authorization prerequisites. They are not unresolved choices between architecture stacks. Never guess them from another project or from a screenshot.

## Required technical gates

Reproducible locked build; vulnerability/license review; real authentication and negative authorization tests; protected private media; approved knowledge publication; held-out answer/image evaluation; durable workflow restart/replay; provider sandbox contracts; ambiguous-write reconciliation; kill-switch drill; audit durability; secret-redaction checks; backup restore and measured RPO/RTO; operational dashboards/alerts; documented human fallback.

The owner accepts product usability and operating policy. A technical reviewer and automated evidence cover code and security. Required CI checks and branch protections should be enabled by an authorized repository administrator; their existence must be verified, not assumed from a workflow file.

## Activation sequence

Deploy with external actions disabled. Validate local health/auth/scope. Import only approved test knowledge. Enable source-grounded web support. Enable Jira READ_ONLY, then DRAFT_ONLY, then approved public/internal communication. Enable follow-up for selected low-risk request types. Enable auto-close only after a signed-off policy and race/compensation tests. Add diagnostics and approved operational tools separately.

No step is automatically authorized by passing the previous step. Production mutations require explicit environment and operation scope. Preserve a rollback/pause route at each stage.
