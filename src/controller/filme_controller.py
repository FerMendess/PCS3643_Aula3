"""Controller for managing Filme business rules and database persistence."""

import sqlite3
from pathlib import Path

from src.controller.helpers.validar_data import validar_data
from src.model.database import execute_query, execute_query_one, execute_write
from src.model.filme import Filme


class FilmeController:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = db_path

    @property
    def db_path(self) -> str | Path | None:
        return self._db_path

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

        try:
            cursor = execute_write(
                """
                INSERT INTO filmes (nome, data_estreia, data_saida, duracao)
                VALUES (?, ?, ?, ?);
                """,
                (nome.strip(), data_estreia, data_saida, duracao),
                db_path=self._db_path,
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

    def listar_filmes(self) -> list[Filme]:
        rows = execute_query(
            "SELECT codigo, nome, data_estreia, data_saida, duracao FROM filmes ORDER BY codigo ASC;",
            db_path=self._db_path,
        )
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

    def buscar_filme(self, codigo: int | str) -> Filme | None:
        try:
            codigo_int = int(codigo)
        except ValueError, TypeError:
            return None

        row = execute_query_one(
            "SELECT codigo, nome, data_estreia, data_saida, duracao FROM filmes WHERE codigo = ?;",
            (codigo_int,),
            db_path=self._db_path,
        )
        if row is None:
            return None
        return Filme(
            codigo=row["codigo"],
            nome=row["nome"],
            data_estreia=row["data_estreia"],
            data_saida=row["data_saida"],
            duracao=row["duracao"],
        )

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

        nova_estreia = (
            data_estreia if data_estreia is not None else filme_atual.data_estreia
        )
        nova_saida = data_saida if data_saida is not None else filme_atual.data_saida

        dt_estreia = validar_data(nova_estreia)
        dt_saida = validar_data(nova_saida)
        if dt_estreia is None or dt_saida is None or dt_saida < dt_estreia:
            return None

        try:
            execute_write(
                """
                UPDATE filmes
                SET nome = ?, data_estreia = ?, data_saida = ?, duracao = ?
                WHERE codigo = ?;
                """,
                (novo_nome, nova_estreia, nova_saida, nova_duracao, filme_atual.codigo),
                db_path=self._db_path,
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

    def remover_filme(self, codigo: int | str) -> bool:
        try:
            codigo_int = int(codigo)
        except ValueError, TypeError:
            return False

        try:
            cursor = execute_write(
                "DELETE FROM filmes WHERE codigo = ?;",
                (codigo_int,),
                db_path=self._db_path,
            )
        except sqlite3.IntegrityError:
            return False
        else:
            return cursor.rowcount > 0
