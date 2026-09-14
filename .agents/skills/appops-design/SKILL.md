---
name: appops-design
description: Use when changing AppOps architecture, technology, module ownership, contracts, or implementation-slice boundaries.
---

# Design within the baseline

Read [overview](../../../docs/architecture/overview.md), [boundaries](../../../docs/architecture/module-boundaries.md), and the applicable ADRs. Identify the requirement, current owner, and affected invariants.

Keep existing decisions unless a measured constraint or correctness issue justifies change. Compare the smallest compatible change with alternatives; record consequences, migration, failure handling, security, tests, and rollback in an ADR. Do not introduce a platform dependency for appearance alone.

Obtain approval for a materially new scope. Already-delegated architecture selection does not require repeatedly asking the owner to choose frameworks. Plan one independently testable slice using actual paths/interfaces. Do not implement future placeholder services or silently turn a plan into a deployment.

Output: decision, ownership changes, specific contracts, acceptance evidence, and excluded work.
