"""Domain model and Pydantic schemas for Filme."""

from typing import override

from pydantic import BaseModel, ConfigDict, Field


class Filme:
    def __init__(
        self,
        nome: str | None = None,
        data_estreia: str | None = None,
        data_saida: str | None = None,
        duracao: int | None = None,
        codigo: int | None = None,
    ) -> None:
        self.codigo = codigo
        self.nome = nome
        self.data_estreia = data_estreia
        self.data_saida = data_saida
        self.duracao = duracao

    __hash__ = None
    """Compare equality based on attributes."""

    @override
    def __eq__(self, other: object) -> bool:
        """Verify equality between Filme instances."""
        if not isinstance(other, Filme):
            return False
        return (
            self.codigo == other.codigo
            and self.nome == other.nome
            and self.data_estreia == other.data_estreia
            and self.data_saida == other.data_saida
            and self.duracao == other.duracao
        )


class FilmeCreate(BaseModel):
    nome: str = Field(..., min_length=1)
    data_estreia: str
    data_saida: str
    duracao: int = Field(..., gt=0)


class FilmeUpdate(BaseModel):
    nome: str | None = None
    data_estreia: str | None = None
    data_saida: str | None = None
    duracao: int | None = None


class FilmeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    codigo: int
    nome: str
    data_estreia: str
    data_saida: str
    duracao: int
