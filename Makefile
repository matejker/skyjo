default: help
TEST_PATH=./tests
MIN_COVERAGE=80

.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: requirements
requirements:
	poetry install --no-dev

.PHONY: requirements_tools
requirements_tools:
	poetry install

.PHONY: lint
lint: requirements_tools
	poetry run flake8
	poetry run black --check .
	poetry run bandit .

.PHONY: test
test: requirements_tools
	poetry run pytest -vv --color=yes $(TEST_ONLY)

.PHONY: coverage
coverage:
	poetry run pytest --cov skyjo --cov-fail-under=$(MIN_COVERAGE) $(TEST_ONLY)

.PHONY: format
format: requirements_tools
	poetry run black .

.PHONY: typecheck
typecheck: requirements_tools
	poetry run mypy tests skyjo

.PHONY: activate
activate: requirements_tools
	poetry run pre-commit install
