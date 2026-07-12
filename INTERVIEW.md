# Interview questions and answers

## 1. Why call it three-tier when there are four containers?
The logical tiers are presentation, application, and data. Nginx and the static frontend split
presentation responsibilities into ingress policy and assets.

## 2. Why use multi-stage builds?
Build tools stay out of production images, reducing size, dependency count, and attack surface.

## 3. How do containers run without root?
The backend uses UID 10001, unprivileged Nginx uses UID 101, and Alpine PostgreSQL uses UID 70.
Ports are above 1024 and writable locations are explicit.

## 4. Why is PostgreSQL not published to the host?
Only the API needs database access. An internal Docker network removes an unnecessary ingress path.

## 5. What do health checks provide?
They identify process and dependency readiness and gate Compose startup. They do not replace logs,
metrics, traces, or external user-path probes.

## 6. What is the difference between liveness and readiness?
Liveness proves the API process responds. Readiness also executes `SELECT 1`, proving database access.

## 7. Why use a named volume?
It separates database state from container lifecycle and gives Compose a stable persistence object.

## 8. How are schema changes managed?
Alembic versions every change. CI tests upgrade, downgrade, and upgrade again against PostgreSQL.

## 9. Is running migrations at startup always safe?
It is acceptable for one backend replica. Multiple replicas need a dedicated migration job or lock.

## 10. How are environment variables validated?
Compose requires database variables during interpolation, and Pydantic validates types and allowed
values before the application starts.

## 11. Why use structured JSON logs?
Stable fields such as request ID, status, and duration are machine-searchable without fragile parsing.

## 12. How does graceful shutdown work?
The entrypoint uses `exec`, so signals reach Uvicorn. Uvicorn receives a 15-second graceful timeout,
and Compose allows a 20-second stop grace period.

## 13. Why use Nginx as a reverse proxy?
It centralizes ingress, routing, request limits, headers, timeouts, and frontend/API composition.

## 14. How does development differ from production?
Development mounts sources and enables reload/debug logs. Production uses immutable stages,
read-only filesystems, capability dropping, tmpfs, limits, and restart policies.

## 15. What does Hadolint check?
It flags Dockerfile correctness, maintainability, shell, package, and image-building anti-patterns.

## 16. What does Trivy check?
CI scans the repository and built images for high or critical known vulnerabilities.

## 17. Why pin dependencies?
Pins make builds reviewable and repeatable. They require deliberate update automation to avoid staleness.

## 18. How are backups made?
The script streams `pg_dump` through gzip into a timestamped mode-0600 file without embedding credentials.

## 19. How is restore risk reduced?
The script validates its input, requires typing `RESTORE`, uses `ON_ERROR_STOP`, and has a runbook.

## 20. Why are backups excluded from Git?
Dumps contain application data and grow quickly. They belong in protected backup storage, not source control.

## 21. What does least privilege mean here?
No Docker socket, explicit non-root users, no database host port, internal networking, dropped capabilities,
and read-only production filesystems.

## 22. Why no authentication?
The goal is infrastructure demonstration. The limitation is explicit; internet exposure would require auth,
authorization, TLS, CSRF analysis, and rate-policy review.

## 23. How would you scale it?
Use managed PostgreSQL, external migrations, multiple stateless API replicas, shared ingress, metrics,
and an orchestrator with rolling health-aware deployments.

## 24. What would you monitor?
Request rate/errors/latency, container restarts, health failures, DB connections/storage, migration status,
backup age, and restore-test results.

## 25. What is the biggest Compose limitation?
It is a single-host control plane without high availability, sophisticated rollout, or self-healing across nodes.
