"""Controller for managing Sessao and Ticket purchase business rules."""

import sqlite3
from collections.abc import Sequence
from pathlib import Path
from typing import Any, override

from src.controller.filme_controller import FilmeController
from src.controller.helpers.validar_data import validar_data
from src.controller.sala_controller import SalaController
from src.controller.tipo_ingresso_controller import TipoIngressoController
from src.model.database import (
    db_transaction,
    execute_query,
    execute_query_one,
    execute_write,
)
from src.model.sessao import Sessao

__all__ = ["SessaoController"]

_HORA_MINIMA = 0
_HORA_MAXIMA = 23


class _SynchronizedSeatsDict(dict[int, int]):
    def __init__(
        self,
        sessao_codigo: int,
        db_path: str | Path | None = None,
        initial: dict[int, int] | None = None,
    ) -> None:
        super().__init__(initial or {})
        self._sessao_codigo = sessao_codigo
        self._db_path = db_path

    @override
    def __setitem__(self, seat: int, val: int) -> None:
        super().__setitem__(seat, val)
        execute_write(
            "UPDATE assentos SET ocupado = ? WHERE codigo_sessao = ? AND numero_assento = ?;",
            (val, self._sessao_codigo, seat),
            db_path=self._db_path,
        )


class SessaoController:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = db_path
        self._filme_ctrl = FilmeController(db_path)
        self._sala_ctrl = SalaController(db_path)
        self._tipo_ingresso_ctrl = TipoIngressoController(db_path)

    @property
    def db_path(self) -> str | Path | None:
        return self._db_path

    @property
    def filme_ctrl(self) -> FilmeController:
        return self._filme_ctrl

    @property
    def sala_ctrl(self) -> SalaController:
        return self._sala_ctrl

    @property
    def tipo_ingresso_ctrl(self) -> TipoIngressoController:
        return self._tipo_ingresso_ctrl

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
            or not (_HORA_MINIMA <= hora_inicio <= _HORA_MAXIMA)
            or dt_sessao is None
        ):
            return None

        sala = self._sala_ctrl.buscar_sala(numero_sala)
        filme = self._filme_ctrl.buscar_filme(codigo_filme)
        if sala is None or filme is None or sala.capacidade is None:
            return None

        conflito = execute_query_one(
            """
            SELECT 1 FROM sessoes
            WHERE numero_sala = ? AND data = ? AND hora_inicio = ?;
            """,
            (numero_sala, data_sessao, hora_inicio),
            db_path=self._db_path,
        )
        if conflito is not None:
            return None

        try:
            with db_transaction(self._db_path) as conn:
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
                    self._db_path,
                    dict.fromkeys(range(1, sala.capacidade + 1), 0),
                )
                return sessao
        except sqlite3.Error:
            return None

    def listar_sessoes(self) -> list[Sessao]:
        rows = execute_query(
            "SELECT codigo, numero_sala, codigo_filme, data, hora_inicio FROM sessoes ORDER BY codigo ASC;",
            db_path=self._db_path,
        )
        sessoes: list[Sessao] = []
        for row in rows:
            sala = self._sala_ctrl.buscar_sala(row["numero_sala"])
            filme = self._filme_ctrl.buscar_filme(row["codigo_filme"])
            sessao = Sessao(
                codigo=row["codigo"],
                sala=sala,
                filme=filme,
                data=row["data"],
                hora_inicio=row["hora_inicio"],
            )
            rows_assentos = execute_query(
                "SELECT numero_assento, ocupado FROM assentos WHERE codigo_sessao = ? ORDER BY numero_assento ASC;",
                (row["codigo"],),
                db_path=self._db_path,
            )
            sessao.assentos = _SynchronizedSeatsDict(
                row["codigo"],
                self._db_path,
                {a["numero_assento"]: a["ocupado"] for a in rows_assentos},
            )
            sessoes.append(sessao)
        return sessoes

    def buscar_sessao(self, codigo: int | str) -> Sessao | None:
        try:
            codigo_int = int(codigo)
        except (ValueError, TypeError):
            return None

        row = execute_query_one(
            "SELECT codigo, numero_sala, codigo_filme, data, hora_inicio FROM sessoes WHERE codigo = ?;",
            (codigo_int,),
            db_path=self._db_path,
        )
        if row is None:
            return None

        sala = self._sala_ctrl.buscar_sala(row["numero_sala"])
        filme = self._filme_ctrl.buscar_filme(row["codigo_filme"])
        sessao = Sessao(
            codigo=row["codigo"],
            sala=sala,
            filme=filme,
            data=row["data"],
            hora_inicio=row["hora_inicio"],
        )
        rows_assentos = execute_query(
            "SELECT numero_assento, ocupado FROM assentos WHERE codigo_sessao = ? ORDER BY numero_assento ASC;",
            (codigo_int,),
            db_path=self._db_path,
        )
        sessao.assentos = _SynchronizedSeatsDict(
            codigo_int,
            self._db_path,
            {a["numero_assento"]: a["ocupado"] for a in rows_assentos},
        )
        return sessao

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
            not isinstance(novo_num_sala, int)
            or not isinstance(novo_cod_filme, int)
            or not isinstance(nova_hora, int)
            or not (_HORA_MINIMA <= nova_hora <= _HORA_MAXIMA)
            or validar_data(nova_data) is None
            or self._sala_ctrl.buscar_sala(novo_num_sala) is None
            or self._filme_ctrl.buscar_filme(novo_cod_filme) is None
        ):
            return None

        conflito = execute_query_one(
            """
            SELECT 1 FROM sessoes
            WHERE numero_sala = ? AND data = ? AND hora_inicio = ? AND codigo != ?;
            """,
            (novo_num_sala, nova_data, nova_hora, sessao_atual.codigo),
            db_path=self._db_path,
        )
        if conflito is not None:
            return None

        try:
            execute_write(
                """
                UPDATE sessoes
                SET numero_sala = ?, codigo_filme = ?, data = ?, hora_inicio = ?
                WHERE codigo = ?;
                """,
                (
                    novo_num_sala,
                    novo_cod_filme,
                    nova_data,
                    nova_hora,
                    sessao_atual.codigo,
                ),
                db_path=self._db_path,
            )
            return (
                self.buscar_sessao(sessao_atual.codigo)
                if sessao_atual.codigo is not None
                else None
            )
        except sqlite3.Error:
            return None

    def remover_sessao(self, codigo: int | str) -> bool:
        try:
            codigo_int = int(codigo)
        except (ValueError, TypeError):
            return False

        try:
            cursor = execute_write(
                "DELETE FROM sessoes WHERE codigo = ?;",
                (codigo_int,),
                db_path=self._db_path,
            )
        except sqlite3.Error:
            return False
        else:
            return cursor.rowcount > 0

    def listar_filmes_por_data(self, data: str) -> str:
        if validar_data(data) is None:
            return "Data invalida."

        sessoes = self.listar_sessoes()
        linhas: list[str] = []
        for sessao in sessoes:
            if sessao.data == data and sessao.sala and sessao.filme:
                tem_assentos_disponiveis = any(
                    status == 0 for status in sessao.assentos.values()
                )
                if tem_assentos_disponiveis:
                    tipo_obj = self._tipo_ingresso_ctrl.buscar_tipo_ingresso(
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
                    tipo_obj = self._tipo_ingresso_ctrl.buscar_tipo_ingresso(
                        sessao.sala.tipo or ""
                    )
                    valor = tipo_obj.valor if tipo_obj else 0
                    detalhes.append(
                        {
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
                        }
                    )
        return detalhes

    def comprar_ingressos(
        self,
        codigo_sessao: int | str,
        assentos: Sequence[int],
        tipos_ingresso: Sequence[int],
    ) -> int | float:
        if (
            not isinstance(assentos, (list, tuple))
            or not isinstance(tipos_ingresso, (list, tuple))
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

        tipo_obj = self._tipo_ingresso_ctrl.buscar_tipo_ingresso(sessao.sala.tipo or "")
        preco_sala: float = (
            float(tipo_obj.valor) if tipo_obj and tipo_obj.valor is not None else 0.0
        )

        try:
            with db_transaction(self._db_path) as conn:
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
                    preco_sala if tipo == 0 else preco_sala / 2
                    for tipo in tipos_ingresso
                )
                return int(total) if total == int(total) else total
        except sqlite3.Error:
            return 0
