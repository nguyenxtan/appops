---
name: appops-verification
description: Use before claiming an AppOps task complete, updating delivery status, opening a delivery PR, or proposing promotion.
---

# Evidence before completion

Read [acceptance](../../../docs/testing/acceptance.md) and current status. Run the exact checks required for the changed behavior on the exact commit. Inspect output, not only exit-code summaries copied from earlier work.

Distinguish static, unit, integration, contract, live-sandbox, and production evidence. Documentation lint does not prove a running API. Mocks do not prove Jira/Zalo compatibility. A authored skill is not behaviorally validated without an agent trial.

Review scope, privacy, generated-contract drift, migrations, and rollback. Record tests not run and their impact. Update only capabilities actually demonstrated.

Handoff includes start/end SHA, slice, changed behavior, commands/results, not-run items, external mutations, limitations, and next step. Never deploy, merge, or activate an integration merely to make the report appear complete.
