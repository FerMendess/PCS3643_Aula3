"""Root and API status endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["Status"])


@router.get("/", summary="Status da API e informações gerais")
def root() -> dict[str, str]:
    return {
        "status": "online",
        "arquitetura": "MVC (Model-View-Controller)",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }
