"""Integration tests for Filme REST API endpoints."""

import unittest

from fastapi.testclient import TestClient

from app import app
from tests.helpers import reiniciar_estado


class TestFilmeView(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.client = TestClient(app)

    def test_cadastrar_filme_sucesso(self):
        payload = {
            "nome": "O Poderoso Chefão",
            "data_estreia": "10/05/2026",
            "data_saida": "10/08/2026",
            "duracao": 175,
        }
        response = self.client.post("/filmes/", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["nome"], "O Poderoso Chefão")
        self.assertIn("codigo", data)

    def test_cadastrar_filme_duplicado_ou_invalido(self):
        payload = {
            "nome": "O Poderoso Chefão",
            "data_estreia": "10/05/2026",
            "data_saida": "10/08/2026",
            "duracao": 175,
        }
        res_first = self.client.post("/filmes/", json=payload)
        self.assertEqual(res_first.status_code, 201)

        res_dup = self.client.post("/filmes/", json=payload)
        self.assertEqual(res_dup.status_code, 400)

    def test_listar_filmes(self):
        payload = {
            "nome": "Interestelar",
            "data_estreia": "01/06/2026",
            "data_saida": "01/09/2026",
            "duracao": 169,
        }
        self.client.post("/filmes/", json=payload)
        response = self.client.get("/filmes/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["nome"], "Interestelar")

    def test_obter_filme_sucesso(self):
        payload = {
            "nome": "Matrix",
            "data_estreia": "15/05/2026",
            "data_saida": "15/08/2026",
            "duracao": 136,
        }
        res_post = self.client.post("/filmes/", json=payload)
        codigo = res_post.json()["codigo"]

        response = self.client.get(f"/filmes/{codigo}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["duracao"], 136)

    def test_obter_filme_inexistente(self):
        response = self.client.get("/filmes/9999")
        self.assertEqual(response.status_code, 404)

    def test_editar_filme_sucesso(self):
        payload = {
            "nome": "Inception",
            "data_estreia": "10/06/2026",
            "data_saida": "10/09/2026",
            "duracao": 148,
        }
        res_post = self.client.post("/filmes/", json=payload)
        codigo = res_post.json()["codigo"]

        response = self.client.put(f"/filmes/{codigo}", json={"duracao": 150})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["duracao"], 150)

    def test_editar_filme_invalido(self):
        payload = {
            "nome": "Gladiador",
            "data_estreia": "10/06/2026",
            "data_saida": "10/09/2026",
            "duracao": 155,
        }
        res_post = self.client.post("/filmes/", json=payload)
        codigo = res_post.json()["codigo"]

        response = self.client.put(
            f"/filmes/{codigo}", json={"data_saida": "01/01/2026"}
        )
        self.assertEqual(response.status_code, 400)

    def test_remover_filme_sucesso(self):
        payload = {
            "nome": "Avatar",
            "data_estreia": "10/06/2026",
            "data_saida": "10/09/2026",
            "duracao": 162,
        }
        res_post = self.client.post("/filmes/", json=payload)
        codigo = res_post.json()["codigo"]

        res_del = self.client.delete(f"/filmes/{codigo}")
        self.assertEqual(res_del.status_code, 204)

        res_get = self.client.get(f"/filmes/{codigo}")
        self.assertEqual(res_get.status_code, 404)

    def test_remover_filme_inexistente(self):
        response = self.client.delete("/filmes/9999")
        self.assertEqual(response.status_code, 404)
