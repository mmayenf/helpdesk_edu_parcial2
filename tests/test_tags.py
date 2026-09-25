"""Pruebas del Ejercicio 1: Etiquetas y encapsulamiento (SERIE II)."""

import pytest

from app.domain.errors import ValidationError
from app.models.entities import Ticket


def make_ticket(id_=1) -> Ticket:
    return Ticket(
        id=id_,
        title="No imprime",
        description="La impresora no responde",
        category="Hardware",
        priority="Medium",
        requester_id=1,
    )


def test_add_tag_normaliza_y_evita_duplicados():
    ticket = make_ticket()

    ticket.add_tag("  Urgente ")
    ticket.add_tag("urgente")  # mismo valor normalizado, no debe duplicar
    ticket.add_tag("Hardware")

    assert ticket.tags == ("urgente", "hardware")


def test_add_tag_rechaza_valores_vacios():
    ticket = make_ticket()

    with pytest.raises(ValidationError):
        ticket.add_tag("   ")

    with pytest.raises(ValidationError):
        ticket.add_tag("")

    # el rechazo no debe dejar residuos en la coleccion interna
    assert ticket.tags == ()


def test_tags_son_independientes_entre_tickets():
    ticket_a = make_ticket(id_=1)
    ticket_b = make_ticket(id_=2)

    ticket_a.add_tag("hardware")

    assert ticket_a.tags == ("hardware",)
    assert ticket_b.tags == ()


def test_tags_no_permite_reasignacion_publica():
    ticket = make_ticket()

    with pytest.raises(AttributeError):
        ticket.tags = ["algo"]


def test_tags_devuelve_tupla_no_lista():
    ticket = make_ticket()
    ticket.add_tag("hardware")

    assert isinstance(ticket.tags, tuple)
