"""Integration tests for Sessao REST API and ticket purchase endpoints."""

import unittest

from fastapi.testclient import TestClient

from app import app
from tests.helpers import reiniciar_estado


class TestSessaoView(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.client = TestClient(app)

    def test_api_sessoes_crud_e_compra(self):
        self.client.post("/tipos-ingresso/", json={"tipo": "2D", "valor": 40})
        self.client.post("/salas/", json={"numero": 1, "capacidade": 4, "tipo": "2D"})
        res_filme = self.client.post(
            "/filmes/",
            json={
                "nome": "Gladiador II",
                "data_estreia": "01/11/2026",
                "data_saida": "30/11/2026",
                "duracao": 150,
            },
        )
        cod_filme = res_filme.json()["codigo"]

        res_sessao = self.client.post(
            "/sessoes/",
            json={
                "numero_sala": 1,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )
        self.assertEqual(res_sessao.status_code, 201)
        cod_sessao = res_sessao.json()["codigo"]
        self.assertEqual(len(res_sessao.json()["assentos"]), 4)

        res_list = self.client.get("/sessoes/")
        self.assertEqual(res_list.status_code, 200)
        self.assertEqual(len(res_list.json()), 1)

        res_data = self.client.get("/sessoes/data/15/11/2026")
        self.assertEqual(res_data.status_code, 200)
        self.assertEqual(len(res_data.json()), 1)
        self.assertIn("Gladiador II", res_data.json()[0]["descricao"])

        res_compra = self.client.post(
            f"/sessoes/{cod_sessao}/comprar",
            json={"assentos": [1, 2], "tipos_ingresso": [0, 1]},
        )
        self.assertEqual(res_compra.status_code, 200)
        self.assertEqual(res_compra.json()["total"], 60)

        res_compra_repetida = self.client.post(
            f"/sessoes/{cod_sessao}/comprar",
            json={"assentos": [1], "tipos_ingresso": [0]},
        )
        self.assertEqual(res_compra_repetida.status_code, 400)

        res_del = self.client.delete(f"/sessoes/{cod_sessao}")
        self.assertEqual(res_del.status_code, 204)
