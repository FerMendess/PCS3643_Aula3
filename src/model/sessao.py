"""Domain model and Pydantic schemas for Sessao and Ingressos."""

from typing import override

from pydantic import BaseModel, ConfigDict, Field

from model.filme import Filme
from model.sala import Sala


class Sessao:
    def __init__(
        self,
        sala: Sala | None = None,
        filme: Filme | None = None,
        data: str | None = None,
        hora_inicio: int | None = None,
        codigo: int | None = None,
    ) -> None:
        self.codigo = codigo
        self.sala = sala
        self.filme = filme
        self.data = data
        self.hora_inicio = hora_inicio
        self.assentos: dict[int, int] = {}

    __hash__ = None  # type: ignore[assignment]

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sessao):
            return False
        return (
            self.codigo == other.codigo
            and getattr(self.sala, "numero", None)
            == getattr(other.sala, "numero", None)
            and getattr(self.filme, "codigo", None)
            == getattr(other.filme, "codigo", None)
            and self.data == other.data
            and self.hora_inicio == other.hora_inicio
        )


class SessaoCreate(BaseModel):
    numero_sala: int = Field(..., gt=0)
    codigo_filme: int = Field(..., gt=0)
    data: str
    hora_inicio: int = Field(..., ge=0, le=23)


class SessaoUpdate(BaseModel):
    numero_sala: int | None = Field(default=None, gt=0)
    codigo_filme: int | None = Field(default=None, gt=0)
    data: str | None = None
    hora_inicio: int | None = Field(default=None, ge=0, le=23)


class SessaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codigo: int
    numero_sala: int
    codigo_filme: int
    data: str
    hora_inicio: int
    assentos: dict[int, int] = Field(default_factory=dict)


class CompraIngressoRequest(BaseModel):
    assentos: list[int] = Field(..., min_length=1)
    tipos_ingresso: list[int] = Field(..., min_length=1)


class CompraIngressoResponse(BaseModel):
    codigo_sessao: int
    assentos_comprados: list[int]
    total: float | int


class SessaoDisponivelResponse(BaseModel):
    codigo: int
    filme_nome: str
    numero_sala: int
    tipo_sala: str
    hora_inicio: int
    valor: int
    descricao: str
