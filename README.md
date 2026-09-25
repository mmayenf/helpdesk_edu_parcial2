# HelpDesk EDU

Sistema de gestion de tickets de soporte tecnico (proyecto integrador de
Programacion II). Organizado en tres capas independientes:


app/
  domain/        Jerarquia de excepciones de negocio (DomainError y subclases)
  models/        Entidades: User, Ticket, Comment (dataclasses con encapsulamiento)
  services/      Logica de negocio: TicketService, UserService, notificaciones
  repositories/  Persistencia: TicketRepository (abstracta) y su implementacion SQLAlchemy
docs/
  database/      Esquema y consultas SQL (PostgreSQL)
tests/           Pruebas unitarias (pytest)


Requisitos

Python 3.11+
pip install -r requirements.txt

Ejecutar las pruebas

bash
pip install -r requirements.txt
python -m pytest -v


Historial del proyecto

Cada incremento se desarrollo en su propia rama feature/*, con commits
descriptivos, y se integro a main mediante merge (--no-ff) para
conservar el historial de cada ejercicio.
