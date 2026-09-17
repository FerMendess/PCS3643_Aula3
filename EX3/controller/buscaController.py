# ruff: noqa: N999
"""Controller for query/search operations across domain entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from controller.filme_controller import FilmeController
from controller.sala_controller import SalaController
from controller.sessao_controller import SessaoController
from controller.tipo_ingresso_controller import TipoIngressoController

if TYPE_CHECKING:
    from model.filme import Filme
    from model.sala import Sala
    from model.sessao import Sessao
    from model.tipo_ingresso import TipoIngresso


class BuscaController:
    def __init__(self, db_path: str | None = None) -> None:
        self.filme_ctrl = FilmeController(db_path)
        self.sala_ctrl = SalaController(db_path)
        self.sessao_ctrl = SessaoController(db_path)
        self.tipo_ingresso_ctrl = TipoIngressoController(db_path)

    def pegar_filme(self, codigo: int | str) -> Filme | None:
        return self.filme_ctrl.buscar_filme(codigo)

    def listar_filmes(self) -> list[Filme]:
        return self.filme_ctrl.listar_filmes()

    def pegar_sala(self, numero: int | str) -> Sala | None:
        return self.sala_ctrl.buscar_sala(numero)

    def listar_salas(self) -> list[Sala]:
        return self.sala_ctrl.listar_salas()

    def pegar_sessao(self, codigo: int | str) -> Sessao | None:
        return self.sessao_ctrl.buscar_sessao(codigo)

    def listar_sessoes(self) -> list[Sessao]:
        return self.sessao_ctrl.listar_sessoes()

    def pegar_tipo_ingresso(self, tipo: str) -> TipoIngresso | None:
        return self.tipo_ingresso_ctrl.buscar_tipo_ingresso(tipo)

    def listar_filmes_por_data(self, data: str) -> str:
        return self.sessao_ctrl.listar_filmes_por_data(data)
