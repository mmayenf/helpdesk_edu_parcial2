from dataclasses import dataclass, field

from app.models.enums import TicketStatus


@dataclass
class Comment:
    """Un comentario de seguimiento asociado a un ticket."""

    author_id: int
    text: str


@dataclass
class Ticket:
    """Representa un ticket del sistema HelpDesk EDU.

    Relaciones creadas en la Semana 8:
    - requester_id: quien reporto el ticket (solicitante).
    - assignee_id: tecnico asignado (puede no existir todavia).
    - category: categoria del ticket (ej. Hardware, Software).
    - comments: bitacora de seguimiento del ticket.
    """

    id: int
    title: str
    description: str
    category: str
    priority: str
    requester_id: int
    assignee_id: int | None = None
    status: TicketStatus = TicketStatus.OPEN
    comments: list[Comment] = field(default_factory=list)
