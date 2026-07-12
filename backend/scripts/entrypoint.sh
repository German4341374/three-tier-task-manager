#!/bin/sh
set -eu

python -m app.wait_for_db
alembic upgrade head
exec "$@"
