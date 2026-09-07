# Makefile for Smart Farmer Assistant

.PHONY: help install test run seed count-loc clean docker-build

PYTHON = python
PIP = pip

help:
	@echo "Smart Farmer Assistant Commands:"
	@echo "  make install     Install requirements and locked dependencies"
	@echo "  make run         Run Flask development application server"
	@echo "  make seed        Initialize database and seed sample data"
	@echo "  make test        Run test suite with coverage report"
	@echo "  make count-loc   Calculate total production lines of code"
	@echo "  make clean       Remove temporary files and cache"

install:
	$(PIP) install -r requirements-lock.txt

run:
	$(PYTHON) run.py

seed:
	$(PYTHON) database/seeds/seed.py

test:
	pytest --cov=app --cov=ml --cov-report=term-missing

count-loc:
	$(PYTHON) scripts/count_prod_loc.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
