"""Cinema facade delegating to MVC controllers without mutable global state."""

from src.controller.filme_controller import FilmeController
from src.controller.sala_controller import SalaController
from src.controller.sessao_controller import SessaoController
from src.controller.tipo_ingresso_controller import TipoIngressoController
from src.model.filme import Filme
from src.model.sala import Sala
from src.model.sessao import Sessao

_filme_ctrl = FilmeController()
_sala_ctrl = SalaController()
_tipo_ingresso_ctrl = TipoIngressoController()
_sessao_ctrl = SessaoController()


def pegar_sala(numero: int | str) -> Sala | None:
    return _sala_ctrl.buscar_sala(numero)


def pegar_filme(codigo: int | str) -> Filme | None:
    return _filme_ctrl.buscar_filme(codigo)


def pegar_sessao(codigo: int | str) -> Sessao | None:
    return _sessao_ctrl.buscar_sessao(codigo)


def cadastrar_filme(
    nome: str, data_estreia: str, data_saida: str, duracao: int
) -> Filme | None:
    return _filme_ctrl.cadastrar_filme(nome, data_estreia, data_saida, duracao)


def cadastrar_valor_ingresso(tipo_sala_param: str, valor_ingresso: int) -> bool:
    return _tipo_ingresso_ctrl.cadastrar_tipo_ingresso(tipo_sala_param, valor_ingresso)


def cadastrar_sala(numero: int, capacidade: int, tipo_sala_param: str) -> Sala | None:
    return _sala_ctrl.cadastrar_sala(numero, capacidade, tipo_sala_param)


def cadastrar_sessao(
    numero_sala: int, codigo_filme: int, data_sessao: str, hora_inicio: int
) -> Sessao | None:
    return _sessao_ctrl.cadastrar_sessao(
        numero_sala, codigo_filme, data_sessao, hora_inicio
    )


def listar_filmes_por_data(data: str) -> str:
    return _sessao_ctrl.listar_filmes_por_data(data)


def comprarIngressos(  # noqa: N802
    codigo_sessao: int, assentos_param: list[int], tipos_ingresso: list[int]
) -> int | float:
    return _sessao_ctrl.comprar_ingressos(codigo_sessao, assentos_param, tipos_ingresso)
