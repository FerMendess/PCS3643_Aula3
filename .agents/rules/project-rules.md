---
trigger: always_on
description: Project facts. Use for tech stack, repository layout, virtualenv location, and deferred work (TODO.md).
---

# Project Core

## Repository & Tech Stack
- **Tech Stack**: Python 3.14, FastAPI, Uvicorn, SQLite, Pydantic v2, Pytest
- **Virtualenv**: `.venv` at the repository root
- **Entrypoints**: `app.py` (FastAPI web server & OpenAPI docs), `cinema.py` (facade)
- **Code Directory**: `src/` (`model/`, `controller/`, `view/`)
- **Tests Directory**: `tests/` (`controller/test_controller.py`, `model/test_model.py`, `view/test_view.py`)