---
name: appops-knowledge
description: Use when editing document ingestion, source structure, screenshot links, retrieval, publication, or answer provenance.
---

# Preserve knowledge provenance

Read [knowledge architecture](../../../docs/architecture/knowledge.md). Use native extraction first. Do not run OCR by default or silently discard unreadable content.

Preserve source text, page/block anchors, crop transforms, document/version, audience, and review state. Test the page that contains an unrelated previous-section image before the desired step image. Only reviewed links qualify as verified step screenshots.

Apply trusted application/environment/audience/version filters before retrieval and again at delivery. Keep instructions, status prerequisites, actor roles, and safety warnings together. Similarity scores are not permissions or calibrated confidence.

Changing chunking, model, source links, or retrieval requires targeted and held-out evaluation. Unknown evidence must produce clarification/abstention. Never auto-publish imported action permissions or commit internal manuals/screenshots.
