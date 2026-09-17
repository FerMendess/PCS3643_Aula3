"""Automated unit and integration test suite for Cinema MVC application."""

import unittest

import cinema
from cinema import (
    cadastrar_filme,
    cadastrar_sala,
    cadastrar_sessao,
    cadastrar_valor_ingresso,
    comprarIngressos,
    listar_filmes_por_data,
)
from controller.buscaController import BuscaController
from controller.cadastraController import CadastraController
from controller.filme_controller import FilmeController
from controller.sala_controller import SalaController
from controller.sessao_controller import SessaoController
from controller.tipo_ingresso_controller import TipoIngressoController
from fastapi.testclient import TestClient

from app import app


def reiniciar_estado():
    cinema.filmes.clear()
    cinema.salas.clear()
    cinema.sessoes.clear()
    cinema.tipo_sala.clear()


class TestUS01CadastrarFilme(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()

    def test_cadastrar_filme_sucesso(self):
        filme = cadastrar_filme("Matrix", "21/05/1999", "21/08/1999", 136)
        self.assertIsNotNone(filme)
        self.assertEqual(filme.codigo, 1)
        self.assertEqual(filme.nome, "Matrix")
        self.assertEqual(filme.data_estreia, "21/05/1999")
        self.assertEqual(filme.data_saida, "21/08/1999")
        self.assertEqual(filme.duracao, 136)
        self.assertIn(filme, cinema.filmes)

    def test_cadastrar_multiplos_filmes_codigos_sequenciais(self):
        f1 = cadastrar_filme("Filme 1", "01/01/2026", "10/01/2026", 100)
        f2 = cadastrar_filme("Filme 2", "05/01/2026", "15/01/2026", 120)
        self.assertIsNotNone(f1)
        self.assertIsNotNone(f2)
        self.assertEqual(f1.codigo, 1)
        self.assertEqual(f2.codigo, 2)

    def test_cadastrar_filme_data_invalida(self):
        filme = cadastrar_filme("Matrix", "32/01/2026", "10/02/2026", 120)
        self.assertIsNone(filme)
        filme2 = cadastrar_filme("Matrix", "data_errada", "10/02/2026", 120)
        self.assertIsNone(filme2)

    def test_cadastrar_filme_saida_anterior_a_estreia(self):
        filme = cadastrar_filme("Matrix", "20/05/2026", "10/05/2026", 120)
        self.assertIsNone(filme)

    def test_cadastrar_filme_duracao_invalida(self):
        filme_zero = cadastrar_filme("Matrix", "01/01/2026", "10/01/2026", 0)
        self.assertIsNone(filme_zero)
        filme_neg = cadastrar_filme("Matrix", "01/01/2026", "10/01/2026", -90)
        self.assertIsNone(filme_neg)

    def test_cadastrar_filme_nome_invalido(self):
        filme = cadastrar_filme("", "01/01/2026", "10/01/2026", 100)
        self.assertIsNone(filme)
        filme_spaces = cadastrar_filme("   ", "01/01/2026", "10/01/2026", 100)
        self.assertIsNone(filme_spaces)

    def test_cadastrar_filme_nome_repetido(self):
        f1 = cadastrar_filme("Carros", "01/01/2010", "01/03/2010", 115)
        self.assertIsNotNone(f1)
        f2 = cadastrar_filme("Carros", "01/01/2010", "01/03/2010", 115)
        self.assertIsNone(f2)


class TestUS02CadastrarValorIngresso(unittest.TestCase):

    def setUp(self):
        reiniciar_estado()

    def test_cadastrar_valor_ingresso_2d_sucesso(self):
        resultado = cadastrar_valor_ingresso("2D", 30)
        self.assertTrue(resultado)
        self.assertEqual(cinema.tipo_sala["2D"], 30)

    def test_cadastrar_valor_ingresso_3d_sucesso(self):
        resultado = cadastrar_valor_ingresso("3D", 45)
        self.assertTrue(resultado)
        self.assertEqual(cinema.tipo_sala["3D"], 45)

    def test_cadastrar_valor_ingresso_tipo_invalido(self):
        self.assertFalse(cadastrar_valor_ingresso("4D", 50))
        self.assertFalse(cadastrar_valor_ingresso("IMAX", 60))
        self.assertFalse(cadastrar_valor_ingresso("", 30))
        self.assertFalse(cadastrar_valor_ingresso(None, 30))

    def test_cadastrar_valor_ingresso_valor_menor_ou_igual_a_zero(self):
        self.assertFalse(cadastrar_valor_ingresso("2D", 0))
        self.assertFalse(cadastrar_valor_ingresso("2D", -20))

    def test_cadastrar_valor_ingresso_valor_nao_inteiro(self):
        self.assertFalse(cadastrar_valor_ingresso("2D", 35.5))
        self.assertFalse(cadastrar_valor_ingresso("2D", "30"))


class TestUS03CadastrarSala(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()

    def test_cadastrar_sala_sucesso(self):
        sala = cadastrar_sala(1, 50, "2D")
        self.assertIsNotNone(sala)
        self.assertEqual(sala.numero, 1)
        self.assertEqual(sala.capacidade, 50)
        self.assertEqual(sala.tipo, "2D")
        self.assertIn(sala, cinema.salas)

    def test_cadastrar_sala_numero_repetido(self):
        s1 = cadastrar_sala(1, 50, "2D")
        self.assertIsNotNone(s1)
        s2 = cadastrar_sala(1, 60, "3D")
        self.assertIsNone(s2)
        self.assertEqual(len(cinema.salas), 1)

    def test_cadastrar_sala_numero_invalido(self):
        self.assertIsNone(cadastrar_sala(0, 50, "2D"))
        self.assertIsNone(cadastrar_sala(-1, 50, "2D"))

    def test_cadastrar_sala_capacidade_invalida(self):
        self.assertIsNone(cadastrar_sala(2, 0, "2D"))
        self.assertIsNone(cadastrar_sala(2, -10, "2D"))

    def test_cadastrar_sala_tipo_invalido(self):
        self.assertIsNone(cadastrar_sala(3, 50, "4D"))
        self.assertIsNone(cadastrar_sala(3, 50, ""))
        self.assertIsNone(cadastrar_sala(3, 50, None))


class TestUS04CadastrarSessao(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.sala = cadastrar_sala(1, 10, "2D")
        self.filme = cadastrar_filme("Inception", "01/06/2026", "30/06/2026", 148)

    def test_cadastrar_sessao_sucesso(self):
        sessao = cadastrar_sessao(1, 1, "15/06/2026", 20)
        self.assertIsNotNone(sessao)
        self.assertEqual(sessao.codigo, 1)
        self.assertEqual(sessao.sala, self.sala)
        self.assertEqual(sessao.filme, self.filme)
        self.assertEqual(sessao.data, "15/06/2026")
        self.assertEqual(sessao.hora_inicio, 20)
        self.assertEqual(len(sessao.assentos), 10)
        for num_assento in range(1, 11):
            self.assertEqual(sessao.assentos[num_assento], 0)
        self.assertIn(sessao, cinema.sessoes)

    def test_cadastrar_multiplas_sessoes_codigos_sequenciais(self):
        s1 = cadastrar_sessao(1, 1, "15/06/2026", 14)
        s2 = cadastrar_sessao(1, 1, "15/06/2026", 18)
        self.assertIsNotNone(s1)
        self.assertIsNotNone(s2)
        self.assertEqual(s1.codigo, 1)
        self.assertEqual(s2.codigo, 2)

    def test_cadastrar_sessao_sala_inexistente(self):
        sessao = cadastrar_sessao(99, 1, "15/06/2026", 20)
        self.assertIsNone(sessao)

    def test_cadastrar_sessao_filme_inexistente(self):
        sessao = cadastrar_sessao(1, 99, "15/06/2026", 20)
        self.assertIsNone(sessao)

    def test_cadastrar_sessao_conflito_horario_mesma_sala(self):
        s1 = cadastrar_sessao(1, 1, "15/06/2026", 20)
        self.assertIsNotNone(s1)
        s2 = cadastrar_sessao(1, 1, "15/06/2026", 20)
        self.assertIsNone(s2)

    def test_cadastrar_sessao_mesmo_horario_salas_diferentes(self):
        cadastrar_sala(2, 20, "3D")
        s1 = cadastrar_sessao(1, 1, "15/06/2026", 20)
        s2 = cadastrar_sessao(2, 1, "15/06/2026", 20)
        self.assertIsNotNone(s1)
        self.assertIsNotNone(s2)

    def test_cadastrar_sessao_hora_invalida(self):
        self.assertIsNone(cadastrar_sessao(1, 1, "15/06/2026", -1))
        self.assertIsNone(cadastrar_sessao(1, 1, "15/06/2026", 24))
        self.assertIsNone(cadastrar_sessao(1, 1, "15/06/2026", "20"))

    def test_cadastrar_sessao_assentos_quantidade(self):
        sessao = cadastrar_sessao(1, 1, "15/06/2026", 20)
        self.assertIsNotNone(sessao)
        self.assertEqual(cinema.pegar_sala(1).capacidade, len(sessao.assentos))

    def test_cadastrar_sessao_data_invalida(self):
        self.assertIsNone(cadastrar_sessao(1, 1, "32/06/2026", 20))
        self.assertIsNone(cadastrar_sessao(1, 1, "data_invalida", 20))


class TestUS05ListarFilmesPorData(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        cadastrar_valor_ingresso("2D", 40)
        cadastrar_valor_ingresso("3D", 50)
        self.sala1 = cadastrar_sala(1, 2, "3D")
        self.sala2 = cadastrar_sala(2, 5, "2D")
        self.filme1 = cadastrar_filme("King Kong", "01/06/2026", "30/06/2026", 120)
        self.filme2 = cadastrar_filme("Star Wars", "01/06/2026", "30/06/2026", 140)

    def test_listar_filmes_por_data_sucesso_uma_sessao(self):
        cadastrar_sessao(1, 1, "15/06/2026", 12)
        esperado = "1: King Kong, sala 1 (3D), 12h, 50 reais."
        self.assertEqual(listar_filmes_por_data("15/06/2026"), esperado)

    def test_listar_filmes_por_data_multiplas_sessoes(self):
        cadastrar_sessao(1, 1, "15/06/2026", 12)
        cadastrar_sessao(2, 2, "15/06/2026", 13)
        resultado = listar_filmes_por_data("15/06/2026")
        esperado = (
            "1: King Kong, sala 1 (3D), 12h, 50 reais.\n"
            "2: Star Wars, sala 2 (2D), 13h, 40 reais."
        )
        self.assertEqual(resultado, esperado)

    def test_listar_filmes_por_data_sessao_sem_assentos_disponiveis(self):
        sessao = cadastrar_sessao(1, 1, "15/06/2026", 12)
        # Ocupa todos os assentos (capacidade = 2)
        sessao.assentos[1] = 1
        sessao.assentos[2] = 1
        resultado = listar_filmes_por_data("15/06/2026")
        self.assertEqual(resultado, "Nenhum filme no dia escolhido.")

    def test_listar_filmes_por_data_dia_sem_sessoes(self):
        cadastrar_sessao(1, 1, "15/06/2026", 12)
        resultado = listar_filmes_por_data("20/06/2026")
        self.assertEqual(resultado, "Nenhum filme no dia escolhido.")

    def test_listar_filmes_por_data_data_invalida(self):
        self.assertEqual(listar_filmes_por_data("32/06/2026"), "Data invalida.")
        self.assertEqual(listar_filmes_por_data("data_errada"), "Data invalida.")
        self.assertEqual(listar_filmes_por_data(None), "Data invalida.")


class TestUS06ComprarIngressos(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        cadastrar_valor_ingresso("2D", 40)
        self.sala = cadastrar_sala(1, 5, "2D")
        self.filme = cadastrar_filme("Interestelar", "01/06/2026", "30/06/2026", 169)
        self.sessao = cadastrar_sessao(1, 1, "15/06/2026", 19)

    def test_comprar_ingressos_sucesso_inteira(self):
        total = comprarIngressos(1, [1], [0])
        self.assertEqual(total, 40)
        self.assertEqual(self.sessao.assentos[1], 1)

    def test_comprar_ingressos_sucesso_meia(self):
        total = comprarIngressos(1, [2], [1])
        self.assertEqual(total, 20)
        self.assertEqual(self.sessao.assentos[2], 1)

    def test_comprar_ingressos_sucesso_multiplos_misto(self):
        total = comprarIngressos(1, [1, 2], [0, 1])
        self.assertEqual(total, 60)
        self.assertEqual(self.sessao.assentos[1], 1)
        self.assertEqual(self.sessao.assentos[2], 1)

    def test_comprar_ingressos_sessao_inexistente(self):
        total = comprarIngressos(99, [1], [0])
        self.assertEqual(total, 0)
        self.assertEqual(self.sessao.assentos[1], 0)

    def test_comprar_ingressos_assento_ja_ocupado_atomicidade(self):
        self.sessao.assentos[1] = 1

        total = comprarIngressos(1, [1, 2], [0, 0])
        self.assertEqual(total, 0)
        self.assertEqual(self.sessao.assentos[1], 1)
        self.assertEqual(self.sessao.assentos[2], 0)

    def test_comprar_ingressos_assento_inexistente(self):
        total = comprarIngressos(1, [99], [0])
        self.assertEqual(total, 0)

        total_zero = comprarIngressos(1, [0], [0])
        self.assertEqual(total_zero, 0)

    def test_comprar_ingressos_assentos_duplicados(self):
        total = comprarIngressos(1, [1, 1], [0, 0])
        self.assertEqual(total, 0)
        self.assertEqual(self.sessao.assentos[1], 0)

    def test_comprar_ingressos_tamanhos_diferentes(self):
        total = comprarIngressos(1, [1, 2], [0])
        self.assertEqual(total, 0)
        self.assertEqual(self.sessao.assentos[1], 0)
        self.assertEqual(self.sessao.assentos[2], 0)

    def test_comprar_ingressos_lista_vazia(self):
        total = comprarIngressos(1, [], [])
        self.assertEqual(total, 0)

    def test_comprar_ingressos_tipo_invalido(self):
        total = comprarIngressos(1, [1], [2])
        self.assertEqual(total, 0)
        self.assertEqual(self.sessao.assentos[1], 0)


class TestMVCControllers(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.filme_ctrl = FilmeController()
        self.sala_ctrl = SalaController()
        self.tipo_ingresso_ctrl = TipoIngressoController()
        self.sessao_ctrl = SessaoController()
        self.cadastra_ctrl = CadastraController()
        self.busca_ctrl = BuscaController()

    def test_filme_crud_completo(self):
        filme = self.filme_ctrl.cadastrar_filme("Interestelar", "10/10/2026", "20/10/2026", 169)
        self.assertIsNotNone(filme)
        self.assertEqual(filme.nome, "Interestelar")

        buscado = self.busca_ctrl.pegar_filme(filme.codigo)
        self.assertIsNotNone(buscado)
        self.assertEqual(buscado.nome, "Interestelar")

        editado = self.filme_ctrl.editar_filme(filme.codigo, nome="Interestelar IMAX", duracao=175)
        self.assertIsNotNone(editado)
        self.assertEqual(editado.nome, "Interestelar IMAX")
        self.assertEqual(editado.duracao, 175)

        lista = self.filme_ctrl.listar_filmes()
        self.assertEqual(len(lista), 1)

        removido = self.filme_ctrl.remover_filme(filme.codigo)
        self.assertTrue(removido)
        self.assertIsNone(self.filme_ctrl.buscar_filme(filme.codigo))

    def test_sala_crud_completo(self):
        sala = self.cadastra_ctrl.cadastrar_sala(5, 60, "3D")
        self.assertIsNotNone(sala)
        self.assertEqual(sala.numero, 5)

        buscada = self.sala_ctrl.buscar_sala(5)
        self.assertIsNotNone(buscada)
        self.assertEqual(buscada.capacidade, 60)

        editada = self.sala_ctrl.editar_sala(5, capacidade=75, tipo="2D")
        self.assertIsNotNone(editada)
        self.assertEqual(editada.capacidade, 75)
        self.assertEqual(editada.tipo, "2D")

        lista = self.busca_ctrl.listar_salas()
        self.assertEqual(len(lista), 1)

        removida = self.sala_ctrl.remover_sala(5)
        self.assertTrue(removida)
        self.assertIsNone(self.sala_ctrl.buscar_sala(5))

    def test_tipo_ingresso_crud_completo(self):
        cadastrado = self.tipo_ingresso_ctrl.cadastrar_tipo_ingresso("2D", 35)
        self.assertTrue(cadastrado)

        buscado = self.tipo_ingresso_ctrl.buscar_tipo_ingresso("2D")
        self.assertIsNotNone(buscado)
        self.assertEqual(buscado.valor, 35)

        editado = self.tipo_ingresso_ctrl.editar_tipo_ingresso("2D", 40)
        self.assertIsNotNone(editado)
        self.assertEqual(editado.valor, 40)

        lista = self.tipo_ingresso_ctrl.listar_tipos_ingresso()
        self.assertEqual(len(lista), 1)

        removido = self.tipo_ingresso_ctrl.remover_tipo_ingresso("2D")
        self.assertTrue(removido)
        self.assertIsNone(self.tipo_ingresso_ctrl.buscar_tipo_ingresso("2D"))

    def test_sessao_crud_completo(self):
        sala = self.sala_ctrl.cadastrar_sala(1, 10, "2D")
        filme = self.filme_ctrl.cadastrar_filme("Duna", "01/01/2026", "20/01/2026", 155)
        sessao = self.sessao_ctrl.cadastrar_sessao(sala.numero, filme.codigo, "05/01/2026", 18)
        self.assertIsNotNone(sessao)

        buscada = self.sessao_ctrl.buscar_sessao(sessao.codigo)
        self.assertIsNotNone(buscada)
        self.assertEqual(buscada.hora_inicio, 18)

        editada = self.sessao_ctrl.editar_sessao(sessao.codigo, hora_inicio=21)
        self.assertIsNotNone(editada)
        self.assertEqual(editada.hora_inicio, 21)

        lista = self.sessao_ctrl.listar_sessoes()
        self.assertEqual(len(lista), 1)

        removida = self.sessao_ctrl.remover_sessao(sessao.codigo)
        self.assertTrue(removida)
        self.assertIsNone(self.sessao_ctrl.buscar_sessao(sessao.codigo))


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
        res_post = self.client.post("/tipos-ingresso/", json={"tipo": "2D", "valor": 30})
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