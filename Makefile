SHELL := /bin/bash
PYTHON ?= python3
VENV := .venv
PIP := $(VENV)/bin/pip

.PHONY: setup lint test up prod down logs migrate backup restore clean

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --disable-pip-version-check -e './backend[dev]'
	cd frontend && npm ci
	@test -f .env || cp .env.example .env

lint:
	$(VENV)/bin/ruff check backend
	cd frontend && npm run lint
	docker run --rm -i hadolint/hadolint:v2.12.0-alpine < backend/Dockerfile
	docker run --rm -i hadolint/hadolint:v2.12.0-alpine < frontend/Dockerfile

test:
	APP_DATABASE_URL=postgresql+psycopg://test:test@localhost/test $(VENV)/bin/pytest backend/tests
	cd frontend && npm test

up:
	docker compose -f compose.yml -f compose.dev.yml up --build -d

prod:
	docker compose -f compose.yml -f compose.prod.yml up --build -d

down:
	docker compose -f compose.yml -f compose.dev.yml down

logs:
	docker compose logs -f --tail=100

migrate:
	docker compose exec backend alembic upgrade head

backup:
	bash scripts/backup.sh

restore:
	bash scripts/restore.sh $(FILE)

clean:
	docker compose -f compose.yml -f compose.dev.yml down --volumes --remove-orphans
	rm -rf $(VENV) frontend/node_modules frontend/dist .pytest_cache .ruff_cache htmlcov .coverage
