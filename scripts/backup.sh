#!/usr/bin/env bash
set -Eeuo pipefail

if [[ ! -f .env ]]; then
  echo "Missing .env. Copy .env.example and replace placeholder values." >&2
  exit 1
fi

mkdir -p backups
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
output="backups/tasks-${timestamp}.sql.gz"
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB"' | gzip > "${output}"
chmod 600 "${output}"
echo "Backup written to ${output}"
