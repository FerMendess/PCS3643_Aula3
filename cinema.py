"""Backward-compatibility module re-exporting cinema_facade."""

from cinema_facade import (
    cadastrar_filme,
    cadastrar_sala,
    cadastrar_sessao,
    cadastrar_valor_ingresso,
    comprarIngressos,
    listar_filmes_por_data,
    pegar_filme,
    pegar_sala,
    pegar_sessao,
)

__all__ = [
    "cadastrar_filme",
    "cadastrar_sala",
    "cadastrar_sessao",
    "cadastrar_valor_ingresso",
    "comprarIngressos",
    "listar_filmes_por_data",
    "pegar_filme",
    "pegar_sala",
    "pegar_sessao",
]
