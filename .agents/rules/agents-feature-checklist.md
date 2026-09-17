---
trigger: model_decision
description: Use after code changes - quality gate and verification matrix.
globs: src/**/*.py, tests/**/*.py, app.py, cinema.py
---

# Feature Change Checklist

## Post-change Quality Gate
Run the following verification steps before finalizing changes:
1. **Linting & Formatting**: `python -m ruff check src tests app.py cinema.py`
2. **Type Checking**: `python -m mypy`
3. **Automated Tests**: `python -m pytest` (all tests must pass)
4. **Adversarial Review**: Invoke `@adversarial-review` on any diff before delivery.

## Decision Matrix
When changing code, evaluate downstream impacts:
| Changed Area | Action / Verification |
| --- | --- |
| `src/model/` (models, database) | Run `pytest tests/test_model.py`; verify migrations and table schemas in `src/model/database.py`. |
| `src/controller/` (business rules) | Run `pytest tests/test_controller.py`; verify edge cases, schedule clashes, and ticket sales. |
| `src/view/` or `app.py` (endpoints) | Run `pytest tests/test_view.py`; ensure HTTP response codes and Pydantic schemas match REST contract. |
| Configuration / dependencies | Check `pyproject.toml` and `requirements.txt`. |
