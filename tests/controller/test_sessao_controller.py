"""Unit tests for SessaoController and session, listing, and ticket purchase business rules."""

import unittest

from src.controller.filme_controller import FilmeController
from src.controller.sala_controller import SalaController
from src.controller.sessao_controller import SessaoController
from src.controller.tipo_ingresso_controller import TipoIngressoController
from tests.helpers import reiniciar_estado


class TestCadastrarSessao(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.sala_ctrl = SalaController()
        self.filme_ctrl = FilmeController()
        self.sessao_ctrl = SessaoController()
        self.sala = self.sala_ctrl.cadastrar_sala(1, 10, "2D")
        self.filme = self.filme_ctrl.cadastrar_filme(
            "Inception", "01/06/2026", "30/06/2026", 148
        )

    def test_cadastrar_sessao_sucesso(self):
        sessao = self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 20)
        self.assertIsNotNone(sessao)
        assert sessao is not None
        self.assertEqual(sessao.codigo, 1)
        self.assertEqual(sessao.sala, self.sala)
        self.assertEqual(sessao.filme, self.filme)
        self.assertEqual(sessao.data, "15/06/2026")
        self.assertEqual(sessao.hora_inicio, 20)
        self.assertEqual(len(sessao.assentos), 10)
        for num_assento in range(1, 11):
            self.assertEqual(sessao.assentos[num_assento], 0)
        buscada = self.sessao_ctrl.buscar_sessao(sessao.codigo)
        self.assertIsNotNone(buscada)

    def test_cadastrar_multiplas_sessoes_codigos_sequenciais(self):
        s1 = self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 14)
        s2 = self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 18)
        self.assertIsNotNone(s1)
        self.assertIsNotNone(s2)
        assert s1 is not None and s2 is not None
        self.assertEqual(s1.codigo, 1)
        self.assertEqual(s2.codigo, 2)

    def test_cadastrar_sessao_sala_inexistente(self):
        sessao = self.sessao_ctrl.cadastrar_sessao(99, 1, "15/06/2026", 20)
        self.assertIsNone(sessao)

    def test_cadastrar_sessao_filme_inexistente(self):
        sessao = self.sessao_ctrl.cadastrar_sessao(1, 99, "15/06/2026", 20)
        self.assertIsNone(sessao)

    def test_cadastrar_sessao_conflito_horario_mesma_sala(self):
        s1 = self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 20)
        self.assertIsNotNone(s1)
        s2 = self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 20)
        self.assertIsNone(s2)

    def test_cadastrar_sessao_mesmo_horario_salas_diferentes(self):
        self.sala_ctrl.cadastrar_sala(2, 20, "3D")
        s1 = self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 20)
        s2 = self.sessao_ctrl.cadastrar_sessao(2, 1, "15/06/2026", 20)
        self.assertIsNotNone(s1)
        self.assertIsNotNone(s2)

    def test_cadastrar_sessao_hora_invalida(self):
        self.assertIsNone(self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", -1))
        self.assertIsNone(self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 24))
        self.assertIsNone(self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", "20"))  # type: ignore[arg-type]

    def test_cadastrar_sessao_assentos_quantidade(self):
        sessao = self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 20)
        self.assertIsNotNone(sessao)
        sala = self.sala_ctrl.buscar_sala(1)
        assert sala is not None
        self.assertEqual(sala.capacidade, len(sessao.assentos))  # type: ignore[union-attr]

    def test_cadastrar_sessao_data_invalida(self):
        self.assertIsNone(self.sessao_ctrl.cadastrar_sessao(1, 1, "32/06/2026", 20))
        self.assertIsNone(self.sessao_ctrl.cadastrar_sessao(1, 1, "data_invalida", 20))


