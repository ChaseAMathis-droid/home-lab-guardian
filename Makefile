.PHONY: help setup format lint test test-cov run clean

help:
	@echo "Home Lab Guardian - Makefile Commands"
	@echo "======================================"
	@echo "setup        - Create venv and install dependencies"
	@echo "format       - Format code with black and isort"
	@echo "lint         - Run linters (black, isort, flake8, mypy)"
	@echo "test         - Run tests"
	@echo "test-cov     - Run tests with coverage report"
	@echo "run          - Run the agent"
	@echo "docker-build - Build Docker image"
	@echo "docker-up    - Start Docker Compose services"
	@echo "docker-down  - Stop Docker Compose services"
	@echo "clean        - Remove generated files"

setup:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -e ".[dev]"
	@echo "\n✅ Setup complete! Activate with: source venv/bin/activate"

format:
	black src/ tests/
	isort src/ tests/

lint:
	black --check src/ tests/
	isort --check src/ tests/
	flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503
	mypy src/

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=hlg --cov-report=term-missing --cov-report=html
	@echo "\n📊 Coverage report generated in htmlcov/index.html"

run:
	hlg run

docker-build:
	docker build -t home-lab-guardian:latest .

docker-up:
	docker-compose up -d
	@echo "\n✅ Services started. View logs with: docker-compose logs -f agent"

docker-down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/ .coverage htmlcov/ dist/ build/
