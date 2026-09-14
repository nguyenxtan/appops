# Operator runbooks

These are target procedures for the AppOps operator. They are not evidence that the runtime controls already exist. Each deployed runbook must be exercised before it is marked operational.

## Unknown external write outcome

Trigger: an action times out after the remote API may have accepted it. Pause automated writes for the affected case/connector. Inspect action ID, content hash, delivery ID, source ticket state, and operation marker. Reconcile with the provider. Confirm delivered, confirm definitely absent before an approved retry, or leave UNKNOWN_OUTCOME for human resolution. Never clear the ledger and resend blindly. Verify no duplicate message/transition and record evidence.

## Jira outage or expired credentials

Stop new automatic outward writes and no-response closures. Retain durable intake/outbox work. Alert through an independent route. Confirm provider status, credential validity, scopes, and rate limits without logging the credential. Restore access through an approved secret rotation. Reconcile active cases and unknown deliveries before resuming; collapse obsolete reminders instead of sending a backlog. Record SLA impact without silently pausing contractual clocks.

## Wrong source or screenshot reported

Pause or retire the affected publication binding. Preserve answer/source/version/media IDs. Review the original section and media link; do not silently edit an already-published source version. Correct via a new reviewed version/generation, rerun targeted and held-out tests, publish, and increment knowledge epoch. Notify affected users through approved channels if the wrong guidance could cause harm.

## Worker backlog or crash

Inspect oldest outbox/task age, worker capacity, dependency health, and resource limits. Restart/scale only the affected process under the operator's deployment permissions. Use durable IDs to resume; do not recreate every workflow. Check replay compatibility and dead-letter/unknown outcomes. Confirm backlog drains without duplicates.

## Model unavailable or budget exhausted

Disable generation for the affected profile; preserve authorized lexical search and source access. Show UNAVAILABLE rather than invent a response. Inspect provider health, approved route, limits, and budget. Do not route to an unapproved provider or raise spend automatically. Run a bounded preflight before re-enabling.

## Suspected credential or private-data exposure

Disable the affected connector/profile, revoke/rotate the credential, restrict access to exposed material, and preserve a sanitized incident record. Assess logs, traces, Git history, artifacts, external messages, and provider retention. File deletion alone is insufficient. Coordinate history cleanup or third-party erasure with the owner; do not claim screenshots already delivered to users were retracted.

## Restore from backup

Restore into isolation; keep all outbound capabilities paused. Validate AppOps/Temporal/Keycloak schemas and object manifests. Reconcile external ticket state and action deliveries newer than the restore point. Test one synthetic case end-to-end. Resume by application, not globally. Record achieved RPO/RTO and unresolved discrepancies.

## Human takeover and emergency stop

An authorized operator pauses the case, application, connector, or whole platform. Verify queued actions are denied at execution and in-flight effects are visible. Assign a human owner and preserve evidence. Resumption requires explicit authority plus current state/credential/policy checks. A pause does not undo an action already accepted by a remote service.
