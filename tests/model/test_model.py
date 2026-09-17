"""Unit tests for Model entities and schemas."""

import unittest

from pydantic import ValidationError

from src.model.filme import Filme, FilmeCreate, FilmeResponse, FilmeUpdate
from src.model.sala import Sala, SalaCreate, SalaResponse, SalaUpdate
from src.model.sessao import (
    CompraIngressoRequest,
    CompraIngressoResponse,
    Sessao,
    SessaoCreate,
    SessaoDisponivelResponse,
    SessaoUpdate,
)
from src.model.tipo_ingresso import (
    TipoIngresso,
    TipoIngressoCreate,
    TipoIngressoResponse,
    TipoIngressoUpdate,
)


class TestFilmeModel(unittest.TestCase):
    def test_filme_initialization_and_equality(self):
        f1 = Filme(
            nome="Matrix",
            data_estreia="01/01/2026",
            data_saida="10/01/2026",
            duracao=120,
            codigo=1,
        )
        f2 = Filme(
            nome="Matrix",
            data_estreia="01/01/2026",
            data_saida="10/01/2026",
            duracao=120,
            codigo=1,
        )
        f3 = Filme(
            nome="Matrix 2",
            data_estreia="01/01/2026",
            data_saida="10/01/2026",
            duracao=120,
            codigo=2,
        )

        self.assertEqual(f1, f2)
        self.assertNotEqual(f1, f3)
        self.assertNotEqual(f1, "not a filme")

    def test_filme_schemas_validation(self):
        create = FilmeCreate(
            nome="Matrix",
            data_estreia="01/01/2026",
            data_saida="10/01/2026",
            duracao=120,
        )
        self.assertEqual(create.duracao, 120)

        with self.assertRaises(ValidationError):
            FilmeCreate(
                nome="", data_estreia="01/01/2026", data_saida="10/01/2026", duracao=120
            )

        with self.assertRaises(ValidationError):
            FilmeCreate(
                nome="Matrix",
                data_estreia="01/01/2026",
                data_saida="10/01/2026",
                duracao=0,
            )

        update = FilmeUpdate(duracao=130)
        self.assertEqual(update.duracao, 130)

        resp = FilmeResponse.model_validate(
            Filme(
                codigo=1,
                nome="Matrix",
                data_estreia="01/01/2026",
                data_saida="10/01/2026",
                duracao=120,
            )
        )
        self.assertEqual(resp.codigo, 1)


class TestSalaModel(unittest.TestCase):
    def test_sala_initialization_and_equality(self):
        s1 = Sala(numero=1, capacidade=50, tipo="2D")
        s2 = Sala(numero=1, capacidade=50, tipo="2D")
        s3 = Sala(numero=2, capacidade=50, tipo="2D")

        self.assertEqual(s1, s2)
        self.assertNotEqual(s1, s3)
        self.assertNotEqual(s1, None)

    def test_sala_schemas_validation(self):
        create = SalaCreate(numero=1, capacidade=50, tipo="2D")
        self.assertEqual(create.numero, 1)

        with self.assertRaises(ValidationError):
            SalaCreate(numero=0, capacidade=50, tipo="2D")

        with self.assertRaises(ValidationError):
            SalaCreate(numero=1, capacidade=0, tipo="2D")

        with self.assertRaises(ValidationError):
            SalaCreate(numero=1, capacidade=50, tipo="4D")  # type: ignore[arg-type]

        update = SalaUpdate(capacidade=60)
        self.assertEqual(update.capacidade, 60)

        resp = SalaResponse.model_validate(Sala(numero=1, capacidade=50, tipo="2D"))
        self.assertEqual(resp.numero, 1)


class TestTipoIngressoModel(unittest.TestCase):
    def test_tipo_ingresso_initialization_and_equality(self):
        t1 = TipoIngresso(tipo="2D", valor=30)
        t2 = TipoIngresso(tipo="2D", valor=30)
        t3 = TipoIngresso(tipo="3D", valor=40)

        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)
        self.assertNotEqual(t1, 30)

    def test_tipo_ingresso_schemas_validation(self):
        create = TipoIngressoCreate(tipo="2D", valor=30)
        self.assertEqual(create.valor, 30)

        with self.assertRaises(ValidationError):
            TipoIngressoCreate(tipo="", valor=30)

        with self.assertRaises(ValidationError):
            TipoIngressoCreate(tipo="2D", valor=-5)

        update = TipoIngressoUpdate(valor=35)
        self.assertEqual(update.valor, 35)

        resp = TipoIngressoResponse.model_validate(TipoIngresso(tipo="2D", valor=30))
        self.assertEqual(resp.tipo, "2D")


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
