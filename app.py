"""Main entrypoint and composition root for the Cinema MVC REST API application."""

import logging
import logging.config
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# pyrefly: ignore [missing-import]
from src.model.database import init_db

# pyrefly: ignore [missing-import]
from src.view.filme_view import router as filme_router

# pyrefly: ignore [missing-import]
from src.view.root_view import router as root_router

# pyrefly: ignore [missing-import]
from src.view.sala_view import router as sala_router

# pyrefly: ignore [missing-import]
from src.view.sessao_view import router as sessao_router

# pyrefly: ignore [missing-import]
from src.view.tipo_ingresso_view import router as tipo_ingresso_router

_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

logging.config.dictConfig(_LOGGING_CONFIG)
_logger = logging.getLogger("cinema.app")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    _logger.info("Inicializando persistência do banco de dados SQLite...")
    init_db()
    _logger.info("Persistência SQLite pronta.")
    yield
    _logger.info("Encerrando aplicação.")


app = FastAPI(
    title="Sistema de Venda de Ingressos de Cinema (MVC)",
    description=(
        "API REST baseada em arquitetura MVC para gerenciamento de filmes, "
        "salas, sessões e tipos de ingresso com persistência em SQLite."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(filme_router)
app.include_router(sala_router)
app.include_router(tipo_ingresso_router)
app.include_router(sessao_router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
