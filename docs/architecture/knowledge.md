# Knowledge ingestion, retrieval, and screenshot provenance

## Scope

Initial supported inputs are native-text PDF and DOCX. The supplied examples motivate preserving headings, state conditions, ordered steps, and original screenshots; they do not justify blanket OCR or an assumption that every picture belongs to the nearest paragraph. Internal source files are not stored in this public repository.

OCR is disabled in the baseline. A scan-only or unreadable page produces a visible review finding. No importer may label a document fully ready while silently dropping content. A later OCR adapter requires its own evaluation, cost limits, and provenance label.

## Import stages

`UPLOADED -> VALIDATING -> EXTRACTING -> EXTRACTED -> INDEXING -> REVIEW_REQUIRED -> READY_FOR_PUBLICATION -> PUBLISHED`.

Failures use `FAILED` with a stage-specific error; suspicious files use `QUARANTINED`. Publication status is distinct from ingestion progress. Retry cannot publish. A changed file creates a new version; a duplicate hash in the same application/document returns the existing version unless a different parsing profile was explicitly requested.

Initial admission limits: 50 MiB upload, 300 PDF pages, 100 MiB uncompressed DOCX contents, bounded XML depth, and a 15-minute total ingestion workflow budget. These are configurable safety limits, not a throughput claim. Reject password-protected PDFs, executable attachments, unexpected archive paths, remote DOCX relationships, and unsupported formats with actionable error codes. Validate MIME signature as well as extension. Scan quarantined uploads using ClamAV before parsing in hosted environments; an unavailable scanner blocks promotion, not a bypass.

Document workers have no business or provider credentials and do not execute macros, scripts, hyperlinks, or embedded files. Bound CPU, memory, page rendering size, scratch space, and network access. Delete temporary files on completion and on worker restart cleanup.

## Native PDF processing

Use pdfplumber for characters, words, bounding boxes, page order, and native tables. Use pypdfium2 to render original pages and crops. pdfplumber supplies image positions but is not a general image-reconstruction engine; rendering the bounded original region is the canonical initial screenshot extraction method.

Normalize every bounding box to `[left, top, right, bottom]` in `[0,1]`, after applying crop box and page rotation. Store the original page number as 1-based for citation. Store rendering scale and transform version. Test rotated pages, nonzero crop origins, multi-column text, page-spanning sections, and repeated header/footer removal. Preserve an original source span before text normalization.

For each page record extracted character count, replacement-character anomalies, layout warnings, and source objects. A low character count is a review signal, not proof that OCR is required; a cover or image page may legitimately have little text.

## DOCX processing

Use python-docx and bounded OOXML relationships to preserve heading hierarchy, paragraph order, lists, tables, and inline image anchors. Store a stable block identifier and section path. Do not invent page numbers: DOCX pagination depends on rendering environment. Unsupported floating objects, text boxes, revision markup, or content that cannot be mapped confidently creates a review finding. Rendering to PDF is not silently introduced as a dependency.

## Screenshot association

A media asset is attached to a source location. A candidate link associates it with a section/step, not merely a page. Rules may propose links using source order, captions, heading boundaries, continuation markers, and explicit step labels. Confidence is not approval.

The review console shows the original page, extracted text, candidate crop, and proposed step side by side. A reviewer can select a different crop, assign the step, mark a whole-page preview, flag a sensitive region, or reject the image. Publication requires `review_status=VERIFIED` for a `STEP_IMAGE` link. Unreviewed links are never presented as verified instructions. An authorized whole-page preview must be labelled as a page preview, not as the screenshot for a specific step.

Keep source screenshot and presentation overlay separate. The system may add a reviewed numbered marker or highlight on a copy; it must not modify the original source, invent a button, or claim a guessed UI location is verified. Both images retain provenance and hashes.

Acceptance fixture: one page has the previous section's delete-confirmation image above a new activation section and its image. Activation questions must not receive the delete screenshot. This fixture is synthetic; it tests the observed class of layout risk without publishing internal images.

## Procedures and actor labels

Chunk by heading, procedure, status condition, and ordered steps. Default text window: target 750 embedding-tokenizer tokens, maximum 1,000, up to 100 tokens overlap only when a long section must split. Do not separate a safety prerequisite from its action. Repeat governing state/role conditions in derived retrieval context while retaining original source spans.

A procedure step contains instruction, required actor role, permission code, applicability, risk class, expected result, and optional link to a separately reviewed action definition. Import can propose these fields, but an authorized operator must verify them. `UNKNOWN` actor or risk prevents publishing an executable procedure. Informational content can be published without executable metadata if it is clearly non-executable.

An end-user badge means 'this user is authorized to perform this step in this application/environment now', not merely that a manual calls it a user action. Render server-evaluated capabilities. If scope or permissions are unavailable, show 'requires operator confirmation' rather than a false enabled action.

## Version and audience selection

The registry binds an approved document version to an application, environment, audience, and effective interval. Default retrieval uses that binding. New upload time is not version precedence. Conflicting instructions or two current versions for the same binding block publication. Historical requests require explicit version context and permission.

Document, chunk, image, and file access inherit at least the document's classification. Redacted derivatives may have a different approved audience, but never automatically broaden access. Retiring knowledge increments a scope-specific epoch; retrieval and delivery recheck it. Persisted answers keep historical provenance but must not expose a revoked source to a now-unauthorized reader.

## Retrieval algorithm

1. Resolve trusted organization, principal, application, environment, audience, and publication bindings before searching. If ambiguous, ask one clarification.
2. Lexical search: PostgreSQL `tsvector` with the `simple` configuration, versioned accent normalization, and an application glossary for abbreviations. Use `ts_rank_cd`; do not label this BM25 or claim Vietnamese morphological analysis.
3. Semantic search: local Qwen3-Embedding-0.6B, normalized 1024-dimensional vectors, fixed profile. Embed queries with the documented retrieval instruction; embed source chunks without that query prefix.
4. Retrieve up to 30 lexical and 30 semantic candidates inside authorized scope. Fuse with reciprocal rank fusion, initial constant 60, deduplicate by source/step, then select up to 8 chunks within a 6,000-token context budget.
5. No reranker in the baseline. Add one only after held-out evaluation demonstrates improvement over its added latency/cost.
6. Require applicable evidence for an answer. Return `NEEDS_CLARIFICATION`, `NO_EVIDENCE`, or `CONFLICTING_EVIDENCE` rather than manufacture a procedure. Similarity scores are not calibrated confidence probabilities.
7. Generate a structured answer, validate citation/media IDs against the selected context, then recheck scope at delivery.

When embeddings or chat are unavailable, authorized lexical search and source links remain available. The UI must explicitly distinguish a source-search result from an AI-generated answer. No cross-user answer cache in the initial release. A future cache key must include entitlement epoch, audience, application/environment, publication epoch, model/prompt profile, and normalized query.

## Publication and erasure

Publish in a transaction that switches the binding, bumps the epoch, and emits an outbox event. Reprocessing builds a new generation and never edits existing answer provenance. Erasure removes searchable text/vectors, revokes file access, and schedules source/derived object deletion under retention policy. Backup expiry and audit minimization are handled separately; removing a vector is not full erasure.

See [AI runtime](ai-runtime.md), [security](security.md), [data model](data-model.md), and [primary sources](../references.md).
