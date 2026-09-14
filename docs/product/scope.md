# Product scope and requirement register

## Purpose

AppOps is an operator-owned software operations platform. It supports approximately 15 applications initially and grows by adding application configuration, approved knowledge, connector adapters, and operational procedures, not by cloning one bot per application.

The first useful release answers how-to questions with approved source references and correctly associated screenshots. The target platform accepts Jira tickets, guides users, gathers permitted diagnostics, assigns work to the appropriate human role, follows up durably, and requests or performs only authorized actions.

## User-supplied requirements

| ID | Requirement | Owner document |
| --- | --- | --- |
| R01 | Import user guides and answer from their content | Knowledge |
| R02 | Attach the correct original screenshot; no invented interface images | Knowledge |
| R03 | Separate approximately 15 applications and their knowledge | Security and data model |
| R04 | Native PDF text does not require blanket OCR | Knowledge |
| R05 | Expose web, Telegram, and the specified Zalo Bot Platform channel | Integrations |
| R06 | Grow toward software operations, not only chat | Overview and case workflows |
| R07 | Integrate Jira intake, replies, follow-up, and closure policies | Case workflows and integrations |
| R08 | Mark steps by the role allowed to perform them | Security and knowledge |
| R09 | Integrate logs, Grafana-related diagnostics, and application APIs | Integrations |
| R10 | Trace evidence, decisions, approvals, and outcomes | Observability |
| R11 | Support controlled expansion into automation | Security and durable work |
| R12 | Maintain clean code and concrete module boundaries | Module boundaries and standards |
| R13 | Keep canonical architecture and delivery docs in Git | Documentation index and status |
| R14 | Supply repository-local skills for coding agents | Agent skills |
| R15 | Operate, recover, pause, and maintain the platform itself | Deployment and runbooks |

## Selected product rules

These are design decisions made under delegated authority, not claims that the user already has them configured.

One initial organization contains many applications. Every application has environments, ownership, role grants, knowledge publication bindings, connector bindings, and a follow-up policy. Include `organization_id` from the beginning; do not sell multi-tenant isolation as proven before its tests pass.

A chat conversation is not automatically a ticket. Create an internal case only on an explicit support request, escalation, or a linked external ticket. Case management exists in the foundation; external Jira automation is delivered in its own gated slice.

Jira remains authoritative for Jira status, assignee, comments, and resolution. AppOps stores work state, evidence, action decisions, and a projection of Jira facts. No-response closure and technically resolved outcomes remain distinct.

A procedure step can be `END_USER`, `OPS_L1`, `OPS_L2`, `APPLICATION_ADMIN`, `DEVELOPER`, `DBA`, `INFRA`, `SECURITY`, or `VENDOR`. An instruction is not permission, and an approved guide is not an executable action grant.

## Explicit exclusions from the first release

No unrestricted shell, model-generated SQL execution, automatic production restart, autonomous access grants, training a foundation model, data warehouse, feature store, Kafka, Kubernetes, multi-agent planning swarm, or multi-system remediation transaction. These need a separate decision and acceptance evidence before introduction.

OCR and user-uploaded screenshot understanding are later capabilities. The first importer detects unsupported scan-only or unreadable pages and routes them to review rather than pretending ingestion is complete.

## External facts not yet provided

Jira edition and installed products, project workflows, approved closure rules, user directory, data-handling approvals, hosting account, application inventory, traffic, document volume, and contractual SLA have not been supplied. They are deployment inputs, not a reason to leave the internal architecture undefined. Defaults stay safe until [go-live inputs](../operations/go-live.md) are completed.

## Success

Measure source correctness, screenshot correctness, permission isolation, response quality, case delivery reliability, escalation quality, reopen rates, and recovery. Do not optimize the percentage of tickets closed at the expense of unresolved user issues. Numeric initial acceptance targets are specified in [acceptance](../testing/acceptance.md), not claimed as current results.
