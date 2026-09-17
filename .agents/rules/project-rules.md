---
trigger: always_on
description: Project facts. Use for tech stack, repository layout, virtualenv location, and deferred work (TODO.md).
---

# Project Core

## Repository & Tech Stack
- **Project**: PCS3643 - Aula 3 (Sistema de Venda de Ingressos de Cinema MVC)
- **Tech Stack**: Python 3.10+ (tested on Python 3.14), FastAPI, Uvicorn, SQLite, Pydantic v2, Pytest
- **Virtualenv**: `.venv` at the repository root
- **Entrypoints**: `app.py` (FastAPI web server & OpenAPI docs), `cinema.py` (facade)
- **Code Directory**: `src/` (`model/`, `controller/`, `view/`)
- **Tests Directory**: `tests/` (`test_model.py`, `test_controller.py`, `test_view.py`)

## Deferred work (TODO.md)
When you or the user defer something for later, record it in `TODO.md` at the repository root:
- Add a bullet with a short description and context (file, area, or reason deferred).
- Update `TODO.md` in the same turn you agree to defer.
- If `TODO.md` does not exist yet, create it with a short heading and the first item.
