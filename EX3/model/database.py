"""Database connection and table initialization for SQLite."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DEFAULT_DB_FILE = Path(__file__).resolve().parent.parent / "cinema.db"
_CONFIG: dict[str, str | Path] = {"path": DEFAULT_DB_FILE}


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


def init_db(db_path: str | Path | None = None) -> None:
    conn = get_connection(db_path)
    with conn:
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
    conn.close()


def reset_db(db_path: str | Path | None = None) -> None:
    conn = get_connection(db_path)
    with conn:
        conn.execute("DELETE FROM assentos;")
        conn.execute("DELETE FROM sessoes;")
        conn.execute("DELETE FROM tipos_ingresso;")
        conn.execute("DELETE FROM salas;")
        conn.execute("DELETE FROM filmes;")
        conn.execute("DELETE FROM sqlite_sequence WHERE name IN ('filmes', 'sessoes');")
    conn.close()
