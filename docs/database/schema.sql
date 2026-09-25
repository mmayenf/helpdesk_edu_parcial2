-- Esquema de referencia para HelpDesk EDU (PostgreSQL).
-- Sirve de base para docs/database/queries_parcial2.sql. Si tu proyecto
-- ya tiene un esquema propio (por ejemplo con nombres de tabla distintos),
-- ajusta los nombres en las consultas segun corresponda.

CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(150) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE,
    role        VARCHAR(30)  NOT NULL DEFAULT 'REQUESTER'
);

CREATE TABLE IF NOT EXISTS tickets (
    id            SERIAL PRIMARY KEY,
    title         VARCHAR(200) NOT NULL,
    description   TEXT NOT NULL,
    category      VARCHAR(100) NOT NULL,
    priority      VARCHAR(20)  NOT NULL,
    status        VARCHAR(20)  NOT NULL DEFAULT 'Open',
    requester_id  INTEGER NOT NULL REFERENCES users(id),
    assignee_id   INTEGER REFERENCES users(id),
    created_at    TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS comments (
    id          SERIAL PRIMARY KEY,
    ticket_id   INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    author_id   INTEGER NOT NULL REFERENCES users(id),
    text        TEXT NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT now()
);

-- Historial de cambios de un ticket (estado, prioridad, asignacion, etc.).
-- ON DELETE CASCADE: si se borra el ticket, su historial se borra con el
-- (integridad referencial), lo que se demuestra en queries_parcial2.sql.
CREATE TABLE IF NOT EXISTS ticket_history (
    id          SERIAL PRIMARY KEY,
    ticket_id   INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    field       VARCHAR(50) NOT NULL,
    old_value   VARCHAR(200),
    new_value   VARCHAR(200),
    changed_at  TIMESTAMP NOT NULL DEFAULT now()
);
