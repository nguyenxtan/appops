---
name: appops-debugging
description: Use when investigating an AppOps failure, flaky test, unexpected provider outcome, state mismatch, or performance regression.
---

# Diagnose before modifying

Capture the smallest failing behavior, exact commit/environment, and sanitized evidence. Identify the failing boundary: transport, authorization, retrieval, persistence, workflow, provider, or presentation.

Form one causal hypothesis and design a test that distinguishes it from alternatives. Reproduce first; inspect current state and operation ledger before retrying a side effect. Change the smallest responsible component and add a regression test.

Do not inflate all timeouts, remove meaningful assertions, enable broad permissions, or restart production just to hide symptoms. Distinguish definite failure from unknown remote success.

Report observed facts, inference, fix, verification, and remaining uncertainty. Follow [runbooks](../../../docs/operations/runbooks.md) for operational containment and [standards](../../../docs/development/standards.md) for code changes.
