# Agent Guidelines

- Use English for code, configuration, documentation, and commits.
- Never commit `.env`, database dumps, private keys, tokens, or personal data.
- Keep backend and frontend containers non-root and preserve the internal network boundary.
- Pin important dependencies and images; explain any intentional exceptions.
- Add migrations for schema changes and test both upgrade and downgrade paths.
- Keep structured logging fields stable and avoid logging task descriptions or secrets.
- Run `make lint` and `make test`; run Compose health checks when Docker is available.
- Update backup, restore, security, and architecture documentation when behavior changes.
