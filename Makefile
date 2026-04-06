# Makefile for BLK-REV Extractor

.PHONY: help install test clean run gui cli

PYTHON := python3
PIP := pip3

help:
	@echo "BLK-REV Extractor - Available Commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run all tests"
	@echo "  make test-unit  - Run unit tests only"
	@echo "  make run        - Run GUI application"
	@echo "  make cli        - Run CLI help"
	@echo "  make clean      - Clean temporary files"
	@echo "  make build      - Build distribution package"

install:
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed successfully"

test: test-unit test-integration
	@echo "All tests completed"

test-unit:
	$(PYTHON) test_unit.py

test-integration:
	$(PYTHON) test_integration.py

test-sample:
	$(PYTHON) test_sample.py

run:
	$(PYTHON) main.py

cli:
	$(PYTHON) cli.py --help

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf build/ dist/ *.egg-info/
	@echo "Cleanup completed"

build:
	$(PYTHON) setup.py sdist bdist_wheel
	@echo "Build completed. Check dist/ directory"

lint:
	@echo "Running code checks..."
	-flake8 backend/ frontend/ utils/ --max-line-length=100 --ignore=E501,W503
	@echo "Lint check completed"

docs:
	@echo "Documentation files:"
	@ls -la *.md

dev-setup:
	$(PYTHON) -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "  source venv/bin/activate  (Linux/Mac)"
	@echo "  venv\Scripts\activate     (Windows)"
