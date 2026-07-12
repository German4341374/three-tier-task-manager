# syntax=docker/dockerfile:1.7
FROM node:22.14.0-alpine3.21 AS builder
WORKDIR /build
RUN chown node:node /build
COPY --chown=node:node package.json package-lock.json ./
COPY --chown=node:node scripts ./scripts
COPY --chown=node:node src ./src
USER node
RUN npm ci --ignore-scripts && npm run build

FROM nginxinc/nginx-unprivileged:1.30.3-alpine3.23 AS production
COPY --from=builder --chown=101:101 /build/dist /usr/share/nginx/html
COPY --chown=101:101 nginx.conf /etc/nginx/conf.d/default.conf
USER 101:101
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O - http://127.0.0.1:8080/health || exit 1

FROM node:22.14.0-alpine3.21 AS development
WORKDIR /app
COPY --chown=node:node package.json package-lock.json ./
COPY --chown=node:node scripts ./scripts
COPY --chown=node:node src ./src
USER node
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O - http://127.0.0.1:8080/ || exit 1
CMD ["npm", "run", "dev"]
