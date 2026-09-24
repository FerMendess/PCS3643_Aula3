"""Integration tests for Sessao REST API and ticket purchase endpoints."""

import unittest

from fastapi.testclient import TestClient

from app import app
from tests.helpers import reiniciar_estado


class TestSessaoView(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.client = TestClient(app)

    def _setup_base(self) -> tuple[int, int]:
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
        return res_filme.json()["codigo"], 1

    def test_cadastrar_sessao_sucesso(self):
        cod_filme, num_sala = self._setup_base()
        response = self.client.post(
            "/sessoes/",
            json={
                "numero_sala": num_sala,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["numero_sala"], num_sala)
        self.assertEqual(data["codigo_filme"], cod_filme)
        self.assertEqual(len(data["assentos"]), 4)

    def test_cadastrar_sessao_filme_ou_sala_inexistente(self):
        cod_filme, _ = self._setup_base()
        response = self.client.post(
            "/sessoes/",
            json={
                "numero_sala": 999,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_cadastrar_sessao_conflito_horario(self):
        cod_filme, num_sala = self._setup_base()
        res1 = self.client.post(
            "/sessoes/",
            json={
                "numero_sala": num_sala,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )
        self.assertEqual(res1.status_code, 201)

        # Choque de horário na mesma sala e mesma data/hora
        res2 = self.client.post(
            "/sessoes/",
            json={
                "numero_sala": num_sala,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )
        self.assertEqual(res2.status_code, 400)

    def test_listar_sessoes(self):
        cod_filme, num_sala = self._setup_base()
        self.client.post(
            "/sessoes/",
            json={
                "numero_sala": num_sala,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )

        response = self.client.get("/sessoes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_obter_sessao_sucesso(self):
        cod_filme, num_sala = self._setup_base()
        res_post = self.client.post(
            "/sessoes/",
            json={
                "numero_sala": num_sala,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )
        cod_sessao = res_post.json()["codigo"]

        response = self.client.get(f"/sessoes/{cod_sessao}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["codigo"], cod_sessao)
        self.assertEqual(data["hora_inicio"], 20)

    def test_obter_sessao_inexistente(self):
        response = self.client.get("/sessoes/999")
        self.assertEqual(response.status_code, 404)

    def test_editar_sessao_sucesso(self):
        cod_filme, num_sala = self._setup_base()
        self.client.post("/salas/", json={"numero": 2, "capacidade": 6, "tipo": "2D"})

        res_post = self.client.post(
            "/sessoes/",
            json={
                "numero_sala": num_sala,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )
        cod_sessao = res_post.json()["codigo"]

        response = self.client.put(
            f"/sessoes/{cod_sessao}",
            json={"numero_sala": 2, "hora_inicio": 18},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["numero_sala"], 2)
        self.assertEqual(data["hora_inicio"], 18)

    def test_editar_sessao_invalida(self):
        cod_filme, num_sala = self._setup_base()
        res_post = self.client.post(
            "/sessoes/",
            json={
                "numero_sala": num_sala,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )
        cod_sessao = res_post.json()["codigo"]

        # Sala inexistente
        response = self.client.put(
            f"/sessoes/{cod_sessao}",
            json={"numero_sala": 999},
        )
        self.assertEqual(response.status_code, 400)

    def test_remover_sessao_sucesso(self):
        cod_filme, num_sala = self._setup_base()
        res_post = self.client.post(
            "/sessoes/",
            json={
                "numero_sala": num_sala,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )
        cod_sessao = res_post.json()["codigo"]

        res_del = self.client.delete(f"/sessoes/{cod_sessao}")
        self.assertEqual(res_del.status_code, 204)

        res_get = self.client.get(f"/sessoes/{cod_sessao}")
        self.assertEqual(res_get.status_code, 404)

    def test_remover_sessao_inexistente(self):
        response = self.client.delete("/sessoes/999")
        self.assertEqual(response.status_code, 404)

    def test_listar_sessoes_por_data(self):
        cod_filme, num_sala = self._setup_base()
        self.client.post(
            "/sessoes/",
            json={
                "numero_sala": num_sala,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )

        response = self.client.get("/sessoes/data/15/11/2026")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertIn("Gladiador II", data[0]["descricao"])

    def test_comprar_ingressos_endpoint_sucesso(self):
        cod_filme, num_sala = self._setup_base()
        res_post = self.client.post(
            "/sessoes/",
            json={
                "numero_sala": num_sala,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )
        cod_sessao = res_post.json()["codigo"]

        response = self.client.post(
            f"/sessoes/{cod_sessao}/comprar",
            json={"assentos": [1, 2], "tipos_ingresso": [0, 1]},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total"], 60)
        self.assertEqual(data["assentos_comprados"], [1, 2])

    def test_comprar_ingressos_endpoint_assento_ocupado(self):
        cod_filme, num_sala = self._setup_base()
        res_post = self.client.post(
            "/sessoes/",
            json={
                "numero_sala": num_sala,
                "codigo_filme": cod_filme,
                "data": "15/11/2026",
                "hora_inicio": 20,
            },
        )
        cod_sessao = res_post.json()["codigo"]

        res1 = self.client.post(
            f"/sessoes/{cod_sessao}/comprar",
            json={"assentos": [1], "tipos_ingresso": [0]},
        )
        self.assertEqual(res1.status_code, 200)

        # Tentativa de comprar o mesmo assento novamente
        res2 = self.client.post(
            f"/sessoes/{cod_sessao}/comprar",
            json={"assentos": [1], "tipos_ingresso": [0]},
        )
        self.assertEqual(res2.status_code, 400)
