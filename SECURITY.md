# Security Policy

Report vulnerabilities through GitHub private security advisories rather than public issues.
Remove credentials, task data, hostnames, and addresses from reports.

The application containers run as non-root users, the database and backend use an internal
network, and production overrides remove Linux capabilities and enable read-only filesystems
where practical. Only Nginx publishes a host port. Docker socket access is never mounted.

`.env` and backup files are ignored. Rotate a value immediately if it is exposed; deleting it
from a later commit does not remove it from history. This demonstration has no authentication
or TLS termination and must not be exposed directly to the internet.
