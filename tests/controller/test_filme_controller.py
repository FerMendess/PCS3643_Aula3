"""Unit tests for FilmeController and filme registration business rules."""

import unittest

from src.controller.busca_controller import BuscaController
from src.controller.filme_controller import FilmeController
from tests.helpers import reiniciar_estado


class TestCadastrarFilme(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.filme_ctrl = FilmeController()

    def test_cadastrar_filme_sucesso(self):
        filme = self.filme_ctrl.cadastrar_filme(
            "Matrix", "21/05/1999", "21/08/1999", 136
        )
        self.assertIsNotNone(filme)
        assert filme is not None
        self.assertEqual(filme.codigo, 1)
        self.assertEqual(filme.nome, "Matrix")
        self.assertEqual(filme.data_estreia, "21/05/1999")
        self.assertEqual(filme.data_saida, "21/08/1999")
        self.assertEqual(filme.duracao, 136)
        buscado = self.filme_ctrl.buscar_filme(filme.codigo)
        self.assertIsNotNone(buscado)

    def test_cadastrar_multiplos_filmes_codigos_sequenciais(self):
        f1 = self.filme_ctrl.cadastrar_filme("Filme 1", "01/01/2026", "10/01/2026", 100)
        f2 = self.filme_ctrl.cadastrar_filme("Filme 2", "05/01/2026", "15/01/2026", 120)
        self.assertIsNotNone(f1)
        self.assertIsNotNone(f2)
        assert f1 is not None and f2 is not None
        self.assertEqual(f1.codigo, 1)
        self.assertEqual(f2.codigo, 2)

    def test_cadastrar_filme_data_invalida(self):
        filme = self.filme_ctrl.cadastrar_filme(
            "Matrix", "32/01/2026", "10/02/2026", 120
        )
        self.assertIsNone(filme)
        filme2 = self.filme_ctrl.cadastrar_filme(
            "Matrix", "data_errada", "10/02/2026", 120
        )
        self.assertIsNone(filme2)

    def test_cadastrar_filme_saida_anterior_a_estreia(self):
        filme = self.filme_ctrl.cadastrar_filme(
            "Matrix", "20/05/2026", "10/05/2026", 120
        )
        self.assertIsNone(filme)

    def test_cadastrar_filme_duracao_invalida(self):
        filme_zero = self.filme_ctrl.cadastrar_filme(
            "Matrix", "01/01/2026", "10/01/2026", 0
        )
        self.assertIsNone(filme_zero)
        filme_neg = self.filme_ctrl.cadastrar_filme(
            "Matrix", "01/01/2026", "10/01/2026", -90
        )
        self.assertIsNone(filme_neg)

    def test_cadastrar_filme_nome_invalido(self):
        filme = self.filme_ctrl.cadastrar_filme("", "01/01/2026", "10/01/2026", 100)
        self.assertIsNone(filme)
        filme_spaces = self.filme_ctrl.cadastrar_filme(
            "   ", "01/01/2026", "10/01/2026", 100
        )
        self.assertIsNone(filme_spaces)

    def test_cadastrar_filme_nome_repetido(self):
        f1 = self.filme_ctrl.cadastrar_filme("Carros", "01/01/2010", "01/03/2010", 115)
        self.assertIsNotNone(f1)
        f2 = self.filme_ctrl.cadastrar_filme("Carros", "01/01/2010", "01/03/2010", 115)
        self.assertIsNone(f2)


class TestFilmeControllerCRUD(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.filme_ctrl = FilmeController()
        self.busca_ctrl = BuscaController()

    def test_filme_crud_completo(self):
        filme = self.filme_ctrl.cadastrar_filme(
            "Interestelar", "10/10/2026", "20/10/2026", 169
        )
        self.assertIsNotNone(filme)
        assert filme is not None
        self.assertEqual(filme.nome, "Interestelar")

        buscado = self.busca_ctrl.pegar_filme(filme.codigo)  # type: ignore[arg-type]
        self.assertIsNotNone(buscado)
        assert buscado is not None
        self.assertEqual(buscado.nome, "Interestelar")

        editado = self.filme_ctrl.editar_filme(
            filme.codigo, nome="Interestelar IMAX", duracao=175
        )  # type: ignore[arg-type]
        self.assertIsNotNone(editado)
        assert editado is not None
        self.assertEqual(editado.nome, "Interestelar IMAX")
        self.assertEqual(editado.duracao, 175)

        lista = self.filme_ctrl.listar_filmes()
        self.assertEqual(len(lista), 1)

        removido = self.filme_ctrl.remover_filme(filme.codigo)  # type: ignore[arg-type]
        self.assertTrue(removido)
        self.assertIsNone(self.filme_ctrl.buscar_filme(filme.codigo))  # type: ignore[arg-type]
