"""Domain model and Pydantic schemas for TipoIngresso."""

from typing import override

from pydantic import BaseModel, ConfigDict, Field


class TipoIngresso:
    def __init__(self, tipo: str | None = None, valor: int | None = None) -> None:
        self.tipo = tipo
        self.valor = valor

    __hash__ = None  # type: ignore[assignment]
    """Compare equality based on attributes."""

    @override
    def __eq__(self, other: object) -> bool:
        """Verify equality between TipoIngresso instances."""
        if not isinstance(other, TipoIngresso):
            return False
        return self.tipo == other.tipo and self.valor == other.valor


class TipoIngressoCreate(BaseModel):
    tipo: str = Field(..., min_length=1)
    valor: int = Field(..., gt=0)


class TipoIngressoUpdate(BaseModel):
    valor: int = Field(..., gt=0)


class TipoIngressoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tipo: str
    valor: int
