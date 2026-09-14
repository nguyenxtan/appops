---
name: appops-start
description: Use when starting or resuming an AppOps task, especially after a handoff or uncertain repository state.
---

# Start an AppOps task

Read root AGENTS.md, current status, assigned slice, and relevant architecture before changing files. Verify branch, local/remote HEAD, working tree, and existing tests. Preserve unrelated changes.

State the smallest authorized deliverable and the checks that will prove it. Distinguish product requirements, selected architecture, implementation status, and missing environment facts. Do not ask the owner to reselect technologies already decided; flag only a real conflict or non-resolvable authorization prerequisite.

Load only relevant skills from [routing](../../../docs/development/agent-skills.md). Use a task branch. A documentation or feature request is not deployment or production-write approval.

Before stopping, leave exact commits, changed behavior, checks/results, not-run items, external mutations, and one next step. Never infer that prior slices passed from an optimistic handoff sentence.
