"""Integration tests for View layer and FastAPI REST API endpoints."""

import unittest

from fastapi.testclient import TestClient

import cinema
from app import app


def reiniciar_estado():
    cinema.filmes.clear()
    cinema.salas.clear()
    cinema.sessoes.clear()
    cinema.tipo_sala.clear()


class TestFastAPIRestAPI(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.client = TestClient(app)

    def test_root_and_docs_endpoints(self):
        resp_root = self.client.get("/")
        self.assertEqual(resp_root.status_code, 200)
        self.assertEqual(resp_root.json()["status"], "online")
        self.assertEqual(resp_root.json()["arquitetura"], "MVC (Model-View-Controller)")

        resp_openapi = self.client.get("/openapi.json")
        self.assertEqual(resp_openapi.status_code, 200)

        resp_docs = self.client.get("/docs")
        self.assertEqual(resp_docs.status_code, 200)

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
