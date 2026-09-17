"""Domain model and Pydantic schemas for Sala."""

from typing import Literal, override

from pydantic import BaseModel, ConfigDict, Field


class Sala:
    def __init__(
        self,
        numero: int | None = None,
        capacidade: int | None = None,
        tipo: str | None = None,
    ) -> None:
        self.numero = numero
        self.capacidade = capacidade
        self.tipo = tipo

    __hash__ = None  # type: ignore[assignment]

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sala):
            return False
        return (
            self.numero == other.numero
            and self.capacidade == other.capacidade
            and self.tipo == other.tipo
        )


class SalaCreate(BaseModel):
    numero: int = Field(..., gt=0)
    capacidade: int = Field(..., gt=0)
    tipo: Literal["2D", "3D"]


class SalaUpdate(BaseModel):
    capacidade: int | None = Field(default=None, gt=0)
    tipo: Literal["2D", "3D"] | None = None


class SalaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    numero: int
    capacidade: int
    tipo: str
