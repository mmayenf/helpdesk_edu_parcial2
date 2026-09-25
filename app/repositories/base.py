"""Contrato abstracto de persistencia para tickets.

Esta interfaz define las operaciones basicas que cualquier motor de
almacenamiento (SQLAlchemy, un mock en memoria para pruebas, etc.) debe
implementar. No incluye operaciones especificas de un motor (como
reportes de agregacion): esas se agregan solo en la implementacion
concreta que las necesite, sin ensuciar el contrato abstracto.
"""

from abc import ABC, abstractmethod
from typing import Any


class TicketRepository(ABC):
    """Operaciones minimas de persistencia para tickets."""

    @abstractmethod
    def add(self, ticket: Any) -> None:
        """Agrega un ticket (aun no confirmado) al repositorio."""

    @abstractmethod
    def get(self, ticket_id: int) -> Any | None:
        """Devuelve el ticket con ticket_id, o None si no existe."""

    @abstractmethod
    def list_all(self) -> list[Any]:
        """Devuelve todos los tickets almacenados."""
