# ADR 0001: Four containers implement three logical tiers

- Status: Accepted
- Date: 2026-07-13

The presentation tier is split into an Nginx edge proxy and a static frontend container. This
keeps ingress policy independent from frontend assets while preserving the classic presentation,
application, and data tiers. The extra container costs memory but makes routing and trust
boundaries visible in a portfolio demonstration.
