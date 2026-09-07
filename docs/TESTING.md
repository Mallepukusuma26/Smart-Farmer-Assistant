# Smart Farmer Assistant — Automated Testing Guide

## Test Suite Architecture

The project includes unit, integration, ML inference, and security test suites located in `tests/`:

- `tests/unit/test_models.py`: Database entities, password hashing, to_dict serialization tests.
- `tests/unit/test_services.py`: Service logic for Auth, Soil Analysis, Fertilizer Dosage, and Expenses.
- `tests/unit/test_ml_pipeline.py`: Inference tests for CropPredictor, YieldPredictor, and ProfitPredictor.
- `tests/integration/test_auth_routes.py`: Login, logout, registration HTTP route tests.
- `tests/security/test_security.py`: RBAC 403 authorization enforcement tests.

## Running Tests

Execute the full test suite using `pytest`:
```bash
pytest
```
To run tests with detailed verbosity and coverage:
```bash
pytest -v --cov=app --cov=ml
```
