# Security policy

AppOps currently contains a documentation foundation, not a supported production release. Runtime security controls described in the architecture are requirements to implement and test.

This is a public repository. Do not submit vulnerabilities containing real credentials, private manuals, personal information, ticket bodies, or production logs through public issues. Contact the repository owner through an independently verified private channel. A private reporting endpoint has not been established in this repository.

If a secret is exposed: revoke or rotate it first, preserve a sanitized incident record, remove it from active code and artifacts, and assess history cleanup with the owner. Deleting a file alone does not revoke a leaked credential.

See [security architecture](docs/architecture/security.md) for threat boundaries and [operational runbooks](docs/operations/runbooks.md) for incident handling.
