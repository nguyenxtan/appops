# Repository agent skills

## Purpose and limits

Skills provide reusable working procedures. AGENTS.md supplies standing project rules; architecture documents supply design authority; code/tests enforce behavior. A skill is not a runtime permission boundary, an installed production agent, or proof that a coding model will always comply.

The skills are authored specifically for this repository and stored in `.agents/skills/<name>/SKILL.md` with standard `name` and `description` frontmatter. Codex supports this repository location. No global plugins or skill collections are installed or overwritten by this change.

## Routing

| Skill | Use when |
| --- | --- |
| [appops-start](../../.agents/skills/appops-start/SKILL.md) | Starting/resuming any assigned AppOps task |
| [appops-design](../../.agents/skills/appops-design/SKILL.md) | Changing architecture, contracts, ownership, or slice scope |
| [appops-tdd](../../.agents/skills/appops-tdd/SKILL.md) | Implementing a behavior or fixing a defect |
| [appops-knowledge](../../.agents/skills/appops-knowledge/SKILL.md) | Editing ingestion, retrieval, publication, or screenshot association |
| [appops-workflows](../../.agents/skills/appops-workflows/SKILL.md) | Changing case states, timers, retries, closure, or Temporal work |
| [appops-connectors](../../.agents/skills/appops-connectors/SKILL.md) | Adding/changing Jira, channels, diagnostics, or other external adapters |
| [appops-security](../../.agents/skills/appops-security/SKILL.md) | Changing identity, scope, policy, approvals, secrets, or data delivery |
| [appops-observability](../../.agents/skills/appops-observability/SKILL.md) | Adding evidence, audit, telemetry, or incident linkage |
| [appops-console](../../.agents/skills/appops-console/SKILL.md) | Editing user/operations UI or capability-driven controls |
| [appops-debugging](../../.agents/skills/appops-debugging/SKILL.md) | Investigating failures, inconsistent outcomes, or flaky tests |
| [appops-verification](../../.agents/skills/appops-verification/SKILL.md) | Claiming completion, publishing a PR, or preparing a release |
| [appops-review](../../.agents/skills/appops-review/SKILL.md) | Reviewing implementation, feedback, security, or architecture compliance |

Load `appops-start` first, then only the skills relevant to the change. For example, Jira follow-up needs workflows, connectors, security, TDD, and verification; a documentation spelling fix does not need the model/parser stack.

## Quality checks

`catalog.json` is the machine-readable inventory. Documentation tooling checks names, descriptions, folder alignment, links, duplicate entries, and pressure-scenario coverage. Each skill is deliberately short and refers to canonical docs instead of copying them.

[Pressure scenarios](../../tests/skills/scenarios.json) specify baseline and with-skill behavioral tests. Their current state is **NOT_RUN**: this authoring session does not provide an independent coding-agent execution harness. Do not promote static validation into a claim of proven behavioral effectiveness.

S0 must run these scenarios in isolated agent sessions, record model/runtime, baseline behavior, with-skill behavior, evidence, and failures, then improve the smallest relevant skill. Evaluate both overreach and unnecessary refusal. A future agent should not block authorized implementation merely because a skill describes approval gates already satisfied by the assigned scope.

## Maintenance

Update the owning skill when a recurring judgment error is observed. Keep mechanical checks in code/tests. Add a new skill only for a repeated task class not covered by this inventory; avoid a skill per file or provider endpoint. Third-party skill adoption requires source/version/license review and must not silently replace repository policy.
