"""Database connection, execution helpers, and table initialization for SQLite."""

import os
import sqlite3
import tomllib
from collections.abc import Generator, Iterable, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any, cast

_CONFIG_FILE = Path(__file__).resolve().parents[2] / "config.toml"


def _load_config() -> dict[str, str | Path]:
    fallback_path = Path(__file__).resolve().parent.parent / "cinema.db"
    if _CONFIG_FILE.is_file():
        try:
            with _CONFIG_FILE.open("rb") as f:
                data = tomllib.load(f)
            database_section = data.get("database")
            if isinstance(database_section, dict):
                path_value = database_section.get("path")
                if isinstance(path_value, str):
                    configured_path = Path(path_value)
                    if not configured_path.is_absolute():
                        configured_path = _CONFIG_FILE.parent / configured_path
                    return {"path": configured_path}
        except (tomllib.TOMLDecodeError, OSError):
            return {"path": fallback_path}
    return {"path": fallback_path}


_CONFIG: dict[str, str | Path] = _load_config()


def set_db_path(db_path: str | Path) -> None:
    _CONFIG["path"] = db_path


def get_db_path() -> str | Path:
    env_path = os.getenv("CINEMA_DB_PATH")
    if env_path:
        return env_path
    return _CONFIG["path"]


def get_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    target_path = db_path if db_path is not None else get_db_path()
    conn = sqlite3.connect(str(target_path), timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def db_transaction(
    db_path: str | Path | None = None,
) -> Generator[sqlite3.Connection]:
    conn = get_connection(db_path)
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def execute_query(
    sql: str,
    params: Sequence[Any] = (),
    db_path: str | Path | None = None,
) -> list[sqlite3.Row]:
    with db_transaction(db_path) as conn:
        cursor = conn.execute(sql, params)
        return cast(list[sqlite3.Row], cursor.fetchall())


def execute_query_one(
    sql: str,
    params: Sequence[Any] = (),
    db_path: str | Path | None = None,
) -> sqlite3.Row | None:
    with db_transaction(db_path) as conn:
        cursor = conn.execute(sql, params)
        return cast(sqlite3.Row | None, cursor.fetchone())


def execute_write(
    sql: str,
    params: Sequence[Any] = (),
    db_path: str | Path | None = None,
) -> sqlite3.Cursor:
    with db_transaction(db_path) as conn:
        return conn.execute(sql, params)


def execute_write_many(
    sql: str,
    seq_of_params: Iterable[Sequence[Any]],
    db_path: str | Path | None = None,
) -> sqlite3.Cursor:
    with db_transaction(db_path) as conn:
        return conn.executemany(sql, seq_of_params)


def init_db(db_path: str | Path | None = None) -> None:
    with db_transaction(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS filmes (
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                data_estreia TEXT NOT NULL,
                data_saida TEXT NOT NULL,
                duracao INTEGER NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS salas (
                numero INTEGER PRIMARY KEY,
                capacidade INTEGER NOT NULL,
                tipo TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tipos_ingresso (
                tipo TEXT PRIMARY KEY,
                valor INTEGER NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessoes (
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_sala INTEGER NOT NULL,
                codigo_filme INTEGER NOT NULL,
                data TEXT NOT NULL,
                hora_inicio INTEGER NOT NULL,
                FOREIGN KEY (numero_sala) REFERENCES salas(numero) ON DELETE RESTRICT,
                FOREIGN KEY (codigo_filme) REFERENCES filmes(codigo) ON DELETE RESTRICT
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS assentos (
                codigo_sessao INTEGER NOT NULL,
                numero_assento INTEGER NOT NULL,
                ocupado INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (codigo_sessao, numero_assento),
                FOREIGN KEY (codigo_sessao) REFERENCES sessoes(codigo) ON DELETE CASCADE
            );
        """)


def reset_db(db_path: str | Path | None = None) -> None:
    with db_transaction(db_path) as conn:
        conn.execute("DELETE FROM assentos;")
        conn.execute("DELETE FROM sessoes;")
        conn.execute("DELETE FROM tipos_ingresso;")
        conn.execute("DELETE FROM salas;")
        conn.execute("DELETE FROM filmes;")
        conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('filmes', 'sessoes');")
