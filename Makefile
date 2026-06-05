.PHONY: help setup run test smoke-test auth-test coverage docs clean

PYTHON ?= python

help:
	@echo "Доступные команды:"
	@echo "  make setup       - установить зависимости для разработки"
	@echo "  make run         - запустить HR-приложение"
	@echo "  make test        - запустить все тесты"
	@echo "  make smoke-test  - запустить smoke-тесты"
	@echo "  make auth-test   - запустить unit-тесты авторизации"
	@echo "  make coverage    - запустить тесты с отчётом покрытия"
	@echo "  make clean       - удалить временные файлы"
	@echo "  make docs        - собрать проектную документацию"

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

coverage:
	./scripts/coverage.sh

clean:
	rm -rf .pytest_cache htmlcov .coverage
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
docs:
	./scripts/build-docs.sh