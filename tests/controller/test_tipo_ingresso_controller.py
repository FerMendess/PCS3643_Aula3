"""Unit tests for TipoIngressoController and ticket pricing business rules."""

import unittest

from src.controller.tipo_ingresso_controller import TipoIngressoController
from tests.helpers import reiniciar_estado


class TestCadastrarValorIngresso(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.tipo_ingresso_ctrl = TipoIngressoController()

    def test_cadastrar_valor_ingresso_2d_sucesso(self):
        resultado = self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso("2D", 30)
        self.assertTrue(resultado)
        tipo = self.tipo_ingresso_ctrl.buscar_tipo_ingresso("2D")
        self.assertIsNotNone(tipo)
        assert tipo is not None
        self.assertEqual(tipo.valor, 30)

    def test_cadastrar_valor_ingresso_3d_sucesso(self):
        resultado = self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso("3D", 45)
        self.assertTrue(resultado)
        tipo = self.tipo_ingresso_ctrl.buscar_tipo_ingresso("3D")
        self.assertIsNotNone(tipo)
        assert tipo is not None
        self.assertEqual(tipo.valor, 45)

    def test_cadastrar_valor_ingresso_tipo_invalido(self):
        self.assertFalse(self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso("4D", 50))
        self.assertFalse(self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso("IMAX", 60))
        self.assertFalse(self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso("", 30))
        self.assertFalse(self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso(None, 30))

    def test_cadastrar_valor_ingresso_valor_menor_ou_igual_a_zero(self):
        self.assertFalse(self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso("2D", 0))
        self.assertFalse(self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso("2D", -20))

    def test_cadastrar_valor_ingresso_valor_nao_inteiro(self):
        self.assertFalse(self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso("2D", 35.5))
        self.assertFalse(self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso("2D", "30"))


class TestTipoIngressoControllerCRUD(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.tipo_ingresso_ctrl = TipoIngressoController()

    def test_tipo_ingresso_crud_completo(self):
        cadastrado = self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso("2D", 35)
        self.assertTrue(cadastrado)

        buscado = self.tipo_ingresso_ctrl.buscar_tipo_ingresso("2D")
        self.assertIsNotNone(buscado)
        assert buscado is not None
        self.assertEqual(buscado.valor, 35)

        editado = self.tipo_ingresso_ctrl.editar_tipo_ingresso("2D", 40)
        self.assertIsNotNone(editado)
        assert editado is not None
        self.assertEqual(editado.valor, 40)

        lista = self.tipo_ingresso_ctrl.listar_tipos_ingresso()
        self.assertEqual(len(lista), 1)

        removido = self.tipo_ingresso_ctrl.remover_tipo_ingresso("2D")
        self.assertTrue(removido)
        self.assertIsNone(self.tipo_ingresso_ctrl.buscar_tipo_ingresso("2D"))
