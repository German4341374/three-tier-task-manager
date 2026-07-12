# ADR 0002: Run migrations before the API process

- Status: Accepted
- Date: 2026-07-13

The entrypoint waits for PostgreSQL, applies Alembic migrations, and then replaces itself with
Uvicorn. This is simple and deterministic for one Compose backend. Multiple replicas would need
a separate migration job or deployment lock to prevent concurrent schema changes.
