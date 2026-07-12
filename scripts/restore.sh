#!/usr/bin/env bash
set -Eeuo pipefail

backup="${1:-}"
if [[ -z "${backup}" || ! -f "${backup}" ]]; then
  echo "Usage: $0 backups/tasks-TIMESTAMP.sql.gz" >&2
  exit 1
fi

read -r -p "Restore ${backup} and overwrite current task data? Type RESTORE: " confirmation
[[ "${confirmation}" == "RESTORE" ]] || { echo "Restore cancelled."; exit 1; }
gunzip -c "${backup}" | docker compose exec -T db sh -c \
  'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
echo "Restore completed from ${backup}"
