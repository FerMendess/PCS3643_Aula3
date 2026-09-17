---
trigger: model_decision
description: Use when editing Python files - MVC layout, layer boundaries, and persistence rules.
globs: src/**/*.py, app.py, cinema.py
---

# Architecture (MVC)

| Layer | Path | Responsibilities & Key Modules |
| --- | --- | --- |
| **Entrypoint** | `app.py` | FastAPI application instance, lifespan (`init_db()`), router registration (`include_router`), root status endpoint. |
| **Facade** | `cinema.py` | High-level orchestration facade coordinating controllers (`FilmeController`, `SalaController`, `SessaoController`, `TipoIngressoController`). |
| **View** | `src/view/` | FastAPI REST routers (`filme_view.py`, `sala_view.py`, `sessao_view.py`, `tipo_ingresso_view.py`). Handles HTTP status codes, validation error responses, and endpoints. |
| **Controller** | `src/controller/` | Business rules and validation (`filme_controller.py`, `sala_controller.py`, `sessao_controller.py`, `tipo_ingresso_controller.py`, `cadastraController.py`, `buscaController.py`, `helpers/validar_data.py`). Handles seat reservation atomic checks, scheduling overlap prevention. |
| **Model** | `src/model/` | Domain entities and SQLite persistence: `database.py` (connection management, table creation, query execution), `filme.py`, `sala.py`, `sessao.py`, `tipo_ingresso.py` (Pydantic schemas & entity classes). |

## Invariants & Layer Boundaries
- **Dependency Direction**: View -> Controller -> Model -> Database.
- **View isolation**: Controllers and Models MUST NEVER import Views or FastAPI routing constructs.
- **Model isolation**: Models encapsulate schema definitions and database mapping; they MUST NEVER import Controllers or Views.
- **Persistence**: Relational SQLite database stored in `cinema.db`, managed via `src/model/database.py`.