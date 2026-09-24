"""Domain model and Pydantic schemas for Sessao and Ingressos."""

from collections.abc import Mapping
from pathlib import Path
from typing import override

from pydantic import BaseModel, ConfigDict, Field

from src.model.database import execute_write
from src.model.filme import Filme
from src.model.sala import Sala


class AssentosDict(dict[int, int]):
    """Dictionary representing seats that synchronizes updates with database persistence."""

    def __init__(
        self,
        sessao_codigo: int | None = None,
        db_path: str | Path | None = None,
        initial: Mapping[int, int] | None = None,
    ) -> None:
        super().__init__(initial or {})
        self._sessao_codigo = sessao_codigo
        self._db_path = db_path

    @override
    def __setitem__(self, seat: int, val: int) -> None:
        super().__setitem__(seat, val)
        if self._sessao_codigo is not None:
            execute_write(
                "UPDATE assentos SET ocupado = ? WHERE codigo_sessao = ? AND numero_assento = ?;",
                (val, self._sessao_codigo, seat),
                db_path=self._db_path,
            )


class Sessao:
    def __init__(
        self,
        sala: Sala | None = None,
        filme: Filme | None = None,
        data: str | None = None,
        hora_inicio: int | None = None,
        codigo: int | None = None,
    ) -> None:
        self._codigo = codigo
        self._db_path: str | Path | None = None
        self.sala = sala
        self.filme = filme
        self.data = data
        self.hora_inicio = hora_inicio
        self._assentos: AssentosDict = AssentosDict(sessao_codigo=codigo)

    @property
    def codigo(self) -> int | None:
        return self._codigo

    @codigo.setter
    def codigo(self, value: int | None) -> None:
        self._codigo = value
        if hasattr(self, "_assentos") and isinstance(self._assentos, AssentosDict):
            self._assentos._sessao_codigo = value

    @property
    def db_path(self) -> str | Path | None:
        return self._db_path

    @db_path.setter
    def db_path(self, value: str | Path | None) -> None:
        self._db_path = value
        if hasattr(self, "_assentos") and isinstance(self._assentos, AssentosDict):
            self._assentos._db_path = value

    @property
    def assentos(self) -> AssentosDict:
        return self._assentos

    @assentos.setter
    def assentos(self, value: Mapping[int, int] | None) -> None:
        if isinstance(value, AssentosDict):
            self._assentos = value
        else:
            self._assentos = AssentosDict(
                sessao_codigo=self._codigo,
                db_path=self._db_path,
                initial=value,
            )

    def ocupar_assento(self, seat: int) -> None:
        self.assentos[seat] = 1

    def liberar_assento(self, seat: int) -> None:
        self.assentos[seat] = 0

    def tem_assentos_disponiveis(self) -> bool:
        return any(status == 0 for status in self.assentos.values())

    __hash__ = None

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
