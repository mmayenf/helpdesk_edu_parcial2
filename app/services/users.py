from app.domain.errors import NotFoundError
from app.models.entities import User


class UserService:
    """Servicio de usuarios del sistema HelpDesk EDU.

    Mantiene su propia coleccion en memoria. TicketService no accede a
    esta lista directamente: siempre pasa por require(id), igual que
    con cualquier otro repositorio de dominio.
    """

    def __init__(self) -> None:
        self._users: list[User] = []
        self._next_id: int = 1

    def register(self, name: str, email: str, role: str = "REQUESTER") -> User:
        """Registra un nuevo usuario y devuelve la instancia creada."""
        user = User(id=self._next_id, name=name, email=email, role=role)
        self._users.append(user)
        self._next_id += 1
        return user

    def require(self, user_id: int) -> User:
        """Devuelve el usuario con user_id o lanza NotFoundError."""
        for user in self._users:
            if user.id == user_id:
                return user
        raise NotFoundError(f"No existe un usuario con id {user_id}")

    def list(self) -> list[User]:
        return list(self._users)
