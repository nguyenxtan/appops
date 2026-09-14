# AI runtime and model profiles

## Boundary

RAG is a retrieval-and-generation workflow, not a single model. AppOps uses one embedding model and one initial chat profile. No mandatory reranker, vision model, agent framework, or fine-tuning pipeline is introduced.

The model can summarize approved context, classify a question, draft a reply, and propose a registered action. It cannot select unrestricted application scope, grant permissions, approve itself, decide an external side effect succeeded, or close a ticket directly. Programmatic schema validity does not prove factual correctness.

## Embedding profile

Select `Qwen/Qwen3-Embedding-0.6B`, 1024 dimensions, L2 normalization, Sentence Transformers, query-side retrieval instruction, and document-side plain content. Host locally as a private process. Download model artifacts only during an approved build/provisioning step and pin the model repository revision and artifact hashes. Do not fetch or execute unpinned model code on each request.

The model card supports multilingual embeddings; Vietnamese suitability for these applications is still an acceptance test, not guaranteed by the model name. CPU is the baseline evaluation target. Measure memory, latency, and throughput before accepting its deployment sizing. The full published context window is not an invitation to embed an entire manual at once.

A text-only embedding is sufficient to retrieve a reviewed source step and its linked screenshot. Returning a stored screenshot does not require a vision model. User screenshot interpretation is outside the first release.

## Chat profile

Initial evaluation model: `openai/gpt-4.1-mini` through the OpenRouter HTTP adapter. This is a selected cost-conscious evaluation baseline, not a claim it is the best available model. Its model alias, provider slug, allowed region/data policy, structured-output capability, and operational availability must pass a live preflight before activation. Record the resolved provider/model version in each run where exposed.

Profile defaults: disabled external calls, 30-second total request deadline, 6,000-token evidence budget, 1,500-token output ceiling, at most two model calls per user turn including a single schema-repair attempt. Do not automatically escalate to a more expensive model. Reject calls exceeding organization/application budgets before dispatch. Prices and limits are versioned configuration retrieved at activation; no invented fixed pricing table is embedded in the design.

Use a strict JSON response schema and validate the result again with Pydantic. Provider routing uses an explicit allowlist and disables fallback. For approved private-context egress, require the approved data-collection/ZDR constraints; if no permitted endpoint exists, return an unavailable state and source search, not an unapproved provider.

## Answer contract

An answer has disposition ANSWERED / NEEDS_CLARIFICATION / NO_EVIDENCE / CONFLICTING_EVIDENCE / UNAVAILABLE, a concise summary, ordered instruction steps, verified source IDs, reviewed media IDs, warnings, and an optional proposed action reference. It contains no arbitrary executable code or provider URLs.

Each step identifies its actor role, server-computed current capability, and source anchors. A screenshot ID must belong to the retrieved and currently authorized source version. Post-processing must reject unknown citations, invented media, invalid step roles, and contradictions between a claimed action and the stored tool outcome.

Policy and deterministic checks decide whether an answer can be sent automatically, requires review, or is only a draft. Ambiguous state or missing evidence leads to clarification/escalation. A numerical similarity score or self-reported model confidence is not enough to authorize action.

## Prompt lifecycle

Store versioned prompt templates alongside the owning assistance adapter when implemented. Separate system instructions, user input, retrieved evidence, and tool output. Mark evidence as untrusted source content. Do not concatenate logs into a privileged instruction message.

Record prompt-template version, model profile, retrieved chunk/version IDs, tool result references, redaction profile, token usage, latency, and output disposition. Store concise evidence-based decision summaries, not hidden chain-of-thought or unbounded provider reasoning traces.

## Evaluation

Maintain synthetic public fixtures and a separately approved private evaluation set. Use a held-out question set covering Vietnamese abbreviations, no-accent input, status-dependent procedures, conflicting versions, unknown questions, wrong screenshots, and adversarial instructions. Human-reviewed expected source/step/media labels are the authority. A second model may assist scoring later but is not the sole judge.

Changing embedding model, chunking, prompt, chat model, retrieval algorithm, or provider routing requires rerunning the affected evaluation gates. Do not enable a model on the basis of successful authentication alone.

See [knowledge](knowledge.md), [security](security.md), and [acceptance](../testing/acceptance.md).
