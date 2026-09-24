"""Unit tests for Sala domain model and Pydantic schemas."""

import unittest

from pydantic import ValidationError

from src.model.sala import Sala, SalaCreate, SalaResponse, SalaUpdate


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
            SalaCreate(numero=1, capacidade=50, tipo="4D")

        update = SalaUpdate(capacidade=60)
        self.assertEqual(update.capacidade, 60)

        resp = SalaResponse.model_validate(Sala(numero=1, capacidade=50, tipo="2D"))
        self.assertEqual(resp.numero, 1)
