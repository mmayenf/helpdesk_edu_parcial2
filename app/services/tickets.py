from app.models.entities import Comment, Ticket
from app.models.enums import TicketStatus


class TicketService:
    """Servicio de tickets del sistema HelpDesk EDU."""

    def __init__(self) -> None:
        self._tickets: list[Ticket] = []
        self._next_id: int = 1

    # ------------------------------------------------------------------
    # Codigo de semanas anteriores (creacion y relaciones)
    # ------------------------------------------------------------------
    def create(
        self,
        title: str,
        description: str,
        category: str,
        priority: str,
        requester_id: int,
    ) -> Ticket:
        """Crea un nuevo ticket en estado Open, reportado por requester_id."""
        ticket = Ticket(
            id=self._next_id,
            title=title,
            description=description,
            category=category,
            priority=priority,
            requester_id=requester_id,
            status=TicketStatus.OPEN,
        )
        self._tickets.append(ticket)
        self._next_id += 1
        return ticket

    def assign_technician(self, ticket_id: int, technician_id: int) -> Ticket:
        """Asigna un tecnico a un ticket existente."""
        ticket = self._get_ticket_or_raise(ticket_id)
        ticket.assignee_id = technician_id
        return ticket

    def add_comment(self, ticket_id: int, author_id: int, text: str) -> Ticket:
        """Agrega un comentario de seguimiento al ticket."""
        ticket = self._get_ticket_or_raise(ticket_id)
        ticket.comments.append(Comment(author_id=author_id, text=text))
        return ticket

    def update_status(self, ticket_id: int, status: str | TicketStatus) -> Ticket:
        """Actualiza el estado del ticket, normalizando el valor recibido."""
        ticket = self._get_ticket_or_raise(ticket_id)
        ticket.status = TicketStatus.from_value(status)
        return ticket

    def _get_ticket_or_raise(self, ticket_id: int) -> Ticket:
        for ticket in self._tickets:
            if ticket.id == ticket_id:
                return ticket
        raise ValueError(f"No existe un ticket con id {ticket_id}")

    # ------------------------------------------------------------------
    # Consultas de la Semana 9
    # ------------------------------------------------------------------
    def list_by_technician(self, technician_id: int) -> list[Ticket]:
        """Que tickets tiene asignados este tecnico?

        Recorre self._tickets y devuelve solo los tickets cuyo
        assignee_id coincida con technician_id.
        """
        return [
            ticket for ticket in self._tickets
            if ticket.assignee_id == technician_id
        ]

    def list_by_category(self, category: str) -> list[Ticket]:
        """Que tickets pertenecen a una categoria (ej. Hardware)?

        Devuelve solo los tickets cuya categoria coincida. La comparacion
        ignora mayusculas/minusculas para evitar fallos por formato.
        """
        return [
            ticket for ticket in self._tickets
            if ticket.category.strip().lower() == category.strip().lower()
        ]

    def list_by_status(self, status: str | TicketStatus) -> list[Ticket]:
        """Que tickets siguen abiertos, en proceso, etc.?

        Normaliza el estado recibido (string o TicketStatus) y devuelve
        solo los tickets que tengan ese estado.
        """
        normalized_status = TicketStatus.from_value(status)
        return [
            ticket for ticket in self._tickets
            if ticket.status == normalized_status
        ]
