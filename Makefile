.PHONY: help setup run test smoke-test auth-test integration-test coverage docs build-lib install-lib-local check clean docker-build docker-check compose-check

PYTHON ?= python

help:
	@echo "Доступные команды:"
	@echo "  make setup             - установить зависимости для разработки"
	@echo "  make run               - запустить HR-приложение"
	@echo "  make test              - запустить все тесты"
	@echo "  make smoke-test        - запустить smoke-тесты"
	@echo "  make auth-test         - запустить unit-тесты авторизации"
	@echo "  make integration-test  - запустить integration-тесты"
	@echo "  make coverage          - запустить тесты с отчётом покрытия"
	@echo "  make docs              - собрать проектную документацию"
	@echo "  make build-lib         - собрать переиспользуемый core-пакет"
	@echo "  make install-lib-local - установить пакет локально в editable-режиме"
	@echo "  make check             - выполнить основную проверку проекта"
	@echo "  make docker-build      - собрать Docker-образ для проверки"
	@echo "  make docker-check      - запустить make check внутри Docker"
	@echo "  make compose-check     - запустить проверку через docker compose"
	@echo "  make clean             - удалить временные файлы"

setup:
	./scripts/setup.sh

run:
	./scripts/run.sh

test:
	./scripts/test.sh

smoke-test:
	$(PYTHON) -m pytest tests/smoke -v

auth-test:
	$(PYTHON) -m pytest tests/unit/test_auth.py -v

integration-test:
	$(PYTHON) -m pytest tests/integration -v

coverage:
	./scripts/coverage.sh

docs:
	./scripts/build-docs.sh

build-lib:
	./scripts/build-lib.sh

install-lib-local:
	./scripts/install-lib-local.sh

check: test docs

docker-build:
	docker build -t hr-system-checks:local .

docker-check:
	docker run --rm hr-system-checks:local

compose-check:
	docker compose -f infra/compose.yaml up --build --abort-on-container-exit --exit-code-from checks

clean:
	rm -rf .pytest_cache htmlcov .coverage site dist build
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +