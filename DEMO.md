# Five-minute employer demonstration

## Before the meeting

Run `make setup`, `make up`, and the available checks. Keep the stack running and open the
repository, browser, and terminal. Never claim a check passed unless you ran it successfully.

## 0:00-0:45 — architecture

Show the README Mermaid diagram. Explain that Nginx is the only published service, FastAPI and
PostgreSQL share an internal network, and the PostgreSQL named volume survives container replacement.

## 0:45-1:30 — container engineering

Show both Dockerfiles. Point out builder/runtime stages, pinned images, explicit non-root UIDs,
health checks, and the smaller production targets. Show `compose.prod.yml` read-only filesystems,
dropped capabilities, tmpfs, and resource limits.

## 1:30-2:15 — live application

Create, complete, and delete a task in <http://localhost:8080>. Then run:

```bash
curl -i http://localhost:8080/health
curl -s http://localhost:8080/api/v1/tasks
docker compose ps
```

Explain the browser → proxy → API → database path.

## 2:15-3:00 — state and lifecycle

Show the Alembic migration and `entrypoint.sh`. Explain database waiting, migration ordering,
`exec`, Uvicorn graceful shutdown, health-gated dependencies, and named-volume persistence.

## 3:00-3:45 — quality and security

Show GitHub Actions: backend/frontend tests, migration upgrade/downgrade, Hadolint, Docker builds,
and Trivy scans. Show JSON backend logs with `docker compose logs backend --tail=10`.

## 3:45-4:30 — operations

Show `scripts/backup.sh`, `scripts/restore.sh`, and the recovery runbook. Explain that backups are
gitignored, mode 0600, confirmation-protected on restore, and useful only after restore testing.

## 4:30-5:00 — trade-offs

Contrast source mounts and reload in development with immutable, read-only production images.
Close with one limitation—no auth/TLS/HA—and one next step such as OpenTelemetry or encrypted
scheduled backups.
