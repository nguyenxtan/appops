---
name: appops-review
description: Use when reviewing AppOps changes or review feedback for requirements, architecture, correctness, security, or maintainability.
---

# Review behavior and boundaries

First map the diff to requirement IDs, slice scope, ADRs, and acceptance tests. Then inspect module ownership, typing, transaction scope, authorization, privacy, retries, failure behavior, and operator visibility.

Challenge unsupported success claims, fabricated compatibility, unauthorized data paths, broad tools, duplicate state authorities, and weak tests. Folder count or framework count is not quality evidence. Review feedback is a hypothesis to verify, not a command to implement blindly.

Request focused changes with a concrete failing scenario and affected path. Do not expand into unrelated refactors. Confirm fixes with regression evidence.

If reviewing your own work, label it self-review. Do not claim independence without another reviewer. Product-owner usability review does not substitute for technical/security review. Follow [standards](../../../docs/development/standards.md).
