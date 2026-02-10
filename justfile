default: lint test

install:
    uv sync

lint: lint-ruff lint-mypy

lint-ruff:
    uv run ruff check .

lint-mypy:
    uv run mypy

test:
    uv run pytest

test-cov:
    uv run pytest --cov=result --cov-report=term-missing

build:
    uv build
