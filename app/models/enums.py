from enum import Enum


class TicketStatus(str, Enum):
    """Estados posibles de un ticket a lo largo de su ciclo de vida."""

    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

    @classmethod
    def from_value(cls, value: "str | TicketStatus") -> "TicketStatus":
        """Normaliza un string (o un TicketStatus ya existente) a TicketStatus.

        Permite que el usuario del servicio escriba "open", "OPEN" o
        TicketStatus.OPEN indistintamente.
        """
        if isinstance(value, cls):
            return value

        normalized = str(value).strip().lower().replace("_", " ")
        for status in cls:
            if status.value.lower() == normalized:
                return status

        raise ValueError(f"Estado de ticket invalido: {value!r}")
