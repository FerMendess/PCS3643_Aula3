"""Unit tests for TipoIngresso domain model and Pydantic schemas."""

import unittest

from pydantic import ValidationError

from src.model.tipo_ingresso import (
    TipoIngresso,
    TipoIngressoCreate,
    TipoIngressoResponse,
    TipoIngressoUpdate,
)


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