class TestListarFilmesPorData(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.tipo_ctrl = TipoIngressoController()
        self.sala_ctrl = SalaController()
        self.filme_ctrl = FilmeController()
        self.sessao_ctrl = SessaoController()
        self.tipo_ctrl.cadastrar_tipo_ingresso("2D", 40)
        self.tipo_ctrl.cadastrar_tipo_ingresso("3D", 50)
        self.sala1 = self.sala_ctrl.cadastrar_sala(1, 2, "3D")
        self.sala2 = self.sala_ctrl.cadastrar_sala(2, 5, "2D")
        self.filme1 = self.filme_ctrl.cadastrar_filme(
            "King Kong", "01/06/2026", "30/06/2026", 120
        )
        self.filme2 = self.filme_ctrl.cadastrar_filme(
            "Star Wars", "01/06/2026", "30/06/2026", 140
        )

    def test_listar_filmes_por_data_sucesso_uma_sessao(self):
        self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 12)
        esperado = "1: King Kong, sala 1 (3D), 12h, 50 reais."
        self.assertEqual(
            self.sessao_ctrl.listar_filmes_por_data("15/06/2026"), esperado
        )

    def test_listar_filmes_por_data_multiplas_sessoes(self):
        self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 12)
        self.sessao_ctrl.cadastrar_sessao(2, 2, "15/06/2026", 13)
        resultado = self.sessao_ctrl.listar_filmes_por_data("15/06/2026")
        esperado = (
            "1: King Kong, sala 1 (3D), 12h, 50 reais.\n"
            "2: Star Wars, sala 2 (2D), 13h, 40 reais."
        )
        self.assertEqual(resultado, esperado)

    def test_listar_filmes_por_data_sessao_sem_assentos_disponiveis(self):
        sessao = self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 12)
        assert sessao is not None
        sessao.assentos[1] = 1
        sessao.assentos[2] = 1
        resultado = self.sessao_ctrl.listar_filmes_por_data("15/06/2026")
        self.assertEqual(resultado, "Nenhum filme no dia escolhido.")

    def test_listar_filmes_por_data_dia_sem_sessoes(self):
        self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 12)
        resultado = self.sessao_ctrl.listar_filmes_por_data("20/06/2026")
        self.assertEqual(resultado, "Nenhum filme no dia escolhido.")

    def test_listar_filmes_por_data_data_invalida(self):
        self.assertEqual(
            self.sessao_ctrl.listar_filmes_por_data("32/06/2026"), "Data invalida."
        )
        self.assertEqual(
            self.sessao_ctrl.listar_filmes_por_data("data_errada"), "Data invalida."
        )
        self.assertEqual(
            self.sessao_ctrl.listar_filmes_por_data(None), "Data invalida."
        )  # type: ignore[arg-type]


