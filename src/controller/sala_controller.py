"""Controller for managing Sala business rules and database persistence."""

import sqlite3
from pathlib import Path

from model.database import execute_query, execute_query_one, execute_write
from model.sala import Sala

__all__ = ["SalaController"]


class SalaController:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = db_path

    @property
    def db_path(self) -> str | Path | None:
        return self._db_path

    def cadastrar_sala(
        self,
        numero: int,
        capacidade: int,
        tipo_sala: str,
    ) -> Sala | None:
        if type(numero) is not int or numero <= 0:
            return None
        if type(capacidade) is not int or capacidade <= 0:
            return None
        if not isinstance(tipo_sala, str) or tipo_sala not in ("2D", "3D"):
            return None

        try:
            execute_write(
                "INSERT INTO salas (numero, capacidade, tipo) VALUES (?, ?, ?);",
                (numero, capacidade, tipo_sala),
                db_path=self._db_path,
            )
            return Sala(numero=numero, capacidade=capacidade, tipo=tipo_sala)
        except sqlite3.IntegrityError:
            return None

    def listar_salas(self) -> list[Sala]:
        rows = execute_query(
            "SELECT numero, capacidade, tipo FROM salas ORDER BY numero ASC;",
            db_path=self._db_path,
        )
        return [
            Sala(
                numero=row["numero"],
                capacidade=row["capacidade"],
                tipo=row["tipo"],
            )
            for row in rows
        ]

    def buscar_sala(self, numero: int | str) -> Sala | None:
        try:
            numero_int = int(numero)
        except ValueError, TypeError:
            return None

        row = execute_query_one(
            "SELECT numero, capacidade, tipo FROM salas WHERE numero = ?;",
            (numero_int,),
            db_path=self._db_path,
        )
        if row is None:
            return None
        return Sala(
            numero=row["numero"],
            capacidade=row["capacidade"],
            tipo=row["tipo"],
        )

    def editar_sala(
        self,
        numero: int | str,
        capacidade: int | None = None,
        tipo: str | None = None,
    ) -> Sala | None:
        sala_atual = self.buscar_sala(numero)
        if sala_atual is None:
            return None

        nova_capacidade = (
            capacidade if capacidade is not None else sala_atual.capacidade
        )
        novo_tipo = tipo if tipo is not None else sala_atual.tipo

        if type(nova_capacidade) is not int or nova_capacidade <= 0:
            return None
        if not isinstance(novo_tipo, str) or novo_tipo not in ("2D", "3D"):
            return None

        try:
            execute_write(
                "UPDATE salas SET capacidade = ?, tipo = ? WHERE numero = ?;",
                (nova_capacidade, novo_tipo, sala_atual.numero),
                db_path=self._db_path,
            )
            return Sala(
                numero=sala_atual.numero,
                capacidade=nova_capacidade,
                tipo=novo_tipo,
            )
        except sqlite3.IntegrityError:
            return None

    def remover_sala(self, numero: int | str) -> bool:
        try:
            numero_int = int(numero)
        except ValueError, TypeError:
            return False

        try:
            cursor = execute_write(
                "DELETE FROM salas WHERE numero = ?;",
                (numero_int,),
                db_path=self._db_path,
            )
        except sqlite3.IntegrityError:
            return False
        else:
            return cursor.rowcount > 0
