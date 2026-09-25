"""Pruebas del Ejercicio 2: Observadores y relaciones entre objetos (SERIE II)."""

import pytest

from app.domain.errors import NotFoundError
from app.services.tickets import TicketService
from app.services.users import UserService


def build_service():
    users = UserService()
    tickets = TicketService(users=users)
    return tickets, users


def test_watchers_solo_solicitante_sin_tecnico():
    tickets, users = build_service()
    requester = users.register("Ana Lopez", "ana@edu.com")

    ticket = tickets.create(
        title="No enciende",
        description="El equipo no enciende",
        category="Hardware",
        priority="High",
        requester_id=requester.id,
    )

    result = tickets.watchers(ticket.id)

    assert result == [requester]


def test_watchers_solicitante_y_tecnico_distintos():
    tickets, users = build_service()
    requester = users.register("Ana Lopez", "ana@edu.com")
    technician = users.register("Carlos Diaz", "carlos@edu.com", role="TECHNICIAN")

    ticket = tickets.create(
        title="No enciende",
        description="El equipo no enciende",
        category="Hardware",
        priority="High",
        requester_id=requester.id,
    )
    tickets.assign_technician(ticket.id, technician.id)

    result = tickets.watchers(ticket.id)

    assert result == [requester, technician]


def test_watchers_propaga_error_de_ticket_inexistente():
    tickets, _ = build_service()

    with pytest.raises(NotFoundError):
        tickets.watchers(999)


def test_watchers_deduplica_cuando_solicitante_es_tambien_tecnico():
    tickets, users = build_service()
    same_person = users.register("Ana Lopez", "ana@edu.com", role="TECHNICIAN")

    ticket = tickets.create(
        title="Consulta interna",
        description="El propio tecnico reporta su equipo",
        category="Software",
        priority="Low",
        requester_id=same_person.id,
    )
    tickets.assign_technician(ticket.id, same_person.id)

    result = tickets.watchers(ticket.id)

    assert result == [same_person]
    assert len({w.id for w in result}) == len(result)
