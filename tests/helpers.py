"""Test utilities and state management helpers."""

from src.model.database import reset_db


def reiniciar_estado() -> None:
    reset_db()
