# Database recovery runbook

1. Stop writes: `docker compose stop proxy backend`.
2. Copy the selected dump to a safe location and verify it is non-empty with `gzip -t FILE`.
3. Start PostgreSQL: `docker compose up -d db` and wait for healthy status.
4. Run `make restore FILE=backups/FILE.sql.gz` and type `RESTORE`.
5. Start the backend and proxy: `docker compose up -d backend frontend proxy`.
6. Verify `/health`, list tasks, and inspect backend logs for errors.
7. Record the dump name, recovery time, data-loss window, and operator.

For corrupted volumes, restore into a new named volume first. Never delete the original volume
until application verification and backup retention requirements are satisfied.
