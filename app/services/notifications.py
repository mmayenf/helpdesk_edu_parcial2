"""Contrato de notificaciones y una implementacion simulada (webhook).

TicketService depende solo de la interfaz Notifier (duck typing /
Protocol de Python), nunca de una implementacion concreta. Esto permite
inyectar distintos canales (webhook, email, consola, mock de pruebas)
sin agregar condicionales por tipo dentro de TicketService: es
polimorfismo puro a traves del parametro `notifier`.
"""

from typing import Any, Protocol


class Notifier(Protocol):
    """Cualquier objeto con un metodo notify(event, **kwargs) sirve."""

    def notify(self, event: str, **kwargs: Any) -> None:
        ...


class WebhookNotifier:
    """Notificador simulado: no hace HTTP real ni imprime nada.

    Guarda cada payload enviado en self.sent_payloads, lo que permite
    verificar en las pruebas exactamente que se hubiera enviado a un
    webhook real.
    """

    def __init__(self) -> None:
        self.sent_payloads: list[dict[str, Any]] = []

    def notify(self, event: str, **kwargs: Any) -> None:
        payload: dict[str, Any] = {"event": event, **kwargs}
        self.sent_payloads.append(payload)
