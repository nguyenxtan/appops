# Deployment and recovery architecture

## Selected hosting model

Use Docker images on Ubuntu 24.04 LTS with Docker Compose for local development and the single-host pilot. Caddy terminates HTTPS and routes web/API on one origin. Hosted files use private Cloudflare R2. Cloudflare is not assumed to be a VPS or the host for persistent Temporal workers.

No hostname, VM, bucket, database, or DNS record has been provisioned. These are operator-owned inputs. Do not reuse another project's production database or credentials.

## Process inventory

| Process | Network / credentials | Scaling |
| --- | --- | --- |
| web | Ingress only; no DB/provider secrets | Stateless replicas |
| api | Ingress only; scoped DB/session/storage access | Stateless replicas; bounded pool |
| dispatcher | Private; AppOps outbox and Temporal client | DB-leased consumers |
| worker-core | Private; scoped DB/connector/model access | Task-queue capacity |
| worker-documents | Document namespace and bounded file capabilities only | CPU/memory-isolated replicas |
| embeddings | Private API; no DB/connector credentials | Benchmark separately |
| PostgreSQL | Private network and persistent volume | Measured capacity, deliberate HA later |
| Temporal Server | Private; separate persistence/visibility DB accounts | Persistent pilot configuration |
| Keycloak | OIDC through ingress; separate database/account | Independent identity component |
| ClamAV | Private scanner; no application credentials | Bounded scanning |
| telemetry | Private ingestion; authenticated Grafana | Retention/disk budgets |

One pilot PostgreSQL cluster may host separate `appops`, `temporal`, `temporal_visibility`, and `keycloak` databases with separate users. This is a shared failure domain, not infrastructure isolation. AppOps migrations never alter vendor-managed schemas.

## Local versus pilot

Local development uses Compose dependencies, a Keycloak realm with synthetic identities, and a filesystem StoragePort under ignored `.data/`. Temporal's local development server is acceptable only locally. Hosted pilot uses persistent Temporal Server configuration and authenticated/private access; never deploy `temporal server start-dev` as production durability.

R2 behavior must be tested in an approved staging bucket. Filesystem tests do not prove R2 compatibility. Use only the documented adapter subset: put/get/head/delete/list, bounded metadata, and temporary capabilities. Do not assume all AWS S3 features exist in R2.

## Capacity assumption

Initial pilot evaluation budget: **8 vCPU, 32 GiB RAM, 200 GiB SSD** for the combined parser, model, databases, workflow, and telemetry. This is a test starting point, not a minimum, guarantee, or purchasing instruction. Measure before production spend; local development can run fewer services.

Initial admission: two document jobs, four chat generations, two diagnostic queries per application, bounded queues, and explicit AI budgets. Queue/reject excess work. Isolate parsing/inference pressure from the control plane.

## Network and secrets

Only HTTPS ingress is public. Keep DB, Temporal gRPC, inference, and telemetry private. Use authenticated workload connections and mTLS across host/network trust boundaries. A Docker network is not a complete authorization boundary. Restrict document-worker egress to storage/Temporal/scanning. Never mount the Docker socket into an agent.

Use non-root containers, read-only filesystems where feasible, resource limits, dropped capabilities, and per-process secrets. Backup credentials are separate. Pin image digests and source commits. Scan images/dependencies before promotion.

## Release procedure

Build/test immutable images; review migrations and workflow history compatibility; check backup freshness; apply expand migrations through an approved release job; roll out compatible workers/API/web; run authenticated smoke tests; inspect queues; enable only approved capabilities.

Migrations never run from API startup. Workflow upgrades require replay tests and old-worker retention until migration is safe. Roll back compatible images or use a forward fix; schema downgrade is not automatically safe. Keep communication and mutation disabled during initial deployment.

## Backups and recovery

Initial pilot objectives: **RPO 15 minutes, RTO 4 hours**, unproven until restore testing. Use pgBackRest base backups plus continuous WAL archiving to approved private backup storage. Object durability is not a backup: retain checksummed manifests and a separately controlled backup copy or verified protection against deletion.

Back up AppOps, Temporal persistence/visibility, and Keycloak. Keep encryption/recovery keys separately. Restore to isolation with outbound actions paused; reconcile Jira and unknown deliveries before resuming. Never blindly replay an outbox after point-in-time restore.

Test API-host loss, worker restart, database restore, object loss, provider outage, and workflow compatibility before go-live. Do not claim external messages/operations can all be rolled back.

## Growth path

Separate DB, Temporal, inference, and telemetry into independent resource/failure domains; then add API/worker replicas. Introduce orchestration/HA only with operational ownership and failure tests. Kubernetes, dedicated vector storage, or a broker requires measured need, an ADR, and a migration plan.
