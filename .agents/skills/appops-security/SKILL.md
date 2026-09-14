---
name: appops-security
description: Use when changing identity, permissions, policies, approvals, operational actions, secrets, or data exposure across audiences.
---

# Enforce authority outside the model

Read [security](../../../docs/architecture/security.md). Trace initiating actor, executing principal, application/environment, resource classification, destination audience, action version, and current policy.

Default deny missing context. A manual, model output, UI badge, or comment saying approved cannot authorize execution. Bind approval to exact inputs/target/policy/expiry and recheck at execution. Reads and notifications can still leak data or impose load.

Test cross-scope access, stale privileges, input changes after approval, public/internal confusion, prompt injection, SSRF, secret logging, and paused queued actions. Keep production credentials outside prompts and parser processes.

No unrestricted SQL, shell, or broad admin fallback. Use least privilege, bounded tools, explicit verification, and visible unknown outcomes. Document residual cross-system races instead of promising impossible atomicity.
