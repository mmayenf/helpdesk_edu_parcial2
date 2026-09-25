"""Implementacion de TicketRepository sobre SQLAlchemy.

Incluye el mapeo ORM (TicketORM) y count_by_status(), un reporte de
agregacion que es especifico de este motor y por eso no forma parte
de la interfaz abstracta TicketRepository (ver app/repositories/base.py).
"""

from __future__ import annotations

from sqlalchemy import Integer, String, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from app.repositories.base import TicketRepository


class Base(DeclarativeBase):
    pass


class TicketORM(Base):
    """Mapeo de la tabla `tickets` para persistencia con SQLAlchemy."""

    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(2000))
    category: Mapped[str] = mapped_column(String(100))
    priority: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20))
    requester_id: Mapped[int] = mapped_column(Integer)
    assignee_id: Mapped[int | None] = mapped_column(Integer, nullable=True)


class SqlAlchemyTicketRepository(TicketRepository):
    """TicketRepository respaldado por una sesion de SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, ticket: TicketORM) -> None:
        self._session.add(ticket)

    def get(self, ticket_id: int) -> TicketORM | None:
        return self._session.get(TicketORM, ticket_id)

    def list_all(self) -> list[TicketORM]:
        return list(self._session.scalars(select(TicketORM)))

    def count_by_status(self) -> dict[str, int]:
        """Reporte de tickets agrupados por estado.

        Usa select(status, count()).group_by(status) directamente sobre
        la base de datos (no en Python), devolviendo solo los estados
        que efectivamente tienen tickets. Si la tabla esta vacia,
        devuelve {} en lugar de fallar.
        """
        rows = self._session.execute(
            select(TicketORM.status, func.count()).group_by(TicketORM.status)
        ).all()
        return {status: count for status, count in rows}
