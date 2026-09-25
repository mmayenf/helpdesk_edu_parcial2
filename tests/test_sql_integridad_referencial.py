"""Pruebas del Ejercicio 4: SQL e integridad referencial (SERIE II).

Estas pruebas NO reemplazan la ejecucion en PostgreSQL pedida por el
enunciado (ver docs/database/queries_parcial2.sql y la seccion del
Ejercicio 4 en README_parcial2.md para esa evidencia). Sirven como una
verificacion automatizada y reproducible de la MISMA logica (JOIN,
HAVING, NOT EXISTS y ON DELETE CASCADE dentro de BEGIN/ROLLBACK) usando
SQLite, disponible en cualquier maquina sin instalar un servidor aparte.
"""

import sqlite3

import pytest

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    VARCHAR(150) NOT NULL,
    email   VARCHAR(150) NOT NULL UNIQUE,
    role    VARCHAR(30)  NOT NULL DEFAULT 'REQUESTER'
);

CREATE TABLE tickets (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    title         VARCHAR(200) NOT NULL,
    description   TEXT NOT NULL,
    category      VARCHAR(100) NOT NULL,
    priority      VARCHAR(20)  NOT NULL,
    status        VARCHAR(20)  NOT NULL DEFAULT 'Open',
    requester_id  INTEGER NOT NULL REFERENCES users(id),
    assignee_id   INTEGER REFERENCES users(id)
);

CREATE TABLE comments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id   INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    author_id   INTEGER NOT NULL REFERENCES users(id),
    text        TEXT NOT NULL
);

CREATE TABLE ticket_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id   INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    field       VARCHAR(50) NOT NULL,
    old_value   VARCHAR(200),
    new_value   VARCHAR(200)
);
"""

SEED = """
INSERT INTO users (name, email, role) VALUES
 ('Ana Lopez', 'ana@edu.com', 'REQUESTER'),
 ('Bruno Perez', 'bruno@edu.com', 'REQUESTER'),
 ('Carlos Diaz', 'carlos@edu.com', 'TECHNICIAN'),
 ('Diana Ruiz', 'diana@edu.com', 'TECHNICIAN');

INSERT INTO tickets (title, description, category, priority, status, requester_id, assignee_id) VALUES
 ('No imprime', 'La impresora no responde', 'Hardware', 'Medium', 'Open', 1, 3),
 ('No enciende', 'El equipo no enciende', 'Hardware', 'High', 'Open', 2, 3),
 ('Error de login', 'No puede iniciar sesion', 'Software', 'Low', 'Resolved', 1, 4),
 ('Pantalla azul', 'Falla al iniciar Windows', 'Hardware', 'Critical', 'Open', 2, NULL),
 ('Falta licencia', 'No tiene licencia de Office', 'Software', 'Medium', 'Closed', 1, 4);

INSERT INTO comments (ticket_id, author_id, text) VALUES
 (1, 3, 'Reviso mañana a primera hora'),
 (3, 4, 'Se reseteo la contraseña, resuelto');

INSERT INTO ticket_history (ticket_id, field, old_value, new_value) VALUES
 (1, 'status', 'Open', 'Open'),
 (1, 'assignee_id', NULL, '3'),
 (3, 'status', 'Open', 'Resolved');
"""


@pytest.fixture()
def con():
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SCHEMA)
    connection.executescript(SEED)
    connection.commit()
    yield connection
    connection.close()


def test_a_tickets_abiertos_con_nombre_solicitante(con):
    rows = con.execute("""
        SELECT t.id, t.title, u.name AS requester_name
        FROM tickets t
        JOIN users u ON u.id = t.requester_id
        WHERE t.status = 'Open'
        ORDER BY t.id
    """).fetchall()

    ids = [r[0] for r in rows]
    assert ids == [1, 2, 4]
    assert rows[0][2] == "Ana Lopez"


def test_b_conteo_por_tecnico_excluye_cero_y_ordena_desc(con):
    rows = con.execute("""
        SELECT u.id, u.name, COUNT(t.id) AS ticket_count
        FROM users u
        JOIN tickets t ON t.assignee_id = u.id
        GROUP BY u.id, u.name
        HAVING COUNT(t.id) > 0
        ORDER BY ticket_count DESC
    """).fetchall()

    # Ana y Bruno (solicitantes, no tecnicos) no aparecen: nunca tienen
    # tickets asignados, por lo que su conteo nunca existe en el JOIN.
    technician_ids = {r[0] for r in rows}
    assert technician_ids == {3, 4}
    assert all(count > 0 for _, _, count in rows)


def test_c_tickets_sin_comentarios_via_not_exists(con):
    rows = con.execute("""
        SELECT t.id
        FROM tickets t
        WHERE NOT EXISTS (SELECT 1 FROM comments c WHERE c.ticket_id = t.id)
        ORDER BY t.id
    """).fetchall()

    assert [r[0] for r in rows] == [2, 4, 5]


def test_d_on_delete_cascade_se_revierte_con_rollback(con):
    inicial = con.execute(
        "SELECT COUNT(*) FROM ticket_history WHERE ticket_id = 1"
    ).fetchone()[0]
    assert inicial > 0

    con.execute("BEGIN")
    con.execute("DELETE FROM tickets WHERE id = 1")

    tras_delete = con.execute(
        "SELECT COUNT(*) FROM ticket_history WHERE ticket_id = 1"
    ).fetchone()[0]
    assert tras_delete == 0  # la cascada borro el historial

    con.execute("ROLLBACK")

    tras_rollback = con.execute(
        "SELECT COUNT(*) FROM ticket_history WHERE ticket_id = 1"
    ).fetchone()[0]
    assert tras_rollback == inicial  # todo vuelve a como estaba

    ticket_sigue_existiendo = con.execute(
        "SELECT COUNT(*) FROM tickets WHERE id = 1"
    ).fetchone()[0]
    assert ticket_sigue_existiendo == 1
