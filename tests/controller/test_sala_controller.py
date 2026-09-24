"""Unit tests for SalaController and sala registration business rules."""

import unittest

from src.controller.busca_controller import BuscaController
from src.controller.cadastra_controller import CadastraController
from src.controller.sala_controller import SalaController
from tests.helpers import reiniciar_estado


class TestCadastrarSala(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.sala_ctrl = SalaController()

    def test_cadastrar_sala_sucesso(self):
        sala = self.sala_ctrl.cadastrar_sala(1, 50, "2D")
        self.assertIsNotNone(sala)
        assert sala is not None
        self.assertEqual(sala.numero, 1)
        self.assertEqual(sala.capacidade, 50)
        self.assertEqual(sala.tipo, "2D")
        buscada = self.sala_ctrl.buscar_sala(sala.numero)
        self.assertIsNotNone(buscada)

    def test_cadastrar_sala_numero_repetido(self):
        s1 = self.sala_ctrl.cadastrar_sala(1, 50, "2D")
        self.assertIsNotNone(s1)
        s2 = self.sala_ctrl.cadastrar_sala(1, 60, "3D")
        self.assertIsNone(s2)
        self.assertEqual(len(self.sala_ctrl.listar_salas()), 1)

    def test_cadastrar_sala_numero_invalido(self):
        self.assertIsNone(self.sala_ctrl.cadastrar_sala(0, 50, "2D"))
        self.assertIsNone(self.sala_ctrl.cadastrar_sala(-1, 50, "2D"))

    def test_cadastrar_sala_capacidade_invalida(self):
        self.assertIsNone(self.sala_ctrl.cadastrar_sala(2, 0, "2D"))
        self.assertIsNone(self.sala_ctrl.cadastrar_sala(2, -10, "2D"))

    def test_cadastrar_sala_tipo_invalido(self):
        self.assertIsNone(self.sala_ctrl.cadastrar_sala(3, 50, "4D"))
        self.assertIsNone(self.sala_ctrl.cadastrar_sala(3, 50, ""))
        self.assertIsNone(self.sala_ctrl.cadastrar_sala(3, 50, None))


class TestSalaControllerCRUD(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.sala_ctrl = SalaController()
        self.cadastra_ctrl = CadastraController()
        self.busca_ctrl = BuscaController()

    def test_sala_crud_completo(self):
        sala = self.cadastra_ctrl.cadastrar_sala(5, 60, "3D")
        self.assertIsNotNone(sala)
        assert sala is not None
        self.assertEqual(sala.numero, 5)

        buscada = self.sala_ctrl.buscar_sala(5)
        self.assertIsNotNone(buscada)
        assert buscada is not None
        self.assertEqual(buscada.capacidade, 60)

        editada = self.sala_ctrl.editar_sala(5, capacidade=75, tipo="2D")
        self.assertIsNotNone(editada)
        assert editada is not None
        self.assertEqual(editada.capacidade, 75)
        self.assertEqual(editada.tipo, "2D")

        lista = self.busca_ctrl.listar_salas()
        self.assertEqual(len(lista), 1)

        removida = self.sala_ctrl.remover_sala(5)
        self.assertTrue(removida)
        self.assertIsNone(self.sala_ctrl.buscar_sala(5))
