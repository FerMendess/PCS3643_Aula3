# ruff: noqa: N999
"""Controller for query/search operations across domain entities."""

from pathlib import Path

from controller.filme_controller import FilmeController
from controller.sala_controller import SalaController
from controller.sessao_controller import SessaoController
from controller.tipo_ingresso_controller import TipoIngressoController
from model.filme import Filme
from model.sala import Sala
from model.sessao import Sessao
from model.tipo_ingresso import TipoIngresso

__all__ = ["BuscaController"]


class BuscaController:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self._filme_ctrl = FilmeController(db_path)
        self._sala_ctrl = SalaController(db_path)
        self._sessao_ctrl = SessaoController(db_path)
        self._tipo_ingresso_ctrl = TipoIngressoController(db_path)

    @property
    def filme_ctrl(self) -> FilmeController:
        return self._filme_ctrl

    @property
    def sala_ctrl(self) -> SalaController:
        return self._sala_ctrl

    @property
    def sessao_ctrl(self) -> SessaoController:
        return self._sessao_ctrl

    @property
    def tipo_ingresso_ctrl(self) -> TipoIngressoController:
        return self._tipo_ingresso_ctrl

    def pegar_filme(self, codigo: int | str) -> Filme | None:
        return self._filme_ctrl.buscar_filme(codigo)

    def listar_filmes(self) -> list[Filme]:
        return self._filme_ctrl.listar_filmes()

    def pegar_sala(self, numero: int | str) -> Sala | None:
        return self._sala_ctrl.buscar_sala(numero)

    def listar_salas(self) -> list[Sala]:
        return self._sala_ctrl.listar_salas()

    def pegar_sessao(self, codigo: int | str) -> Sessao | None:
        return self._sessao_ctrl.buscar_sessao(codigo)

    def listar_sessoes(self) -> list[Sessao]:
        return self._sessao_ctrl.listar_sessoes()

    def pegar_tipo_ingresso(self, tipo: str) -> TipoIngresso | None:
        return self._tipo_ingresso_ctrl.buscar_tipo_ingresso(tipo)

    def listar_filmes_por_data(self, data: str) -> str:
        return self._sessao_ctrl.listar_filmes_por_data(data)
