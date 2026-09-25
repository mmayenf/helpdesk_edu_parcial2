"""Pruebas del Ejercicio 5: Consulta agregada y persistencia con SQLAlchemy (SERIE II)."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.repositories.sqlalchemy import Base, SqlAlchemyTicketRepository, TicketORM


def new_engine():
    """Crea un engine SQLite en memoria compartido entre sesiones.

    StaticPool asegura que todas las conexiones usen la MISMA base en
    memoria (por defecto, cada conexion SQLite ':memory:' tendria su
    propia base vacia).
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine


def test_count_by_status_con_tres_tickets_en_dos_estados():
    engine = new_engine()

    # --- Sesion 1: se crean e insertan los tickets, y se confirma. ---
    with Session(engine) as session:
        repo = SqlAlchemyTicketRepository(session)
        repo.add(TicketORM(
            title="No imprime", description="...", category="Hardware",
            priority="Medium", status="Open", requester_id=1,
        ))
        repo.add(TicketORM(
            title="No enciende", description="...", category="Hardware",
            priority="High", status="Open", requester_id=2,
        ))
        repo.add(TicketORM(
            title="Error de login", description="...", category="Software",
            priority="Low", status="Resolved", requester_id=3,
        ))
        session.commit()
    # La sesion se cierra aqui (fin del bloque `with`).

    # --- Sesion 2: nueva sesion, mismo engine; se consulta el reporte. ---
    with Session(engine) as session:
        repo = SqlAlchemyTicketRepository(session)
        report = repo.count_by_status()

    assert report == {"Open": 2, "Resolved": 1}
    assert sum(report.values()) == 3


def test_count_by_status_devuelve_diccionario_vacio_sin_tickets():
    # Base de prueba independiente: engine nuevo, sin ningun ticket.
    engine = new_engine()

    with Session(engine) as session:
        repo = SqlAlchemyTicketRepository(session)
        report = repo.count_by_status()

    assert report == {}


def test_count_by_status_solo_incluye_estados_presentes():
    engine = new_engine()

    with Session(engine) as session:
        repo = SqlAlchemyTicketRepository(session)
        repo.add(TicketORM(
            title="No imprime", description="...", category="Hardware",
            priority="Medium", status="Open", requester_id=1,
        ))
        session.commit()

    with Session(engine) as session:
        repo = SqlAlchemyTicketRepository(session)
        report = repo.count_by_status()

    assert report == {"Open": 1}
    assert "Closed" not in report
