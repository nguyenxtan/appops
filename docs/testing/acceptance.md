# Acceptance matrix

All thresholds are initial engineering gates, not current results or contractual promises. Do not enable real-data automation until the applicable gates have evidence.

## Requirement coverage

| Requirement | Required evidence | First slice |
| --- | --- | --- |
| R01/R04 | Native PDF/DOCX ingestion; scan-only warnings; no blanket OCR calls | S2 |
| R02 | Verified step/image provenance; wrong-image adversarial fixture; authorized media delivery | S2 |
| R03 | Cross-organization/application/environment/audience denial for records, retrieval, files, and cached/resumed responses | S0-S2 |
| R05 | Web journey; Telegram text/photo; actual Zalo Bot Platform text/media sandbox acceptance | S2/S4 |
| R06/R08 | Case state guards and actor-tagged steps; capabilities match current policy | S1-S2 |
| R07 | Duplicate/out-of-order Jira events, public/internal comments, timers, manual close/reopen, unknown-write reconciliation | S3 |
| R09 | Scoped bounded Loki/API reads, truncation, missing logs, no arbitrary SQL/LogQL | S5 |
| R10 | Case-to-evidence/action/approval/delivery trace links with privacy checks | S1 onward |
| R11 | Bound approval, kill switch, execution revalidation, postconditions, compensation | S6 |
| R12/R13 | Import boundaries, type/lint/tests, doc links, truthful status, ADR alignment | Every slice |
| R14 | Skill syntax/catalog checks and independent behavioral scenarios | Foundation and S0 |
| R15 | Backup/restore drill, paused restore, workflow replay, provider outage and operator takeover | Before hosted acceptance |

## Knowledge evaluation

Create at least 150 labelled questions across the initial 15 applications before broad release. Include at least 30 negative/conflicting/unauthorized examples, Vietnamese abbreviation/no-accent input, same terms across applications, state-dependent steps, and image adjacency traps. Public fixtures are synthetic; approved private evaluation data stays outside Git. Keep at least 30% held out from prompt/retrieval tuning.

Initial gates: expected source in top 8 at least 90%; human-judged supported/correct answers at least 90% on answerable questions; correct abstention/clarification at least 95% on negative cases. Unauthorized disclosure: zero. Verified screenshot IDs and version provenance: 100% on the labelled screenshot set. Report denominators, failures, and uncertainty; do not report a percentage without the test set.

A failed retrieval gate is not fixed by increasing model creativity. A failed media gate is not hidden by disabling the test. A PDF with incomplete extraction must not be counted as fully ingested.

## Workflow and delivery gates

Every critical race scenario must pass: duplicated webhook, out-of-order comment, bot loop, human reply at close deadline, connector outage, unknown remote write result, stale wait generation, expired approval, changed action hash, manual takeover, unsupported transition, and human closure without technical verification.

A restart test must prove persisted work resumes without duplicated outward effects. A point-in-time restore test must leave outbound actions paused until reconciliation. Temporal history replay must pass for the supported in-flight workflow versions.

No-response closures are counted separately from technical resolutions. Measure reopened cases and operator overrides to detect harmful automation. No auto-close policy is activated merely because tests pass; the application owner must approve it.

## Performance targets

On the documented pilot profile, evaluate 20 concurrent users, four concurrent generations, and two ingestion jobs with representative source volume. Initial targets: authorized non-AI API p95 under 500 ms; retrieval p95 under 2 seconds; complete supported chat p95 under 15 seconds under the configured provider profile. Record provider versus local time and document volume. Failing a target blocks a capacity claim, not permission checks.

Do not extrapolate from '15 applications' to 100,000 users. Run sustained load, saturation, recovery, and noisy-neighbor tests before changing capacity claims.

## Evidence classes

STATIC = repository checks; UNIT = isolated behavior; INTEGRATION = real local dependencies; CONTRACT = provider-shaped fixtures; LIVE_SANDBOX = actual approved provider account; PRODUCTION = explicit controlled production evidence. One class cannot substitute for another. Record commit, command, environment, dataset/profile versions, timestamp, result, artifacts, and limitations.

Skill scenarios require a baseline and a with-skill agent run in separate controlled sessions. Until performed, label behavioral skill efficacy NOT_RUN. File validation alone does not prove an agent follows instructions.
