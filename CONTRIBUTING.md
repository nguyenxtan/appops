# Contributing

Read [AGENTS.md](AGENTS.md) and [engineering standards](docs/development/standards.md). Use short-lived branches: `docs/<topic>`, `feat/<slice>`, `fix/<issue>`, or `chore/<topic>`. Keep one independently reviewable concern per PR.

A PR must name requirement IDs, the assigned slice, affected architecture decisions, test commands and results, migration impact, rollback strategy, privacy impact, and unverified behavior. Use the [PR template](.github/pull_request_template.md).

Do not duplicate canonical requirements in implementation notes. Update the owning document and link to it. Changing a technology, ownership boundary, security invariant, or side-effect protocol requires an ADR before implementation.

Use English for code, identifiers, technical docs, and agent skills. The product-owner summary and end-user interface use Vietnamese. Explain non-obvious English terms in Vietnamese-facing material.

Do not place real customer or employer data in issues, screenshots, fixtures, commits, or CI artifacts. Report a suspected exposure privately to the repository owner through an already verified channel; never paste a secret into a public issue.

There is no blanket approval to deploy from a merged PR. Promotion requires the environment approval and gates in [go-live](docs/operations/go-live.md).
