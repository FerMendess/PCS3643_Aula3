"""Unit tests for Sessao domain model and Pydantic schemas."""

import unittest

from pydantic import ValidationError

from src.model.filme import Filme
from src.model.sala import Sala
from src.model.sessao import (
    AssentosDict,
    CompraIngressoRequest,
    CompraIngressoResponse,
    Sessao,
    SessaoCreate,
    SessaoDisponivelResponse,
    SessaoUpdate,
)


class TestSessaoModel(unittest.TestCase):
    def test_sessao_initialization_and_equality(self):
        sala1 = Sala(numero=1, capacidade=10, tipo="2D")
        sala2 = Sala(numero=2, capacidade=10, tipo="2D")
        filme1 = Filme(
            codigo=1,
            nome="Matrix",
            data_estreia="01/01/2026",
            data_saida="10/01/2026",
            duracao=120,
        )

        sessao1 = Sessao(
            sala=sala1, filme=filme1, data="05/01/2026", hora_inicio=20, codigo=1
        )
        sessao2 = Sessao(
            sala=sala1, filme=filme1, data="05/01/2026", hora_inicio=20, codigo=1
        )
        sessao3 = Sessao(
            sala=sala2, filme=filme1, data="05/01/2026", hora_inicio=20, codigo=2
        )

        self.assertEqual(sessao1, sessao2)
        self.assertNotEqual(sessao1, sessao3)
        self.assertNotEqual(sessao1, None)

    def test_sessao_schemas_validation(self):
        create = SessaoCreate(
            numero_sala=1, codigo_filme=1, data="05/01/2026", hora_inicio=20
        )
        self.assertEqual(create.hora_inicio, 20)

        with self.assertRaises(ValidationError):
            SessaoCreate(
                numero_sala=0, codigo_filme=1, data="05/01/2026", hora_inicio=20
            )

        with self.assertRaises(ValidationError):
            SessaoCreate(
                numero_sala=1, codigo_filme=1, data="05/01/2026", hora_inicio=25
            )

        update = SessaoUpdate(hora_inicio=22)
        self.assertEqual(update.hora_inicio, 22)

        compra_req = CompraIngressoRequest(assentos=[1, 2], tipos_ingresso=[0, 1])
        self.assertEqual(len(compra_req.assentos), 2)

        with self.assertRaises(ValidationError):
            CompraIngressoRequest(assentos=[], tipos_ingresso=[])

        compra_resp = CompraIngressoResponse(
            codigo_sessao=1, assentos_comprados=[1], total=30
        )
        self.assertEqual(compra_resp.total, 30)

        disp_resp = SessaoDisponivelResponse(
            codigo=1,
            filme_nome="Matrix",
            numero_sala=1,
            tipo_sala="2D",
            hora_inicio=20,
            valor=30,
            descricao="Desc",
        )
        self.assertEqual(disp_resp.codigo, 1)

    def test_sessao_assentos_domain_methods(self):
        sessao = Sessao()
        sessao.assentos = {1: 0, 2: 0}
        self.assertTrue(sessao.tem_assentos_disponiveis())
        sessao.ocupar_assento(1)
        self.assertEqual(sessao.assentos[1], 1)
        self.assertTrue(sessao.tem_assentos_disponiveis())
        sessao.ocupar_assento(2)
        self.assertFalse(sessao.tem_assentos_disponiveis())
        sessao.liberar_assento(1)
        self.assertEqual(sessao.assentos[1], 0)
        self.assertTrue(sessao.tem_assentos_disponiveis())

    def test_sessao_assentos_setter_and_property_propagation(self):
        sessao = Sessao()
        self.assertIsInstance(sessao.assentos, AssentosDict)
        self.assertIsNone(sessao.assentos._sessao_codigo)

        sessao.codigo = 42
        self.assertEqual(sessao.assentos._sessao_codigo, 42)

        sessao.db_path = "test.db"
        self.assertEqual(sessao.assentos._db_path, "test.db")

        sessao.assentos = {1: 0, 2: 1}
        self.assertIsInstance(sessao.assentos, AssentosDict)
        self.assertEqual(sessao.assentos._sessao_codigo, 42)
        self.assertEqual(sessao.assentos._db_path, "test.db")
        self.assertEqual(sessao.assentos[1], 0)
        self.assertEqual(sessao.assentos[2], 1)
