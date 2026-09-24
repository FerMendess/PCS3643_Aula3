"""Integration tests for TipoIngresso REST API endpoints."""

import unittest

from fastapi.testclient import TestClient

from app import app
from tests.helpers import reiniciar_estado


class TestTipoIngressoView(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.client = TestClient(app)

    def test_cadastrar_tipo_ingresso_sucesso(self):
        response = self.client.post(
            "/tipos-ingresso/", json={"tipo": "2D", "valor": 30}
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["tipo"], "2D")
        self.assertEqual(data["valor"], 30)

    def test_cadastrar_tipo_ingresso_invalido(self):
        # Tipo de sala não suportado pelo controller ("4D")
        response = self.client.post(
            "/tipos-ingresso/", json={"tipo": "4D", "valor": 30}
        )
        self.assertEqual(response.status_code, 400)

    def test_cadastrar_tipo_ingresso_valor_negativo(self):
        # Valor negativo viola validação de schema (gt=0)
        response = self.client.post(
            "/tipos-ingresso/", json={"tipo": "2D", "valor": -5}
        )
        self.assertEqual(response.status_code, 422)

    def test_listar_tipos_ingresso(self):
        self.client.post("/tipos-ingresso/", json={"tipo": "2D", "valor": 30})
        self.client.post("/tipos-ingresso/", json={"tipo": "3D", "valor": 45})

        response = self.client.get("/tipos-ingresso/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        tipos = [item["tipo"] for item in data]
        self.assertIn("2D", tipos)
        self.assertIn("3D", tipos)

    def test_obter_tipo_ingresso_sucesso(self):
        self.client.post("/tipos-ingresso/", json={"tipo": "2D", "valor": 30})

        response = self.client.get("/tipos-ingresso/2D")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["valor"], 30)

    def test_obter_tipo_ingresso_inexistente(self):
        response = self.client.get("/tipos-ingresso/IMAX")
        self.assertEqual(response.status_code, 404)

    def test_editar_tipo_ingresso_sucesso(self):
        self.client.post("/tipos-ingresso/", json={"tipo": "2D", "valor": 30})

        response = self.client.put("/tipos-ingresso/2D", json={"valor": 35})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["valor"], 35)

    def test_editar_tipo_ingresso_inexistente(self):
        response = self.client.put("/tipos-ingresso/IMAX", json={"valor": 50})
        self.assertEqual(response.status_code, 404)

    def test_remover_tipo_ingresso_sucesso(self):
        self.client.post("/tipos-ingresso/", json={"tipo": "2D", "valor": 30})

        res_del = self.client.delete("/tipos-ingresso/2D")
        self.assertEqual(res_del.status_code, 204)

        res_get = self.client.get("/tipos-ingresso/2D")
        self.assertEqual(res_get.status_code, 404)

    def test_remover_tipo_ingresso_inexistente(self):
        response = self.client.delete("/tipos-ingresso/IMAX")
        self.assertEqual(response.status_code, 404)
