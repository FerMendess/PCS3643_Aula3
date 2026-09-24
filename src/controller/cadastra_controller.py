"""Controller for creation/registration operations across domain entities."""

from pathlib import Path

from src.controller.filme_controller import FilmeController
from src.controller.sala_controller import SalaController
from src.controller.sessao_controller import SessaoController
from src.controller.tipo_ingresso_controller import TipoIngressoController
from src.model.filme import Filme
from src.model.sala import Sala
from src.model.sessao import Sessao


class CadastraController:
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

    def cadastrar_filme(
        self, nome: str, data_estreia: str, data_saida: str, duracao: int
    ) -> Filme | None:
        return self._filme_ctrl.cadastrar_filme(nome, data_estreia, data_saida, duracao)

    def cadastrar_sala(
        self, numero: int, capacidade: int, tipo_sala: str
    ) -> Sala | None:
        return self._sala_ctrl.cadastrar_sala(numero, capacidade, tipo_sala)

    def cadastrar_valor_ingresso(self, tipo_sala: str, valor_ingresso: int) -> bool:
        return self._tipo_ingresso_ctrl.cadastrar_tipo_ingresso(
            tipo_sala, valor_ingresso
        )

    def cadastrar_sessao(
        self, numero_sala: int, codigo_filme: int, data_sessao: str, hora_inicio: int
    ) -> Sessao | None:
        return self._sessao_ctrl.cadastrar_sessao(
            numero_sala, codigo_filme, data_sessao, hora_inicio
        )
