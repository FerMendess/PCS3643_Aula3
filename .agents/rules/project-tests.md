---
trigger: model_decision
description: Use when writing or editing tests - test layout, execution commands, and isolation rules.
globs: tests/**/*.py
---

# Tests

| File | Scope |
| --- | --- |
| `tests/model/test_model.py` | Unit tests for domain models and Pydantic schemas (validations, serialization). |
| `tests/controller/test_controller.py` | Unit tests for controllers, business logic, schedule conflicts, and atomic ticket purchasing. |
| `tests/view/test_view.py` | Integration tests for FastAPI endpoints using `TestClient` (CRUD, status codes, payload contracts). |

## Execution Commands
- **Run all tests**: `python -m pytest`
- **Run with coverage**: `python -m pytest --cov=src`
- **Run single test file**: `python -m pytest tests/controller/test_controller.py`

## Test Isolation & Fixtures
- Tests isolate database side-effects by reinitializing SQLite schema or state in `setUp` / `tearDown` methods to guarantee isolated and reproducible executions.
- Do not leave residual mock data in production database (`cinema.db`).