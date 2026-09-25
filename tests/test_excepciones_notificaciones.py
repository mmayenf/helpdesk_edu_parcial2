"""Pruebas del Ejercicio 3: Excepciones y polimorfismo (SERIE II)."""

import pytest

from app.domain.errors import DomainError, DuplicateAssignmentError
from app.services.notifications import WebhookNotifier
from app.services.tickets import TicketService
from app.services.users import UserService


def build_service(notifier=None):
    users = UserService()
    technician = users.register("Carlos Diaz", "carlos@edu.com", role="TECHNICIAN")
    tickets = TicketService(users=users, notifier=notifier)
    ticket = tickets.create(
        title="No enciende",
        description="El equipo no enciende",
        category="Hardware",
        priority="High",
        requester_id=users.register("Ana Lopez", "ana@edu.com").id,
    )
    return tickets, ticket, technician


def test_duplicate_assignment_error_es_domain_error():
    assert issubclass(DuplicateAssignmentError, DomainError)


def test_assign_rechaza_reasignacion_al_mismo_tecnico():
    notifier = WebhookNotifier()
    tickets, ticket, technician = build_service(notifier=notifier)

    tickets.assign(ticket.id, technician.id)  # primera asignacion, valida

    with pytest.raises(DuplicateAssignmentError):
        tickets.assign(ticket.id, technician.id)  # reasignacion, rechazada


def test_reasignacion_rechazada_no_tiene_efectos_secundarios():
    notifier = WebhookNotifier()
    tickets, ticket, technician = build_service(notifier=notifier)

    tickets.assign(ticket.id, technician.id)
    comentarios_antes = list(ticket.comments)
    notificaciones_antes = list(notifier.sent_payloads)

    with pytest.raises(DuplicateAssignmentError):
        tickets.assign(ticket.id, technician.id)

    assert ticket.comments == comentarios_antes
    assert notifier.sent_payloads == notificaciones_antes
    assert ticket.assignee_id == technician.id  # no cambio


def test_assign_valido_notifica_con_el_payload_correcto():
    notifier = WebhookNotifier()
    tickets, ticket, technician = build_service(notifier=notifier)

    tickets.assign(ticket.id, technician.id)

    assert len(notifier.sent_payloads) == 1
    payload = notifier.sent_payloads[0]
    assert payload == {
        "event": "ticket_assigned",
        "ticket_id": ticket.id,
        "technician_id": technician.id,
    }


def test_assign_sin_notifier_no_falla():
    tickets, ticket, technician = build_service(notifier=None)

    # No debe lanzar ninguna excepcion aunque no haya notifier inyectado.
    result = tickets.assign(ticket.id, technician.id)

    assert result.assignee_id == technician.id
