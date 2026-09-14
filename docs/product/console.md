# Operations console

## Interface principles

One console serves users/operators through server-computed capabilities. Vietnamese is the initial interface language. Keep application/environment visible and production unmistakable. A hidden button is not authorization; a disabled action must explain why.

Asynchronous screens distinguish queued, processing, review required, delivered, failed, and unknown outcome. Never show 'done' solely because an API returned 202.

## Navigation

| Area | Audience | Behavior |
| --- | --- | --- |
| /support | Authorized user | Select scope; ask; view sources/screenshots; request help |
| /cases | Ops | Filter by application, state, owner, age, severity, overdue/pause |
| /cases/{id} | Scoped participants | Replies, internal notes, assigned work, evidence, deadlines, Jira state |
| /knowledge | Editor/approver | Versions, warnings, publication bindings |
| /knowledge/review/{id} | Reviewer | Source page/block, text, crops, actor/risk labels, approval |
| /applications | Administrator | Ownership, environments, roles, approved bindings |
| /approvals | Approver | Exact target/input/evidence/risk/expiry; approve/reject |
| /integrations | Scoped admin | Health, reconciliation, scopes, mode, test results; no secrets |
| /automation | Ops/policy admin | Pause controls and affected queued/in-flight actions |
| /audit | Authorized reviewer | Redacted actor/action/resource/outcome history |
| /usage | Owner/ops | Budgets, estimates, latency, quality |

These are target views. Shared visual primitives use shadcn/ui; business behavior lives in feature folders.

## Knowledge answer

Show disposition, ordered steps, and badges: 'Bạn có thể thực hiện', 'Cần bộ phận vận hành', or 'Cần người có quyền phê duyệt'. Derive badges from authorization and procedure metadata. Show the approved image beside its step, source/version/page or DOCX section, and uncertainty. Provide an authorized full-size view.

Expose a runnable button only for a registered, authorized action. A user-performed step does not imply AppOps can automate that application's interface.

## Ticket workbench

Separate public replies from internal notes and show recipients before sending. Display the follow-up deadline, business timezone/calendar, reminders, exclusions, and pause reason. Jira status and AppOps work state are distinct.

Evidence panels distinguish observations, hypotheses, missing telemetry, truncation, and verification. Human takeover, reassignment, cancellation, and pause preserve history.

## Accessibility

Require keyboard operation, visible focus, labelled inputs, semantic tables, readable errors, responsive layout, and risk cues beyond color. Playwright behavioral/accessibility checks cover critical journeys. Screenshot comparison alone does not prove behavior or permission correctness.
