# BRICK 2 Makefile

.PHONY: help install install-dev test test-unit test-integration test-performance lint format type-check security-check clean docker-build docker-run docker-dev setup-db migrate upgrade-db

# Default target
help:
	@echo "BRICK 2 - Available Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  install          Install production dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo "  setup-db         Set up database"
	@echo ""
	@echo "Database:"
	@echo "  migrate          Create new migration"
	@echo "  upgrade-db       Run database migrations"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run all tests"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-performance Run performance tests"
	@echo "  test-coverage    Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint             Run linting (flake8)"
	@echo "  format           Format code (black, isort)"
	@echo "  type-check       Run type checking (mypy)"
	@echo "  security-check   Run security checks (bandit, safety)"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build     Build Docker image"
	@echo "  docker-run       Run Docker container"
	@echo "  docker-dev       Run development environment"
	@echo ""
	@echo "Utilities:"
	@echo "  clean            Clean up temporary files"
	@echo "  run              Run the application"
	@echo "  run-dev          Run the application in development mode"

# Installation
install:
	poetry install --no-dev

install-dev:
	poetry install

# Database
setup-db:
	poetry run alembic upgrade head

migrate:
	@read -p "Enter migration message: " msg; \
	poetry run alembic revision --autogenerate -m "$$msg"

upgrade-db:
	poetry run alembic upgrade head

# Testing
test:
	poetry run pytest

test-unit:
	poetry run pytest -m "unit"

test-integration:
	poetry run pytest -m "integration"

test-performance:
	poetry run pytest -m "performance"
	poetry run python tests/performance/database_performance.py
	poetry run python tests/performance/memory_test.py

test-coverage:
	poetry run pytest --cov=src/brick2 --cov-report=html --cov-report=term-missing

# Code Quality
lint:
	poetry run flake8 src/ tests/ --max-line-length=100 --exclude=__pycache__
	poetry run black --check src/ tests/
	poetry run isort --check-only src/ tests/

format:
	poetry run black src/ tests/
	poetry run isort src/ tests/

type-check:
	poetry run mypy src/brick2 --ignore-missing-imports

security-check:
	poetry run bandit -r src/brick2
	poetry run safety check

# Docker
docker-build:
	docker build -t brick2:latest .

docker-run:
	docker-compose up -d

docker-dev:
	docker-compose -f docker-compose.dev.yml up -d

# Application
run:
	poetry run python -m brick2

run-dev:
	poetry run uvicorn brick2.main:app --reload --host 0.0.0.0 --port 8000

# Utilities
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf bandit-report.json
	rm -rf safety-report.json
	rm -rf database-performance-report.json
	rm -rf memory-profile.txt
	rm -rf memory-leak-profile.txt

# CI/CD helpers
ci-test:
	poetry run pytest --cov=src/brick2 --cov-report=xml --cov-report=html --junitxml=test-results.xml

ci-lint:
	poetry run flake8 src/ tests/ --max-line-length=100 --exclude=__pycache__ --format=junit-xml --output-file=flake8-results.xml
	poetry run black --check src/ tests/
	poetry run isort --check-only src/ tests/

ci-security:
	poetry run bandit -r src/brick2 -f json -o bandit-report.json
	poetry run safety check --json --output safety-report.json

# Development helpers
dev-setup: install-dev setup-db
	@echo "Development environment set up successfully!"

quick-test:
	poetry run python simple_service_test.py

load-test:
	poetry run locust -f tests/performance/locustfile.py --headless -u 50 -r 5 -t 30s

benchmark:
	poetry run pytest tests/performance/benchmark_tests.py --benchmark-json=benchmark-results.json
