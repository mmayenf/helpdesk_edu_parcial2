# HelpDesk EDU

Sistema de gestion de tickets de soporte tecnico (proyecto integrador de
Programacion II). Organizado en tres capas independientes:

```
app/
  domain/        Jerarquia de excepciones de negocio (DomainError y subclases)
  models/        Entidades: User, Ticket, Comment (dataclasses con encapsulamiento)
  services/      Logica de negocio: TicketService, UserService, notificaciones
  repositories/  Persistencia: TicketRepository (abstracta) y su implementacion SQLAlchemy
docs/
  database/      Esquema y consultas SQL (PostgreSQL)
tests/           Pruebas unitarias (pytest)
```

## Requisitos

- Python 3.11+
- `pip install -r requirements.txt`

## Ejecutar las pruebas

```bash
pip install -r requirements.txt
python -m pytest -v
```

## Historial del proyecto

- **Semana 9** (`chore: baseline semana 9`): consultas en memoria
  (`list_by_technician`, `list_by_category`, `list_by_status`).
- **SERIE II** (ver `README_parcial2.md`): encapsulamiento de etiquetas,
  observadores, excepciones/polimorfismo, SQL con integridad referencial,
  y persistencia con SQLAlchemy.

Cada incremento se desarrollo en su propia rama `feature/*`, con commits
descriptivos, y se integro a `main` mediante merge (`--no-ff`) para
conservar el historial de cada ejercicio.
