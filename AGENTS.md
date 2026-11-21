# Innovart Digital — FastAPI REST API

Spanish-language ("mensaje", etc.) API for Usuarios, Roles, Personas, Empleados, Servicios, Agenda, ServicioAgenda, Pagos, Consultas y Respuestas. FastAPI + Pydantic for automatic OpenAPI/Swagger, SQLAlchemy 2.0 ORM (PyMySQL driver) for persistence. Tables are declared as ORM models in `Models/` (one file per entity) and created idempotently on startup with `Base.metadata.create_all`.

## Setup (do first, every time)

1. `cp .env.example .env` — `.env` is gitignored and does not exist in the repo; you must create it.
2. `.venv/` already exists: `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`).
3. `pip install -r requirements.txt` — FastAPI, Uvicorn, SQLAlchemy, PyMySQL, python-dotenv, Werkzeug.
4. You need a running MySQL server (no SQLite fallback). Set credentials in `.env`. The API creates the database and tables on startup if they do not exist; the configured user still needs permission to create them.

## Run

- `python app.py` — main entrypoint, reads `PORT` (default `5000`) and `DEBUG`.
- `uvicorn app:app --reload` — equivalent development command.
- Swagger UI: `http://127.0.0.1:5000/docs`; ReDoc: `/redoc`; OpenAPI JSON: `/openapi.json`.
- `/health` — verifica estado de la API y conexión a MySQL (`200` si OK, `503` si la BD está caída).

### Docker Compose

- `docker compose up -d --build` — levanta MySQL (`db`) y la API (`api`). Lee variables de `.env`.
- `docker compose logs -f api` — logs de la API.
- `docker compose down` — detiene; `docker compose down -v` también borra datos de MySQL.
- La API crea la base con `CREATE DATABASE IF NOT EXISTS` y las tablas con `Base.metadata.create_all`, por lo que funciona tanto con volúmenes nuevos como existentes.
- El volumen `mysql_data` es persistente.
- Dentro del contenedor, `MYSQL_HOST=db` (nombre del servicio, no `localhost`).

## Architecture (request flow)

- `app.py` — crea la aplicación FastAPI, configura CORS, registra `/health`, las redirecciones de documentación y los routers.
- `Models/` — un archivo por entidad con el modelo ORM de SQLAlchemy (tabla, columnas, claves foráneas y restricciones).
- `Models/Base.py` — base declarativa (`Base`) y opciones comunes de tabla (`table_options`).
- `Schemas/` — un archivo por entidad con los schemas Pydantic (`XCreate`, `XUpdate`, `XResponse`). `Schemas/Common.py` contiene tipos compartidos.
- `Services/` — un archivo por entidad. `Services/BaseService.py` implementa el CRUD genérico sobre `Session`; `Services/UsuarioService.py` agrega hash de contraseña, login y validación de correo.
- `Routes/` — un archivo por entidad. `Routes/BaseRoutes.py` genera las cinco rutas CRUD estándar; `Routes/__init__.py` agrega todos los routers.
- `Config.py` — variables de entorno.
- `Database.py` — motor SQLAlchemy, `SessionLocal`, dependencia `get_session` y creación idempotente del esquema.

Flujo: Route -> Service -> SQLAlchemy `Session` -> MySQL. FastAPI construye el OpenAPI automáticamente a partir de los schemas Pydantic de `Schemas/`; los response models usan `from_attributes` para serializar las entidades ORM.

## Database quirks

- Tablas en plural y minúsculas (`roles`, `personas`, `usuarios`, `servicios`, etc.) y columnas en minúsculas (`id`, `usuarios_id`, `personas_id`, etc.).
- La columna de contraseña es `contrasena`; se hashea con `werkzeug.security` (`generate_password_hash` / `check_password_hash`) y nunca se devuelve en las respuestas.
- Los UUID se generan en el servidor al crear registros; no se exigen en el cuerpo de la petición.
- El esquema se define una sola vez en `Models/`; no hay `schema.sql` ni migraciones (sin Alembic). `create_all` no altera tablas existentes.
- Los errores de integridad de MySQL se traducen a `409` con mensajes en español (`_integrity_message` en `Services/BaseService.py`).

## What does NOT exist here

- No `tests/` directory, no pytest, no lint/format/typecheck config, no CI workflows, no `ruff`/`mypy`/`flake8`. Do not invent test or lint commands; verify by running the API and hitting endpoints.

## Adding a new entity

1. Add `Models/X.py` with the ORM model.
2. Add `Schemas/X.py` with `XCreate`, `XUpdate`, `XResponse`.
3. Add `Services/XService.py` subclassing `CrudService` with `name` and `model`.
4. Add `Routes/XRoutes.py` using `build_crud_router` with the schemas and the service.
5. Register the router in `Routes/__init__.py`.
6. FastAPI publica automáticamente el nuevo recurso en `/docs`.
