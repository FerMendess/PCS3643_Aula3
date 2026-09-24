"""Integration tests for Filme REST API endpoints."""

import unittest

from fastapi.testclient import TestClient

from app import app
from tests.helpers import reiniciar_estado


class TestFilmeView(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.client = TestClient(app)

    def test_api_filmes_crud(self):
        payload = {
            "nome": "O Poderoso Chefão",
            "data_estreia": "10/05/2026",
            "data_saida": "10/08/2026",
            "duracao": 175,
        }
        res_post = self.client.post("/filmes/", json=payload)
        self.assertEqual(res_post.status_code, 201)
        codigo = res_post.json()["codigo"]
        self.assertEqual(res_post.json()["nome"], "O Poderoso Chefão")

        res_dup = self.client.post("/filmes/", json=payload)
        self.assertEqual(res_dup.status_code, 400)

        res_list = self.client.get("/filmes/")
        self.assertEqual(res_list.status_code, 200)
        self.assertEqual(len(res_list.json()), 1)

        res_get = self.client.get(f"/filmes/{codigo}")
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_get.json()["duracao"], 175)

        res_get_404 = self.client.get("/filmes/9999")
        self.assertEqual(res_get_404.status_code, 404)

        res_put = self.client.put(f"/filmes/{codigo}", json={"duracao": 180})
        self.assertEqual(res_put.status_code, 200)
        self.assertEqual(res_put.json()["duracao"], 180)

        res_del = self.client.delete(f"/filmes/{codigo}")
        self.assertEqual(res_del.status_code, 204)

        res_del_404 = self.client.delete(f"/filmes/{codigo}")
        self.assertEqual(res_del_404.status_code, 404)
