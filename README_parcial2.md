# README_parcial2 — SERIE II (HelpDesk EDU)

Este documento resume como reproducir y verificar cada uno de los 5
ejercicios de la SERIE II, sus resultados y las limitaciones conocidas.

## Estructura de ramas y commits

| Rama | Ejercicio | Commits principales |
|---|---|---|
| `feature/etiquetas-encapsuladas` | 1. Etiquetas y encapsulamiento | `feat(errors): ...`, `feat(ticket): ...` |
| `feature/observadores-watchers` | 2. Observadores y relaciones | `feat(users,tickets): ...` |
| `feature/excepciones-polimorfismo` | 3. Excepciones y polimorfismo | `feat(tickets,notifications): ...` |
| `feature/sql-integridad-referencial` | 4. SQL e integridad referencial | `docs(sql): ...` |
| `feature/agregacion-sqlalchemy` | 5. Consulta agregada y SQLAlchemy | `feat(repositories): ...` |

Cada rama se integro a `main` con `git merge --no-ff`, dejando un commit
de merge visible por ejercicio (`git log --oneline --graph` lo muestra).

## 1. Etiquetas y encapsulamiento

**Archivos:** `app/models/entities.py`, `app/domain/errors.py`

**Reproducir:**
```bash
python -m pytest tests/test_tags.py -v
```

**Resultado:** 5/5 pruebas OK. Se verifica normalizacion (`strip().lower()`),
rechazo de vacios con `ValidationError`, independencia entre instancias de
`Ticket`, y que `ticket.tags = [...]` falla con `AttributeError` (no hay
setter para la propiedad).

**Limitacion:** las etiquetas viven solo en memoria (no hay columna ni
migracion SQL), tal como pide el enunciado.

## 2. Observadores y relaciones entre objetos

**Archivos:** `app/services/tickets.py`, `app/services/users.py` (nuevo)

**Reproducir:**
```bash
python -m pytest tests/test_watchers.py -v
```

**Resultado:** 4/4 pruebas OK. `watchers()` devuelve solicitante + tecnico
asignado sin duplicados, y propaga `NotFoundError` si el ticket no existe.

**Limitacion:** `TicketService` crea su propio `UserService` por defecto
si no se le inyecta uno; en produccion ambos deberian compartir la misma
instancia (o repositorio) para que los ids de usuario sean consistentes.

## 3. Excepciones y polimorfismo

**Archivos:** `app/domain/errors.py`, `app/services/tickets.py`, `app/services/notifications.py` (nuevo)

**Reproducir:**
```bash
python -m pytest tests/test_excepciones_notificaciones.py -v
```

**Resultado:** 5/5 pruebas OK. `assign()` rechaza una reasignacion al
mismo tecnico con `DuplicateAssignmentError` sin mutar el ticket ni
notificar; una asignacion valida si notifica, con el payload correcto
capturado en `WebhookNotifier.sent_payloads`.

**Limitacion:** no se implemento un historial de auditoria persistente
(la validacion de "no duplicar" usa el estado actual de `assignee_id`,
no un log completo de asignaciones pasadas).

## 4. SQL e integridad referencial

**Archivos:** `docs/database/schema.sql`, `docs/database/queries_parcial2.sql`

**Reproducir (en tu propia instancia de PostgreSQL):**
```bash
psql -U <usuario> -d <basededatos> -f docs/database/schema.sql
# cargar datos de prueba propios...
psql -U <usuario> -d <basededatos> -f docs/database/queries_parcial2.sql
```

Para la consulta (d), reemplaza el parametro `:ticket_id_con_historial`
por el id de un ticket que ya tenga filas en `ticket_history` antes de
ejecutar el bloque `BEGIN ... ROLLBACK`.

**Resultado:** *(pendiente — completar con la salida real de tu
PostgreSQL: pega aqui aqui los conteos de las 4 consultas, en particular
el conteo inicial > 0, el conteo tras `DELETE` = 0, y el conteo tras
`ROLLBACK` = valor original)*.

**Limitacion:** este entorno de desarrollo no tiene un servidor
PostgreSQL disponible para generar la evidencia automaticamente; las
consultas estan escritas y documentadas, pero la ejecucion y captura de
salida debe hacerse manualmente contra la base de datos del proyecto.

## 5. Consulta agregada y persistencia con SQLAlchemy

**Archivos:** `app/repositories/base.py` (nuevo), `app/repositories/sqlalchemy.py` (nuevo)

**Reproducir:**
```bash
python -m pytest tests/test_sqlalchemy_repository.py -v
```

**Resultado:** 3/3 pruebas OK. `count_by_status()` devuelve el
diccionario correcto (`{"Open": 2, "Resolved": 1}` con 3 tickets en dos
estados), la suma coincide con el total de tickets, y una base vacia
devuelve `{}`. Se prueba con SQLite en memoria + `StaticPool` para
compartir el mismo engine entre la sesion que inserta (con `commit()`) y
la sesion nueva que consulta el reporte.

**Limitacion:** `count_by_status()` se agrego solo a
`SqlAlchemyTicketRepository`, no a la interfaz abstracta
`TicketRepository` (es un reporte especifico de este motor). Las
pruebas usan SQLite en vez de PostgreSQL por practicidad; la consulta
(`select(...).group_by(...)`) es estandar SQL y deberia comportarse
igual en Postgres.

## Resumen de pruebas

```bash
python -m pytest -v
```

23/23 pruebas pasando (6 de la Semana 9 + 17 nuevas de la SERIE II). Ver
`evidencia_pytest.txt` para la salida completa.
