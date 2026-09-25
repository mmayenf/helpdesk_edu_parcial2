from dataclasses import dataclass, field

from app.domain.errors import ValidationError
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
    _tags: list[str] = field(default_factory=list, init=False, repr=False)

    @property
    def tags(self) -> tuple[str, ...]:
        """Etiquetas del ticket como tupla de solo lectura.

        No expone la lista interna directamente: quien llame a `tags`
        recibe una copia inmutable, por lo que no puede mutar
        `_tags` desde afuera.
        """
        return tuple(self._tags)

    def add_tag(self, tag: str) -> None:
        """Agrega una etiqueta al ticket, validando y normalizando.

        - Normaliza con strip().lower() para evitar duplicados por
          mayusculas o espacios ("Urgente" y " urgente " son la misma).
        - Rechaza valores vacios (o solo espacios) con ValidationError.
        - Ignora silenciosamente una etiqueta que ya existe (sin
          duplicados), en lugar de lanzar error, ya que agregar dos
          veces la misma etiqueta es una operacion idempotente.
        """
        normalized = tag.strip().lower()
        if not normalized:
            raise ValidationError("La etiqueta no puede estar vacia.")
        if normalized not in self._tags:
            self._tags.append(normalized)
