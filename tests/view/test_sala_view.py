"""Integration tests for Sala REST API endpoints."""

import unittest

from fastapi.testclient import TestClient

from app import app
from tests.helpers import reiniciar_estado


class TestSalaView(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.client = TestClient(app)

    def test_cadastrar_sala_sucesso(self):
        payload = {"numero": 10, "capacidade": 80, "tipo": "3D"}
        response = self.client.post("/salas/", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["numero"], 10)
        self.assertEqual(data["capacidade"], 80)
        self.assertEqual(data["tipo"], "3D")

    def test_cadastrar_sala_duplicada_ou_invalida(self):
        payload = {"numero": 10, "capacidade": 80, "tipo": "3D"}
        res_first = self.client.post("/salas/", json=payload)
        self.assertEqual(res_first.status_code, 201)

        res_dup = self.client.post("/salas/", json=payload)
        self.assertEqual(res_dup.status_code, 400)

    def test_listar_salas(self):
        self.client.post("/salas/", json={"numero": 1, "capacidade": 50, "tipo": "2D"})
        self.client.post("/salas/", json={"numero": 2, "capacidade": 60, "tipo": "3D"})

        response = self.client.get("/salas/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        numeros = [s["numero"] for s in data]
        self.assertIn(1, numeros)
        self.assertIn(2, numeros)

    def test_obter_sala_sucesso(self):
        self.client.post("/salas/", json={"numero": 5, "capacidade": 70, "tipo": "2D"})

        response = self.client.get("/salas/5")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["numero"], 5)
        self.assertEqual(data["capacidade"], 70)
        self.assertEqual(data["tipo"], "2D")

    def test_obter_sala_inexistente(self):
        response = self.client.get("/salas/999")
        self.assertEqual(response.status_code, 404)

    def test_editar_sala_sucesso(self):
        self.client.post("/salas/", json={"numero": 10, "capacidade": 80, "tipo": "3D"})

        response = self.client.put("/salas/10", json={"capacidade": 90, "tipo": "2D"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["capacidade"], 90)
        self.assertEqual(data["tipo"], "2D")

    def test_editar_sala_invalida(self):
        self.client.post("/salas/", json={"numero": 10, "capacidade": 80, "tipo": "3D"})

        # Capacidade inválida (não positiva -> erro 422 de validação de schema)
        response = self.client.put("/salas/10", json={"capacidade": -10, "tipo": "3D"})
        self.assertEqual(response.status_code, 422)

    def test_remover_sala_sucesso(self):
        self.client.post("/salas/", json={"numero": 10, "capacidade": 80, "tipo": "3D"})

        res_del = self.client.delete("/salas/10")
        self.assertEqual(res_del.status_code, 204)

        res_get = self.client.get("/salas/10")
        self.assertEqual(res_get.status_code, 404)

    def test_remover_sala_inexistente(self):
        response = self.client.delete("/salas/999")
        self.assertEqual(response.status_code, 404)