class TestComprarIngressos(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.tipo_ctrl = TipoIngressoController()
        self.sala_ctrl = SalaController()
        self.filme_ctrl = FilmeController()
        self.sessao_ctrl = SessaoController()
        self.tipo_ctrl.cadastrar_tipo_ingresso("2D", 40)
        self.sala = self.sala_ctrl.cadastrar_sala(1, 5, "2D")
        self.filme = self.filme_ctrl.cadastrar_filme(
            "Interestelar", "01/06/2026", "30/06/2026", 169
        )
        self.sessao = self.sessao_ctrl.cadastrar_sessao(1, 1, "15/06/2026", 19)

    def test_comprar_ingressos_sucesso_inteira(self):
        total = self.sessao_ctrl.comprar_ingressos(1, [1], [0])
        self.assertEqual(total, 40)
        sessao_atual = self.sessao_ctrl.buscar_sessao(1)
        assert sessao_atual is not None
        self.assertEqual(sessao_atual.assentos[1], 1)

    def test_comprar_ingressos_sucesso_meia(self):
        total = self.sessao_ctrl.comprar_ingressos(1, [2], [1])
        self.assertEqual(total, 20)
        sessao_atual = self.sessao_ctrl.buscar_sessao(1)
        assert sessao_atual is not None
        self.assertEqual(sessao_atual.assentos[2], 1)

    def test_comprar_ingressos_sucesso_multiplos_misto(self):
        total = self.sessao_ctrl.comprar_ingressos(1, [1, 2], [0, 1])
        self.assertEqual(total, 60)
        sessao_atual = self.sessao_ctrl.buscar_sessao(1)
        assert sessao_atual is not None
        self.assertEqual(sessao_atual.assentos[1], 1)
        self.assertEqual(sessao_atual.assentos[2], 1)

    def test_comprar_ingressos_sessao_inexistente(self):
        total = self.sessao_ctrl.comprar_ingressos(99, [1], [0])
        self.assertEqual(total, 0)
        sessao_atual = self.sessao_ctrl.buscar_sessao(1)
        assert sessao_atual is not None
        self.assertEqual(sessao_atual.assentos[1], 0)

    def test_comprar_ingressos_assento_ja_ocupado_atomicidade(self):
        assert self.sessao is not None
        self.sessao.assentos[1] = 1

        total = self.sessao_ctrl.comprar_ingressos(1, [1, 2], [0, 0])
        self.assertEqual(total, 0)
        sessao_atual = self.sessao_ctrl.buscar_sessao(1)
        assert sessao_atual is not None
        self.assertEqual(sessao_atual.assentos[1], 1)
        self.assertEqual(sessao_atual.assentos[2], 0)

    def test_comprar_ingressos_assento_inexistente(self):
        total = self.sessao_ctrl.comprar_ingressos(1, [99], [0])
        self.assertEqual(total, 0)

        total_zero = self.sessao_ctrl.comprar_ingressos(1, [0], [0])
        self.assertEqual(total_zero, 0)

    def test_comprar_ingressos_assentos_duplicados(self):
        total = self.sessao_ctrl.comprar_ingressos(1, [1, 1], [0, 0])
        self.assertEqual(total, 0)
        sessao_atual = self.sessao_ctrl.buscar_sessao(1)
        assert sessao_atual is not None
        self.assertEqual(sessao_atual.assentos[1], 0)

    def test_comprar_ingressos_tamanhos_diferentes(self):
        total = self.sessao_ctrl.comprar_ingressos(1, [1, 2], [0])
        self.assertEqual(total, 0)
        sessao_atual = self.sessao_ctrl.buscar_sessao(1)
        assert sessao_atual is not None
        self.assertEqual(sessao_atual.assentos[1], 0)
        self.assertEqual(sessao_atual.assentos[2], 0)

    def test_comprar_ingressos_lista_vazia(self):
        total = self.sessao_ctrl.comprar_ingressos(1, [], [])
        self.assertEqual(total, 0)

    def test_comprar_ingressos_tipo_invalido(self):
        total = self.sessao_ctrl.comprar_ingressos(1, [1], [2])
        self.assertEqual(total, 0)
        sessao_atual = self.sessao_ctrl.buscar_sessao(1)
        assert sessao_atual is not None
        self.assertEqual(sessao_atual.assentos[1], 0)


class TestSessaoControllerCRUD(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.filme_ctrl = FilmeController()
        self.sala_ctrl = SalaController()
        self.sessao_ctrl = SessaoController()

    def test_sessao_crud_completo(self):
        sala = self.sala_ctrl.cadastrar_sala(1, 10, "2D")
        filme = self.filme_ctrl.cadastrar_filme("Duna", "01/01/2026", "20/01/2026", 155)
        assert sala is not None and filme is not None
        assert sala.numero is not None and filme.codigo is not None
        sessao = self.sessao_ctrl.cadastrar_sessao(
            sala.numero, filme.codigo, "05/01/2026", 18
        )
        self.assertIsNotNone(sessao)
        assert sessao is not None and sessao.codigo is not None

        buscada = self.sessao_ctrl.buscar_sessao(sessao.codigo)
        self.assertIsNotNone(buscada)
        assert buscada is not None
        self.assertEqual(buscada.hora_inicio, 18)

        editada = self.sessao_ctrl.editar_sessao(sessao.codigo, hora_inicio=21)
        self.assertIsNotNone(editada)
        assert editada is not None
        self.assertEqual(editada.hora_inicio, 21)

        lista = self.sessao_ctrl.listar_sessoes()
        self.assertEqual(len(lista), 1)

        removida = self.sessao_ctrl.remover_sessao(sessao.codigo)
        self.assertTrue(removida)
        self.assertIsNone(self.sessao_ctrl.buscar_sessao(sessao.codigo))
