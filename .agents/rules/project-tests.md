---
trigger: model_decision
description: Use when writing or editing tests - test layout, execution commands, and isolation rules.
globs: tests/**/*.py
---

# Tests

| Directory / Files | Scope |
| --- | --- |
| `tests/model/test_*.py` | Unit tests for domain models and Pydantic schemas per entity (`filme`, `sala`, `sessao`, `tipo_ingresso`). |
| `tests/controller/test_*.py` | Unit tests for controllers, business rules (US01-US06), schedule conflicts, and atomic ticket purchasing. |
| `tests/view/test_*.py` | Integration tests for FastAPI endpoints using `TestClient` (`root`, `filme`, `sala`, `sessao`, `tipo_ingresso`). |

## Execution Commands
- **Run all tests**: `python -m pytest`
- **Run with coverage**: `python -m pytest --cov=src`
- **Run single test file**: `python -m pytest tests/controller/test_sessao_controller.py`

## Test Isolation & Fixtures
- Tests isolate database side-effects by reinitializing SQLite schema or state in `setUp` / `tearDown` methods to guarantee isolated and reproducible executions.
- Do not leave residual mock data in production database (`cinema.db`).