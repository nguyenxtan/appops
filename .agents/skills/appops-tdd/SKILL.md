---
name: appops-tdd
description: Use when implementing or fixing an AppOps behavior, including authorization, persistence, workflow, and UI behavior.
---

# Behavior before implementation

Name the invariant and the production mistake that would violate it. Write a minimal failing test and observe the intended failure. Implement the smallest passing behavior, then refactor without changing the invariant.

Assert observable results, denied effects, or stored state, not only mock-call counts. Use real PostgreSQL for RLS/transactions and a real Temporal test service for durability. Provider-shaped mocks prove contract handling, not live compatibility.

Test unhappy paths and concurrency for side effects. Never delete a safety assertion, bypass authorization, or weaken type checking to obtain green CI. Run related tests and the required slice suite before reporting success.

Follow [engineering standards](../../../docs/development/standards.md) and [acceptance](../../../docs/testing/acceptance.md). Keep fixtures synthetic and free of real user data.
