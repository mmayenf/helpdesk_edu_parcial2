-- ============================================================
-- SERIE II - Ejercicio 4: SQL e integridad referencial
-- Motor objetivo: PostgreSQL
-- Esquema de referencia: docs/database/schema.sql
-- ============================================================


-- (a) Tickets abiertos con el nombre del solicitante (JOIN)
-- ------------------------------------------------------------
SELECT
    t.id,
    t.title,
    t.status,
    u.name AS requester_name
FROM tickets t
JOIN users u ON u.id = t.requester_id
WHERE t.status = 'Open'
ORDER BY t.id;


-- (b) Conteo de tickets por tecnico asignado
-- ------------------------------------------------------------
-- Agrupado por id y nombre del tecnico; HAVING excluye tecnicos con
-- conteo cero (es decir, sin tickets asignados) y se ordena de mayor
-- a menor carga de trabajo.
SELECT
    u.id            AS technician_id,
    u.name          AS technician_name,
    COUNT(t.id)     AS ticket_count
FROM users u
JOIN tickets t ON t.assignee_id = u.id
GROUP BY u.id, u.name
HAVING COUNT(t.id) > 0
ORDER BY ticket_count DESC;


-- (c) Tickets sin comentarios (NOT EXISTS)
-- ------------------------------------------------------------
SELECT
    t.id,
    t.title
FROM tickets t
WHERE NOT EXISTS (
    SELECT 1
    FROM comments c
    WHERE c.ticket_id = t.id
)
ORDER BY t.id;

-- Version equivalente con LEFT JOIN, por si se prefiere comparar planes:
-- SELECT t.id, t.title
-- FROM tickets t
-- LEFT JOIN comments c ON c.ticket_id = t.id
-- WHERE c.id IS NULL
-- ORDER BY t.id;


-- (d) Demostracion de ON DELETE CASCADE sobre ticket_history,
--     dentro de una transaccion revertida con ROLLBACK.
-- ------------------------------------------------------------
-- Reemplaza :ticket_id_con_historial por el id de un ticket que ya
-- tenga al menos un registro en ticket_history antes de ejecutar.

BEGIN;

-- 1) Conteo inicial: debe ser mayor que cero.
SELECT COUNT(*) AS historial_inicial
FROM ticket_history
WHERE ticket_id = :ticket_id_con_historial;

-- 2) Se borra el ticket; por ON DELETE CASCADE, su historial
--    tambien se borra automaticamente.
DELETE FROM tickets
WHERE id = :ticket_id_con_historial;

-- 3) Conteo tras el DELETE: debe ser cero (la cascada funciono).
SELECT COUNT(*) AS historial_tras_delete
FROM ticket_history
WHERE ticket_id = :ticket_id_con_historial;

-- 4) Se revierte todo: ni el ticket ni su historial deberian
--    haberse borrado realmente.
ROLLBACK;

-- 5) Conteo despues del ROLLBACK: debe volver a ser igual al inicial.
SELECT COUNT(*) AS historial_tras_rollback
FROM ticket_history
WHERE ticket_id = :ticket_id_con_historial;
