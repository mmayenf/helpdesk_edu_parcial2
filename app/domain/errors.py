"""Jerarquia de excepciones de dominio para HelpDesk EDU.

Todas las reglas de negocio (validacion, busquedas fallidas, conflictos
de asignacion, etc.) se comunican mediante subclases de DomainError en
lugar de excepciones genericas de Python. Esto permite que las capas
superiores (UI, API) distingan errores de negocio de errores de
programacion mediante polimorfismo, sin condicionales por tipo.
"""


class DomainError(Exception):
    """Error base para cualquier violacion de una regla de negocio."""


class ValidationError(DomainError):
    """Un dato de entrada no cumple las reglas de validacion del dominio.

    Ejemplo: una etiqueta vacia, un correo invalido, un estado que no
    pertenece a los valores permitidos.
    """


class NotFoundError(DomainError):
    """La entidad solicitada (ticket, usuario, etc.) no existe."""


class DuplicateAssignmentError(DomainError):
    """Se intento asignar un ticket al mismo tecnico que ya lo tiene.

    Se lanza antes de modificar el historial del ticket o de emitir
    notificaciones, de forma que la operacion rechazada no tenga
    efectos secundarios.
    """
