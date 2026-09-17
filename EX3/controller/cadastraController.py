# ruff: noqa: N999
"""Controller for creation/registration operations across domain entities."""

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


class CadastraController:
    def __init__(self, db_path: str | None = None) -> None:
        self.filme_ctrl = FilmeController(db_path)
        self.sala_ctrl = SalaController(db_path)
        self.sessao_ctrl = SessaoController(db_path)
        self.tipo_ingresso_ctrl = TipoIngressoController(db_path)

    def cadastrar_filme(
        self, nome: str, data_estreia: str, data_saida: str, duracao: int
    ) -> Filme | None:
        return self.filme_ctrl.cadastrar_filme(nome, data_estreia, data_saida, duracao)

    def cadastrar_sala(
        self, numero: int, capacidade: int, tipo_sala: str
    ) -> Sala | None:
        return self.sala_ctrl.cadastrar_sala(numero, capacidade, tipo_sala)

    def cadastrar_valor_ingresso(self, tipo_sala: str, valor_ingresso: int) -> bool:
        return self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso(
            tipo_sala, valor_ingresso
        )

    def cadastrar_sessao(
        self, numero_sala: int, codigo_filme: int, data_sessao: str, hora_inicio: int
    ) -> Sessao | None:
        return self.sessao_ctrl.cadastrar_sessao(
            numero_sala, codigo_filme, data_sessao, hora_inicio
        )
