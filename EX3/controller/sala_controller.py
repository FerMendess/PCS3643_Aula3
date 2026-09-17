"""Controller for managing Sala business rules and database persistence."""

from __future__ import annotations

import sqlite3

from model.database import get_connection
from model.sala import Sala


class SalaController:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path

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

        conn = get_connection(self.db_path)
        try:
            with conn:
                conn.execute(
                    "INSERT INTO salas (numero, capacidade, tipo) VALUES (?, ?, ?);",
                    (numero, capacidade, tipo_sala),
                )
            return Sala(numero=numero, capacidade=capacidade, tipo=tipo_sala)
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    def listar_salas(self) -> list[Sala]:
        conn = get_connection(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT numero, capacidade, tipo FROM salas ORDER BY numero ASC;"
            )
            rows = cursor.fetchall()
            return [
                Sala(
                    numero=row["numero"],
                    capacidade=row["capacidade"],
                    tipo=row["tipo"],
                )
                for row in rows
            ]
        finally:
            conn.close()

    def buscar_sala(self, numero: int | str) -> Sala | None:
        try:
            numero_int = int(numero)
        except (ValueError, TypeError):
            return None

        conn = get_connection(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT numero, capacidade, tipo FROM salas WHERE numero = ?;",
                (numero_int,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return Sala(
                numero=row["numero"],
                capacidade=row["capacidade"],
                tipo=row["tipo"],
            )
        finally:
            conn.close()

    def editar_sala(
        self,
        numero: int | str,
        capacidade: int | None = None,
        tipo: str | None = None,
    ) -> Sala | None:
        sala_atual = self.buscar_sala(numero)
        if sala_atual is None:
            return None

        nova_capacidade = capacidade if capacidade is not None else sala_atual.capacidade
        novo_tipo = tipo if tipo is not None else sala_atual.tipo

        if type(nova_capacidade) is not int or nova_capacidade <= 0:
            return None
        if not isinstance(novo_tipo, str) or novo_tipo not in ("2D", "3D"):
            return None

        conn = get_connection(self.db_path)
        try:
            with conn:
                conn.execute(
                    "UPDATE salas SET capacidade = ?, tipo = ? WHERE numero = ?;",
                    (nova_capacidade, novo_tipo, sala_atual.numero),
                )
            return Sala(
                numero=sala_atual.numero,
                capacidade=nova_capacidade,
                tipo=novo_tipo,
            )
        finally:
            conn.close()

    def remover_sala(self, numero: int | str) -> bool:
        try:
            numero_int = int(numero)
        except (ValueError, TypeError):
            return False

        conn = get_connection(self.db_path)
        try:
            with conn:
                cursor = conn.execute(
                    "DELETE FROM salas WHERE numero = ?;",
                    (numero_int,),
                )
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
