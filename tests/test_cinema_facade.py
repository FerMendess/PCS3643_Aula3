"""Unit tests verifying the cinema_facade module interface."""

import unittest

import cinema_facade
from tests.helpers import reiniciar_estado


class TestCinemaFacade(unittest.TestCase):
    def setUp(self) -> None:
        reiniciar_estado()

    def test_facade_fluxo_completo(self) -> None:
        filme = cinema_facade.cadastrar_filme("Matrix", "21/05/1999", "21/08/1999", 136)
        self.assertIsNotNone(filme)
        assert filme is not None and filme.codigo is not None

        filme_buscado = cinema_facade.pegar_filme(filme.codigo)
        self.assertIsNotNone(filme_buscado)
        assert filme_buscado is not None
        self.assertEqual(filme_buscado.nome, "Matrix")

        cadastrou_preco = cinema_facade.cadastrar_valor_ingresso("2D", 30)
        self.assertTrue(cadastrou_preco)

        sala = cinema_facade.cadastrar_sala(1, 50, "2D")
        self.assertIsNotNone(sala)
        assert sala is not None and sala.numero is not None

        sala_buscada = cinema_facade.pegar_sala(sala.numero)
        self.assertIsNotNone(sala_buscada)
        assert sala_buscada is not None
        self.assertEqual(sala_buscada.capacidade, 50)

        sessao = cinema_facade.cadastrar_sessao(
            sala.numero, filme.codigo, "01/06/1999", 20
        )
        self.assertIsNotNone(sessao)
        assert sessao is not None and sessao.codigo is not None

        sessao_buscada = cinema_facade.pegar_sessao(sessao.codigo)
        self.assertIsNotNone(sessao_buscada)
        assert sessao_buscada is not None
        self.assertEqual(sessao_buscada.hora_inicio, 20)

        lista_filmes = cinema_facade.listar_filmes_por_data("01/06/1999")
        self.assertIn("Matrix", lista_filmes)

        valor_total = cinema_facade.comprarIngressos(sessao.codigo, [1, 2], [0, 1])
        self.assertEqual(valor_total, 45)
