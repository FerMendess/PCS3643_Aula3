"""Main entrypoint for the Cinema MVC REST API application."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from model.database import init_db
from view.filme_view import router as filme_router
from view.sala_view import router as sala_router
from view.sessao_view import router as sessao_router
from view.tipo_ingresso_view import router as tipo_ingresso_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    init_db()
    yield


app = FastAPI(
    title="Sistema de Venda de Ingressos de Cinema (MVC)",
    description=(
        "API REST baseada em arquitetura MVC para gerenciamento de filmes, "
        "salas, sessões e tipos de ingresso com persistência em SQLite."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(filme_router)
app.include_router(sala_router)
app.include_router(tipo_ingresso_router)
app.include_router(sessao_router)


@app.get("/", summary="Status da API e informações gerais")
def root() -> dict[str, str]:
    return {
        "status": "online",
        "arquitetura": "MVC (Model-View-Controller)",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
