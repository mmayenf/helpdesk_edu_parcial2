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

pip install -r requirements.txt
python -m pytest -v

Flujo de ramas (control de versiones)

main         <- solo avanza mediante Pull Request revisado
  ^
  | PR
developer    <- rama de integracion continua
  ^
  |-- feature/etiquetas-encapsuladas
  |-- feature/observadores-watchers
  |-- feature/excepciones-polimorfismo
  |-- feature/sql-integridad-referencial
  |-- feature/agregacion-sqlalchemy

Cada ejercicio se desarrollo en su propia rama feature/*, con commits
descriptivos, y se integro a developer mediante merge (--no-ff),
conservando el historial de cada ejercicio. developer llega a main
unicamente a traves de un Pull Request revisado (RNF-05).

Historial del proyecto

Cada incremento se desarrollo en su propia rama feature/*, con commits
descriptivos, y se integro a developer mediante merge (--no-ff) para
conservar el historial de cada ejercicio. Luego developer se integro a
main mediante Pull Request.
