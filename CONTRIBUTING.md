# Contributing

1. Create a focused branch from `main`.
2. Run `make setup` on Linux or WSL2.
3. Add tests and an Alembic migration for schema changes.
4. Run `make lint` and `make test`.
5. Run `make up` and verify all container health checks when Docker is available.
6. Describe risk, rollback, and validation in the pull request.

Use imperative English commit messages. Never commit secrets, `.env`, backups, or generated artifacts.
