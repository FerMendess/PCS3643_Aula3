"""Unit tests for Filme domain model and Pydantic schemas."""

import unittest

from pydantic import ValidationError

from src.model.filme import Filme, FilmeCreate, FilmeResponse, FilmeUpdate


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
