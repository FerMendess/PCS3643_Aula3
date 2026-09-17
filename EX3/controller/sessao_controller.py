"""Controller for managing Sessao and Ticket purchase business rules."""

from __future__ import annotations

import sqlite3
from typing import Any, override

from model.database import get_connection
from model.sessao import Sessao

from controller.filme_controller import FilmeController
from controller.helpers import validar_data
from controller.sala_controller import SalaController
from controller.tipo_ingresso_controller import TipoIngressoController

HORA_MINIMA = 0
HORA_MAXIMA = 23


class _SynchronizedSeatsDict(dict[int, int]):
    def __init__(
        self,
        sessao_codigo: int,
        db_path: str | None = None,
        initial: dict[int, int] | None = None,
    ) -> None:
        super().__init__(initial or {})
        self._sessao_codigo = sessao_codigo
        self._db_path = db_path

    @override
    def __setitem__(self, seat: int, val: int) -> None:
        super().__setitem__(seat, val)
        conn = get_connection(self._db_path)
        try:
            with conn:
                conn.execute(
                    "UPDATE assentos SET ocupado = ? WHERE codigo_sessao = ? AND numero_assento = ?;",
                    (val, self._sessao_codigo, seat),
                )
        finally:
            conn.close()


class SessaoController:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path
        self.filme_ctrl = FilmeController(db_path)
        self.sala_ctrl = SalaController(db_path)
        self.tipo_ingresso_ctrl = TipoIngressoController(db_path)

    def cadastrar_sessao(
        self,
        numero_sala: int,
        codigo_filme: int,
        data_sessao: str,
        hora_inicio: int,
    ) -> Sessao | None:
        dt_sessao = validar_data(data_sessao)
        if (
            type(numero_sala) is not int
            or type(codigo_filme) is not int
            or type(hora_inicio) is not int
            or not (HORA_MINIMA <= hora_inicio <= HORA_MAXIMA)
            or dt_sessao is None
        ):
            return None

        sala = self.sala_ctrl.buscar_sala(numero_sala)
        filme = self.filme_ctrl.buscar_filme(codigo_filme)
        if sala is None or filme is None or sala.capacidade is None:
            return None

        conn = get_connection(self.db_path)
        try:
            with conn:
                cursor = conn.execute(
                    """
                    SELECT 1 FROM sessoes
                    WHERE numero_sala = ? AND data = ? AND hora_inicio = ?;
                    """,
                    (numero_sala, data_sessao, hora_inicio),
                )
                if cursor.fetchone() is not None:
                    return None

                cursor = conn.execute(
                    """
                    INSERT INTO sessoes (numero_sala, codigo_filme, data, hora_inicio)
                    VALUES (?, ?, ?, ?);
                    """,
                    (numero_sala, codigo_filme, data_sessao, hora_inicio),
                )
                codigo_sessao = cursor.lastrowid
                if codigo_sessao is None:
                    return None

                assentos_data = [
                    (codigo_sessao, num, 0) for num in range(1, sala.capacidade + 1)
                ]
                conn.executemany(
                    "INSERT INTO assentos (codigo_sessao, numero_assento, ocupado) VALUES (?, ?, ?);",
                    assentos_data,
                )

                sessao = Sessao(
                    codigo=codigo_sessao,
                    sala=sala,
                    filme=filme,
                    data=data_sessao,
                    hora_inicio=hora_inicio,
                )
                sessao.assentos = _SynchronizedSeatsDict(
                    codigo_sessao,
                    self.db_path,
                    dict.fromkeys(range(1, sala.capacidade + 1), 0),
                )
                return sessao
        finally:
            conn.close()

    def listar_sessoes(self) -> list[Sessao]:
        conn = get_connection(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT codigo, numero_sala, codigo_filme, data, hora_inicio FROM sessoes ORDER BY codigo ASC;"
            )
            rows = cursor.fetchall()
            sessoes: list[Sessao] = []
            for row in rows:
                sala = self.sala_ctrl.buscar_sala(row["numero_sala"])
                filme = self.filme_ctrl.buscar_filme(row["codigo_filme"])
                sessao = Sessao(
                    codigo=row["codigo"],
                    sala=sala,
                    filme=filme,
                    data=row["data"],
                    hora_inicio=row["hora_inicio"],
                )
                cursor_assentos = conn.execute(
                    "SELECT numero_assento, ocupado FROM assentos WHERE codigo_sessao = ? ORDER BY numero_assento ASC;",
                    (row["codigo"],),
                )
                sessao.assentos = _SynchronizedSeatsDict(
                    row["codigo"],
                    self.db_path,
                    {a["numero_assento"]: a["ocupado"] for a in cursor_assentos.fetchall()},
                )
                sessoes.append(sessao)
            return sessoes
        finally:
            conn.close()

    def buscar_sessao(self, codigo: int | str) -> Sessao | None:
        try:
            codigo_int = int(codigo)
        except (ValueError, TypeError):
            return None

        conn = get_connection(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT codigo, numero_sala, codigo_filme, data, hora_inicio FROM sessoes WHERE codigo = ?;",
                (codigo_int,),
            )
            row = cursor.fetchone()
            if row is None:
                return None

            sala = self.sala_ctrl.buscar_sala(row["numero_sala"])
            filme = self.filme_ctrl.buscar_filme(row["codigo_filme"])
            sessao = Sessao(
                codigo=row["codigo"],
                sala=sala,
                filme=filme,
                data=row["data"],
                hora_inicio=row["hora_inicio"],
            )
            cursor_assentos = conn.execute(
                "SELECT numero_assento, ocupado FROM assentos WHERE codigo_sessao = ? ORDER BY numero_assento ASC;",
                (codigo_int,),
            )
            sessao.assentos = _SynchronizedSeatsDict(
                codigo_int,
                self.db_path,
                {a["numero_assento"]: a["ocupado"] for a in cursor_assentos.fetchall()},
            )
            return sessao
        finally:
            conn.close()

    def editar_sessao(
        self,
        codigo: int | str,
        numero_sala: int | None = None,
        codigo_filme: int | None = None,
        data: str | None = None,
        hora_inicio: int | None = None,
    ) -> Sessao | None:
        sessao_atual = self.buscar_sessao(codigo)
        if sessao_atual is None:
            return None

        novo_num_sala = (
            numero_sala
            if numero_sala is not None
            else (sessao_atual.sala.numero if sessao_atual.sala else None)
        )
        novo_cod_filme = (
            codigo_filme
            if codigo_filme is not None
            else (sessao_atual.filme.codigo if sessao_atual.filme else None)
        )
        nova_data = data if data is not None else sessao_atual.data
        nova_hora = hora_inicio if hora_inicio is not None else sessao_atual.hora_inicio

        if (
            type(novo_num_sala) is not int
            or type(novo_cod_filme) is not int
            or type(nova_hora) is not int
            or not (HORA_MINIMA <= nova_hora <= HORA_MAXIMA)
            or validar_data(nova_data) is None
        ):
            return None

        sala = self.sala_ctrl.buscar_sala(novo_num_sala)
        filme = self.filme_ctrl.buscar_filme(novo_cod_filme)
        if sala is None or filme is None:
            return None

        conn = get_connection(self.db_path)
        try:
            with conn:
                cursor = conn.execute(
                    """
                    SELECT 1 FROM sessoes
                    WHERE numero_sala = ? AND data = ? AND hora_inicio = ? AND codigo != ?;
                    """,
                    (novo_num_sala, nova_data, nova_hora, sessao_atual.codigo),
                )
                if cursor.fetchone() is not None:
                    return None

                conn.execute(
                    """
                    UPDATE sessoes
                    SET numero_sala = ?, codigo_filme = ?, data = ?, hora_inicio = ?
                    WHERE codigo = ?;
                    """,
                    (novo_num_sala, novo_cod_filme, nova_data, nova_hora, sessao_atual.codigo),
                )
            if sessao_atual.codigo is None:
                return None
            return self.buscar_sessao(sessao_atual.codigo)
        finally:
            conn.close()

    def remover_sessao(self, codigo: int | str) -> bool:
        try:
            codigo_int = int(codigo)
        except (ValueError, TypeError):
            return False

        conn = get_connection(self.db_path)
        try:
            with conn:
                cursor = conn.execute(
                    "DELETE FROM sessoes WHERE codigo = ?;",
                    (codigo_int,),
                )
                return cursor.rowcount > 0
        finally:
            conn.close()

    def listar_filmes_por_data(self, data: str) -> str:
        if validar_data(data) is None:
            return "Data invalida."

        sessoes = self.listar_sessoes()
        linhas = []
        for sessao in sessoes:
            if sessao.data == data and sessao.sala and sessao.filme:
                tem_assentos_disponiveis = any(
                    status == 0 for status in sessao.assentos.values()
                )
                if tem_assentos_disponiveis:
                    tipo_obj = self.tipo_ingresso_ctrl.buscar_tipo_ingresso(
                        sessao.sala.tipo or ""
                    )
                    valor = tipo_obj.valor if tipo_obj else 0
                    linha = (
                        f"{sessao.codigo}: {sessao.filme.nome}, "
                        f"sala {sessao.sala.numero} ({sessao.sala.tipo}), "
                        f"{sessao.hora_inicio}h, {valor} reais."
                    )
                    linhas.append(linha)

        if not linhas:
            return "Nenhum filme no dia escolhido."

        return "\n".join(linhas)

    def listar_filmes_por_data_detalhado(self, data: str) -> list[dict[str, Any]]:
        if validar_data(data) is None:
            return []

        sessoes = self.listar_sessoes()
        detalhes: list[dict[str, Any]] = []
        for sessao in sessoes:
            if sessao.data == data and sessao.sala and sessao.filme:
                tem_assentos_disponiveis = any(
                    status == 0 for status in sessao.assentos.values()
                )
                if tem_assentos_disponiveis:
                    tipo_obj = self.tipo_ingresso_ctrl.buscar_tipo_ingresso(
                        sessao.sala.tipo or ""
                    )
                    valor = tipo_obj.valor if tipo_obj else 0
                    detalhes.append({
                        "codigo": sessao.codigo,
                        "filme_nome": sessao.filme.nome,
                        "numero_sala": sessao.sala.numero,
                        "tipo_sala": sessao.sala.tipo,
                        "hora_inicio": sessao.hora_inicio,
                        "valor": valor,
                        "descricao": (
                            f"{sessao.codigo}: {sessao.filme.nome}, "
                            f"sala {sessao.sala.numero} ({sessao.sala.tipo}), "
                            f"{sessao.hora_inicio}h, {valor} reais."
                        ),
                    })
        return detalhes

    def comprar_ingressos(
        self,
        codigo_sessao: int | str,
        assentos: list[int],
        tipos_ingresso: list[int],
    ) -> int | float:
        if (
            not isinstance(assentos, list)
            or not isinstance(tipos_ingresso, list)
            or not assentos
            or len(assentos) != len(tipos_ingresso)
            or len(assentos) != len(set(assentos))
        ):
            return 0

        sessao = self.buscar_sessao(codigo_sessao)
        if sessao is None or sessao.sala is None:
            return 0

        for assento, tipo_ing in zip(assentos, tipos_ingresso, strict=True):
            if (
                assento not in sessao.assentos
                or sessao.assentos[assento] != 0
                or tipo_ing not in (0, 1)
            ):
                return 0

        tipo_obj = self.tipo_ingresso_ctrl.buscar_tipo_ingresso(
            sessao.sala.tipo or ""
        )
        preco_sala: float = float(tipo_obj.valor) if tipo_obj and tipo_obj.valor is not None else 0.0

        conn = get_connection(self.db_path)
        try:
            with conn:
                for assento in assentos:
                    cursor = conn.execute(
                        """
                        UPDATE assentos
                        SET ocupado = 1
                        WHERE codigo_sessao = ? AND numero_assento = ? AND ocupado = 0;
                        """,
                        (sessao.codigo, assento),
                    )
                    if cursor.rowcount == 0:
                        conn.rollback()
                        return 0

                total: float = sum(
                    preco_sala if tipo == 0 else preco_sala / 2 for tipo in tipos_ingresso
                )
                return int(total) if total == int(total) else total
        except sqlite3.Error:
            return 0
        finally:
            conn.close()

