"""Controller for managing Filme business rules and database persistence."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from model.database import get_connection
from model.filme import Filme

class FilmeController:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path

    def cadastrar_filme(
        self,
        nome: str,
        data_estreia: str,
        data_saida: str,
        duracao: int,
    ) -> Filme | None:
        if not isinstance(nome, str) or not nome.strip():
            return None
        if not isinstance(duracao, int) or duracao <= 0:
            return None

        dt_estreia = validar_data(data_estreia)
        dt_saida = validar_data(data_saida)
        if dt_estreia is None or dt_saida is None:
            return None
        if dt_saida < dt_estreia:
            return None

        conn = get_connection(self.db_path)
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO filmes (nome, data_estreia, data_saida, duracao)
                    VALUES (?, ?, ?, ?);
                    """,
                    (nome.strip(), data_estreia, data_saida, duracao),
                )
                codigo = cursor.lastrowid
                return Filme(
                    codigo=codigo,
                    nome=nome.strip(),
                    data_estreia=data_estreia,
                    data_saida=data_saida,
                    duracao=duracao,
                )
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    def listar_filmes(self) -> list[Filme]:
        conn = get_connection(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT codigo, nome, data_estreia, data_saida, duracao FROM filmes ORDER BY codigo ASC;"
            )
            rows = cursor.fetchall()
            return [
                Filme(
                    codigo=row["codigo"],
                    nome=row["nome"],
                    data_estreia=row["data_estreia"],
                    data_saida=row["data_saida"],
                    duracao=row["duracao"],
                )
                for row in rows
            ]
        finally:
            conn.close()

    def buscar_filme(self, codigo: int | str) -> Filme | None:
        try:
            codigo_int = int(codigo)
        except (ValueError, TypeError):
            return None

        conn = get_connection(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT codigo, nome, data_estreia, data_saida, duracao FROM filmes WHERE codigo = ?;",
                (codigo_int,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return Filme(
                codigo=row["codigo"],
                nome=row["nome"],
                data_estreia=row["data_estreia"],
                data_saida=row["data_saida"],
                duracao=row["duracao"],
            )
        finally:
            conn.close()

    def editar_filme(
        self,
        codigo: int | str,
        nome: str | None = None,
        data_estreia: str | None = None,
        data_saida: str | None = None,
        duracao: int | None = None,
    ) -> Filme | None:
        filme_atual = self.buscar_filme(codigo)
        if filme_atual is None:
            return None

        novo_nome = nome.strip() if nome is not None else filme_atual.nome
        if not novo_nome:
            return None

        nova_duracao = duracao if duracao is not None else filme_atual.duracao
        if not isinstance(nova_duracao, int) or nova_duracao <= 0:
            return None

        nova_estreia = data_estreia if data_estreia is not None else filme_atual.data_estreia
        nova_saida = data_saida if data_saida is not None else filme_atual.data_saida

        dt_estreia = validar_data(nova_estreia)
        dt_saida = validar_data(nova_saida)
        if dt_estreia is None or dt_saida is None or dt_saida < dt_estreia:
            return None

        conn = get_connection(self.db_path)
        try:
            with conn:
                conn.execute(
                    """
                    UPDATE filmes
                    SET nome = ?, data_estreia = ?, data_saida = ?, duracao = ?
                    WHERE codigo = ?;
                    """,
                    (novo_nome, nova_estreia, nova_saida, nova_duracao, filme_atual.codigo),
                )
            return Filme(
                codigo=filme_atual.codigo,
                nome=novo_nome,
                data_estreia=nova_estreia,
                data_saida=nova_saida,
                duracao=nova_duracao,
            )
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    def remover_filme(self, codigo: int | str) -> bool:
        try:
            codigo_int = int(codigo)
        except (ValueError, TypeError):
            return False

        conn = get_connection(self.db_path)
        try:
            with conn:
                cursor = conn.execute(
                    "DELETE FROM filmes WHERE codigo = ?;",
                    (codigo_int,),
                )
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            # Caso haja sessões vinculadas
            return False
        finally:
            conn.close()
