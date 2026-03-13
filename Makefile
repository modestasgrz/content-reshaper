## Makefile for Content Reshaper
#
# Tools required: uv, ruff, mypy, pytest

SHELL := /bin/bash

.PHONY: help check fix test

## Show help for each make target
help:
	@echo "Available commands:"
	@echo "  make check  - Run linting (ruff) and type checking (mypy)"
	@echo "  make fix    - Automatically fix style issues with ruff"
	@echo "  make test   - Run the pytest test suite"

## Run code quality checks: ruff and mypy
check:
	@echo "Running ruff linter..."
	uv run ruff check .
	@echo "Running mypy type checker..."
	uv run mypy .

## Automatically fix import ordering and formatting issues using ruff
fix:
	@echo "Fixing code style issues with ruff..."
	uv run ruff check --fix .

## Run the pytest test suite
test:
	@echo "Running tests..."
	uv run pytest tests/ -s -vv
