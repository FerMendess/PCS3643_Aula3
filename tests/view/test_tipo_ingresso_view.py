"""Integration tests for TipoIngresso REST API endpoints."""

import unittest

from fastapi.testclient import TestClient

from app import app
from tests.helpers import reiniciar_estado


class TestTipoIngressoView(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.client = TestClient(app)

    def test_api_tipos_ingresso_crud(self):
        res_post = self.client.post(
            "/tipos-ingresso/", json={"tipo": "2D", "valor": 30}
        )
        self.assertEqual(res_post.status_code, 201)
        self.assertEqual(res_post.json()["valor"], 30)

        res_list = self.client.get("/tipos-ingresso/")
        self.assertEqual(res_list.status_code, 200)
        self.assertEqual(len(res_list.json()), 1)

        res_get = self.client.get("/tipos-ingresso/2D")
        self.assertEqual(res_get.status_code, 200)

        res_get_404 = self.client.get("/tipos-ingresso/4D")
        self.assertEqual(res_get_404.status_code, 404)

        res_put = self.client.put("/tipos-ingresso/2D", json={"valor": 35})
        self.assertEqual(res_put.status_code, 200)
        self.assertEqual(res_put.json()["valor"], 35)

        res_del = self.client.delete("/tipos-ingresso/2D")
        self.assertEqual(res_del.status_code, 204)

        res_del_404 = self.client.delete("/tipos-ingresso/2D")
        self.assertEqual(res_del_404.status_code, 404)
