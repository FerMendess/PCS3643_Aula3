"""Integration tests for Sala REST API endpoints."""

import unittest

from fastapi.testclient import TestClient

from app import app
from tests.helpers import reiniciar_estado


class TestSalaView(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.client = TestClient(app)

    def test_api_salas_crud(self):
        payload = {"numero": 10, "capacidade": 80, "tipo": "3D"}
        res_post = self.client.post("/salas/", json=payload)
        self.assertEqual(res_post.status_code, 201)
        self.assertEqual(res_post.json()["numero"], 10)

        res_dup = self.client.post("/salas/", json=payload)
        self.assertEqual(res_dup.status_code, 400)

        res_list = self.client.get("/salas/")
        self.assertEqual(res_list.status_code, 200)
        self.assertEqual(len(res_list.json()), 1)

        res_get = self.client.get("/salas/10")
        self.assertEqual(res_get.status_code, 200)

        res_get_404 = self.client.get("/salas/999")
        self.assertEqual(res_get_404.status_code, 404)

        res_put = self.client.put("/salas/10", json={"capacidade": 90, "tipo": "2D"})
        self.assertEqual(res_put.status_code, 200)
        self.assertEqual(res_put.json()["capacidade"], 90)
        self.assertEqual(res_put.json()["tipo"], "2D")

        res_del = self.client.delete("/salas/10")
        self.assertEqual(res_del.status_code, 204)

        res_del_404 = self.client.delete("/salas/10")
        self.assertEqual(res_del_404.status_code, 404)
