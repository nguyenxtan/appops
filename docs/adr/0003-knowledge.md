# ADR-0003: Native knowledge ingestion and PostgreSQL retrieval

Date: 2026-09-14. Status: Selected baseline; implementation not started.

## Context

Initial guides have native text and screenshots. Wrong image/step association is more relevant than blanket OCR.

## Decision

Use pdfplumber, pypdfium2, and python-docx; preserve provenance and review image links. Disable OCR initially. Use PostgreSQL full-text plus pgvector and local Qwen3 embeddings, without a mandatory reranker.

## Alternatives

Forking a full RAG product imports its UI, authorization, schema, and upgrade constraints. Qdrant and blanket OCR add unproven dependencies.

## Consequences

AppOps owns publication, review, evaluation, and authorization. Unreadable scans produce visible review findings. New OCR/search adapters need acceptance evidence. See [knowledge](../architecture/knowledge.md).
