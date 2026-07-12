# Development versus production

Development uses source mounts, FastAPI reload, DEBUG logs, development image targets, and no
automatic restarts. It prioritizes fast feedback and transparent failures.

Production uses immutable build outputs, read-only filesystems, tmpfs, dropped capabilities,
`no-new-privileges`, resource limits, INFO JSON logs, and restart policies. It prioritizes
repeatability and a smaller attack surface. Both configurations use the same API, migration,
network, and persistence model to reduce environment drift.
