"""Controller for managing TipoIngresso business rules and database persistence."""

import sqlite3
from pathlib import Path

from src.model.database import execute_query, execute_query_one, execute_write
from src.model.tipo_ingresso import TipoIngresso

__all__ = ["TipoIngressoController"]


class TipoIngressoController:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = db_path

    @property
    def db_path(self) -> str | Path | None:
        return self._db_path

    def cadastrar_tipo_ingresso(self, tipo_sala: str, valor_ingresso: int) -> bool:
        if not isinstance(tipo_sala, str) or tipo_sala not in ("2D", "3D"):
            return False
        if type(valor_ingresso) is not int or valor_ingresso <= 0:
            return False

        try:
            execute_write(
                """
                INSERT INTO tipos_ingresso (tipo, valor)
                VALUES (?, ?)
                ON CONFLICT(tipo) DO UPDATE SET valor = excluded.valor;
                """,
                (tipo_sala.strip(), valor_ingresso),
                db_path=self._db_path,
            )
        except sqlite3.Error:
            return False
        return True

    def listar_tipos_ingresso(self) -> list[TipoIngresso]:
        rows = execute_query(
            "SELECT tipo, valor FROM tipos_ingresso ORDER BY tipo ASC;",
            db_path=self._db_path,
        )
        return [TipoIngresso(tipo=row["tipo"], valor=row["valor"]) for row in rows]

    def buscar_tipo_ingresso(self, tipo: str) -> TipoIngresso | None:
        if not isinstance(tipo, str):
            return None

        row = execute_query_one(
            "SELECT tipo, valor FROM tipos_ingresso WHERE tipo = ?;",
            (tipo.strip(),),
            db_path=self._db_path,
        )
        if row is None:
            return None
        return TipoIngresso(tipo=row["tipo"], valor=row["valor"])

    def editar_tipo_ingresso(self, tipo: str, valor: int) -> TipoIngresso | None:
        if type(valor) is not int or valor <= 0:
            return None
        if not isinstance(tipo, str) or tipo not in ("2D", "3D"):
            return None

        try:
            cursor = execute_write(
                "UPDATE tipos_ingresso SET valor = ? WHERE tipo = ?;",
                (valor, tipo.strip()),
                db_path=self._db_path,
            )
            if cursor.rowcount == 0:
                return None
            return TipoIngresso(tipo=tipo.strip(), valor=valor)
        except sqlite3.Error:
            return None

    def remover_tipo_ingresso(self, tipo: str) -> bool:
        if not isinstance(tipo, str):
            return False

        try:
            cursor = execute_write(
                "DELETE FROM tipos_ingresso WHERE tipo = ?;",
                (tipo.strip(),),
                db_path=self._db_path,
            )
        except sqlite3.Error:
            return False
        else:
            return cursor.rowcount > 0
