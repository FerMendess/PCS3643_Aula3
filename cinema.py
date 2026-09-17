"""Cinema facade delegating to MVC controllers and synchronizing with SQLite."""

from typing import Any, TypeVar, override

from controller.filme_controller import FilmeController, validar_data
from controller.sala_controller import SalaController
from controller.sessao_controller import SessaoController
from controller.tipo_ingresso_controller import TipoIngressoController
from model.database import init_db, reset_db
from model.filme import Filme
from model.sala import Sala
from model.sessao import Sessao

init_db()

_filme_ctrl = FilmeController()
_sala_ctrl = SalaController()
_tipo_ingresso_ctrl = TipoIngressoController()
_sessao_ctrl = SessaoController()

_T = TypeVar("_T")
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


class _SynchronizedList(list[_T]):
    def __init__(self, clear_callback: Any = None) -> None:
        super().__init__()
        self._clear_callback = clear_callback

    @override
    def clear(self) -> None:
        super().clear()
        if self._clear_callback:
            self._clear_callback()


class _SynchronizedDict(dict[_KT, _VT]):
    def __init__(self, clear_callback: Any = None) -> None:
        super().__init__()
        self._clear_callback = clear_callback

    @override
    def clear(self) -> None:
        super().clear()
        if self._clear_callback:
            self._clear_callback()


def _clear_all_db() -> None:
    reset_db()


filmes: list[Filme] = _SynchronizedList(clear_callback=_clear_all_db)
salas: list[Sala] = _SynchronizedList(clear_callback=_clear_all_db)
sessoes: list[Sessao] = _SynchronizedList(clear_callback=_clear_all_db)
tipo_sala: dict[str, int] = _SynchronizedDict(clear_callback=_clear_all_db)


def _validar_data(data_str: str) -> Any:
    return validar_data(data_str)


def pegar_sala(numero: int | str) -> Sala | None:
    return _sala_ctrl.buscar_sala(numero)


def pegar_filme(codigo: int | str) -> Filme | None:
    return _filme_ctrl.buscar_filme(codigo)


def pegar_sessao(codigo: int | str) -> Sessao | None:
    sessao = _sessao_ctrl.buscar_sessao(codigo)
    if sessao:
        for s in sessoes:
            if s.codigo == sessao.codigo:
                s.assentos = sessao.assentos
                return s
    return sessao


def cadastrar_filme(
    nome: str, data_estreia: str, data_saida: str, duracao: int
) -> Filme | None:
    filme = _filme_ctrl.cadastrar_filme(nome, data_estreia, data_saida, duracao)
    if filme is not None:
        filmes.append(filme)
    return filme


def cadastrar_valor_ingresso(tipo_sala_param: str, valor_ingresso: int) -> bool:
    sucesso = _tipo_ingresso_ctrl.cadastrar_tipo_ingresso(
        tipo_sala_param, valor_ingresso
    )
    if sucesso:
        tipo_sala[tipo_sala_param] = valor_ingresso
    return sucesso


def cadastrar_sala(numero: int, capacidade: int, tipo_sala_param: str) -> Sala | None:
    sala = _sala_ctrl.cadastrar_sala(numero, capacidade, tipo_sala_param)
    if sala is not None:
        salas.append(sala)
    return sala


def cadastrar_sessao(
    numero_sala: int, codigo_filme: int, data_sessao: str, hora_inicio: int
) -> Sessao | None:
    sessao = _sessao_ctrl.cadastrar_sessao(
        numero_sala, codigo_filme, data_sessao, hora_inicio
    )
    if sessao is not None:
        sessoes.append(sessao)
    return sessao


def listar_filmes_por_data(data: str) -> str:
    return _sessao_ctrl.listar_filmes_por_data(data)


def comprarIngressos(  # noqa: N802
    codigo_sessao: int, assentos_param: list[int], tipos_ingresso: list[int]
) -> int | float:
    total = _sessao_ctrl.comprar_ingressos(
        codigo_sessao, assentos_param, tipos_ingresso
    )
    if total > 0:
        sessao = pegar_sessao(codigo_sessao)
        if sessao:
            for assento in assentos_param:
                sessao.assentos[assento] = 1
    return total
