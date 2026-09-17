"""Unit tests for Controller layer and Cinema business rules."""

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
from src.controller.buscaController import BuscaController
from src.controller.cadastraController import CadastraController
from src.controller.filme_controller import FilmeController
from src.controller.sala_controller import SalaController
from src.controller.sessao_controller import SessaoController
from src.controller.tipo_ingresso_controller import TipoIngressoController


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
        assert filme is not None
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
        assert f1 is not None and f2 is not None
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
        self.assertFalse(cadastrar_valor_ingresso(None, 30))  # type: ignore[arg-type]

    def test_cadastrar_valor_ingresso_valor_menor_ou_igual_a_zero(self):
        self.assertFalse(cadastrar_valor_ingresso("2D", 0))
        self.assertFalse(cadastrar_valor_ingresso("2D", -20))

    def test_cadastrar_valor_ingresso_valor_nao_inteiro(self):
        self.assertFalse(cadastrar_valor_ingresso("2D", 35.5))  # type: ignore[arg-type]
        self.assertFalse(cadastrar_valor_ingresso("2D", "30"))  # type: ignore[arg-type]


class TestUS03CadastrarSala(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()

    def test_cadastrar_sala_sucesso(self):
        sala = cadastrar_sala(1, 50, "2D")
        self.assertIsNotNone(sala)
        assert sala is not None
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
        self.assertIsNone(cadastrar_sala(3, 50, None))  # type: ignore[arg-type]


class TestUS04CadastrarSessao(unittest.TestCase):
    def setUp(self):
        reiniciar_estado()
        self.sala = cadastrar_sala(1, 10, "2D")
        self.filme = cadastrar_filme("Inception", "01/06/2026", "30/06/2026", 148)

    def test_cadastrar_sessao_sucesso(self):
        sessao = cadastrar_sessao(1, 1, "15/06/2026", 20)
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
        self.assertIn(sessao, cinema.sessoes)

    def test_cadastrar_multiplas_sessoes_codigos_sequenciais(self):
        s1 = cadastrar_sessao(1, 1, "15/06/2026", 14)
        s2 = cadastrar_sessao(1, 1, "15/06/2026", 18)
        self.assertIsNotNone(s1)
        self.assertIsNotNone(s2)
        assert s1 is not None and s2 is not None
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
        self.assertIsNone(cadastrar_sessao(1, 1, "15/06/2026", "20"))  # type: ignore[arg-type]

    def test_cadastrar_sessao_assentos_quantidade(self):
        sessao = cadastrar_sessao(1, 1, "15/06/2026", 20)
        self.assertIsNotNone(sessao)
        sala = cinema.pegar_sala(1)
        assert sala is not None
        self.assertEqual(sala.capacidade, len(sessao.assentos))  # type: ignore[union-attr]

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
        assert sessao is not None
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
        self.assertEqual(listar_filmes_por_data(None), "Data invalida.")  # type: ignore[arg-type]


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
        assert self.sessao is not None
        self.assertEqual(self.sessao.assentos[1], 1)

    def test_comprar_ingressos_sucesso_meia(self):
        total = comprarIngressos(1, [2], [1])
        self.assertEqual(total, 20)
        assert self.sessao is not None
        self.assertEqual(self.sessao.assentos[2], 1)

    def test_comprar_ingressos_sucesso_multiplos_misto(self):
        total = comprarIngressos(1, [1, 2], [0, 1])
        self.assertEqual(total, 60)
        assert self.sessao is not None
        self.assertEqual(self.sessao.assentos[1], 1)
        self.assertEqual(self.sessao.assentos[2], 1)

    def test_comprar_ingressos_sessao_inexistente(self):
        total = comprarIngressos(99, [1], [0])
        self.assertEqual(total, 0)
        assert self.sessao is not None
        self.assertEqual(self.sessao.assentos[1], 0)

    def test_comprar_ingressos_assento_ja_ocupado_atomicidade(self):
        assert self.sessao is not None
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
        assert self.sessao is not None
        self.assertEqual(self.sessao.assentos[1], 0)

    def test_comprar_ingressos_tamanhos_diferentes(self):
        total = comprarIngressos(1, [1, 2], [0])
        self.assertEqual(total, 0)
        assert self.sessao is not None
        self.assertEqual(self.sessao.assentos[1], 0)
        self.assertEqual(self.sessao.assentos[2], 0)

    def test_comprar_ingressos_lista_vazia(self):
        total = comprarIngressos(1, [], [])
        self.assertEqual(total, 0)

    def test_comprar_ingressos_tipo_invalido(self):
        total = comprarIngressos(1, [1], [2])
        self.assertEqual(total, 0)
        assert self.sessao is not None
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
        filme = self.filme_ctrl.cadastrar_filme(
            "Interestelar", "10/10/2026", "20/10/2026", 169
        )
        self.assertIsNotNone(filme)
        assert filme is not None
        self.assertEqual(filme.nome, "Interestelar")

        buscado = self.busca_ctrl.pegar_filme(filme.codigo)  # type: ignore[arg-type]
        self.assertIsNotNone(buscado)
        assert buscado is not None
        self.assertEqual(buscado.nome, "Interestelar")

        editado = self.filme_ctrl.editar_filme(
            filme.codigo, nome="Interestelar IMAX", duracao=175
        )  # type: ignore[arg-type]
        self.assertIsNotNone(editado)
        assert editado is not None
        self.assertEqual(editado.nome, "Interestelar IMAX")
        self.assertEqual(editado.duracao, 175)

        lista = self.filme_ctrl.listar_filmes()
        self.assertEqual(len(lista), 1)

        removido = self.filme_ctrl.remover_filme(filme.codigo)  # type: ignore[arg-type]
        self.assertTrue(removido)
        self.assertIsNone(self.filme_ctrl.buscar_filme(filme.codigo))  # type: ignore[arg-type]

    def test_sala_crud_completo(self):
        sala = self.cadastra_ctrl.cadastrar_sala(5, 60, "3D")
        self.assertIsNotNone(sala)
        assert sala is not None
        self.assertEqual(sala.numero, 5)

        buscada = self.sala_ctrl.buscar_sala(5)
        self.assertIsNotNone(buscada)
        assert buscada is not None
        self.assertEqual(buscada.capacidade, 60)

        editada = self.sala_ctrl.editar_sala(5, capacidade=75, tipo="2D")
        self.assertIsNotNone(editada)
        assert editada is not None
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
        assert buscado is not None
        self.assertEqual(buscado.valor, 35)

        editado = self.tipo_ingresso_ctrl.editar_tipo_ingresso("2D", 40)
        self.assertIsNotNone(editado)
        assert editado is not None
        self.assertEqual(editado.valor, 40)

        lista = self.tipo_ingresso_ctrl.listar_tipos_ingresso()
        self.assertEqual(len(lista), 1)

        removido = self.tipo_ingresso_ctrl.remover_tipo_ingresso("2D")
        self.assertTrue(removido)
        self.assertIsNone(self.tipo_ingresso_ctrl.buscar_tipo_ingresso("2D"))

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
