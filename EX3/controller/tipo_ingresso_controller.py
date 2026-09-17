"""Controller for managing TipoIngresso business rules and database persistence."""

from __future__ import annotations

import sqlite3

from model.database import get_connection
from model.tipo_ingresso import TipoIngresso


class TipoIngressoController:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path

    def cadastrar_tipo_ingresso(self, tipo_sala: str, valor_ingresso: int) -> bool:
        if not isinstance(tipo_sala, str) or tipo_sala not in ("2D", "3D"):
            return False
        if type(valor_ingresso) is not int or valor_ingresso <= 0:
            return False

        conn = get_connection(self.db_path)
        try:
            with conn:
                conn.execute(
                    """
                    INSERT INTO tipos_ingresso (tipo, valor)
                    VALUES (?, ?)
                    ON CONFLICT(tipo) DO UPDATE SET valor = excluded.valor;
                    """,
                    (tipo_sala.strip(), valor_ingresso),
                )
        except sqlite3.Error:
            return False
        finally:
            conn.close()
        return True


    def listar_tipos_ingresso(self) -> list[TipoIngresso]:
        conn = get_connection(self.db_path)
        try:
            cursor = conn.execute("SELECT tipo, valor FROM tipos_ingresso ORDER BY tipo ASC;")
            rows = cursor.fetchall()
            return [TipoIngresso(tipo=row["tipo"], valor=row["valor"]) for row in rows]
        finally:
            conn.close()

    def buscar_tipo_ingresso(self, tipo: str) -> TipoIngresso | None:
        if not isinstance(tipo, str):
            return None
        conn = get_connection(self.db_path)
        try:
            cursor = conn.execute(
                "SELECT tipo, valor FROM tipos_ingresso WHERE tipo = ?;",
                (tipo.strip(),),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return TipoIngresso(tipo=row["tipo"], valor=row["valor"])
        finally:
            conn.close()

    def editar_tipo_ingresso(self, tipo: str, valor: int) -> TipoIngresso | None:
        if type(valor) is not int or valor <= 0:
            return None
        if not isinstance(tipo, str) or tipo not in ("2D", "3D"):
            return None

        conn = get_connection(self.db_path)
        try:
            with conn:
                cursor = conn.execute(
                    "UPDATE tipos_ingresso SET valor = ? WHERE tipo = ?;",
                    (valor, tipo.strip()),
                )
                if cursor.rowcount == 0:
                    return None
            return TipoIngresso(tipo=tipo.strip(), valor=valor)
        finally:
            conn.close()

    def remover_tipo_ingresso(self, tipo: str) -> bool:
        if not isinstance(tipo, str):
            return False
        conn = get_connection(self.db_path)
        try:
            with conn:
                cursor = conn.execute(
                    "DELETE FROM tipos_ingresso WHERE tipo = ?;",
                    (tipo.strip(),),
                )
                return cursor.rowcount > 0
        finally:
            conn.close()
