# reciTAL — Technical Test Boilerplate

A deliberately small full-stack application that mirrors our production stack.
You will extend it during the technical test.

If you are the **candidate**, read **[CANDIDATE.md](./CANDIDATE.md)** — it explains
how to run the project and what you are asked to build.

---

## Stack

| Layer      | Technology                         | Why it is here                                              |
| ---------- | ---------------------------------- | ---------------------------------------------------------- |
| Frontend   | Vue 3 + Vuetify 3 + Vite           | Same framework and component library as our real UI.       |
| API        | FastAPI (Python 3.12)              | Same framework as our backend services.                    |
| Database   | PostgreSQL 16                      | Our primary datastore.                                     |
| Tasks      | Celery worker                      | How we run work that is too slow for a request.            |
| Broker     | Redis                              | Celery broker + result backend.                            |
| Orchestr.  | Docker Compose                     | One command brings the whole thing up.                     |

## Run it

```bash
docker compose up --build
```

Then open:

- UI: http://localhost:5173
- API docs (Swagger): http://localhost:8000/docs
- API health: http://localhost:8000/api/health

The first run builds the images and seeds the database with demo data. Stop with
`Ctrl-C`; wipe everything (including the database) with `docker compose down -v`.

## What is in the box

```
backend/
  app/
    core/        config.py (settings) + database.py (engine/session)
    models/      SQLAlchemy ORM models           (one file per table)
    schemas/     Pydantic request/response models
    crud/        data-access functions           (queries live here, not in routers)
    routers/     FastAPI endpoints               (thin HTTP layer)
    tasks/       Celery tasks                     (example.py is a template)
    worker.py    Celery application
    main.py      FastAPI application entrypoint
frontend/
  src/
    api/         axios client (one shared instance)
    components/
      SideBar.vue
      common/    DataTable.vue, PageHeader.vue   (reused across pages)
    views/       one file per page
    router/      route table
    locales/     en.json / fr.json   (UI translations)
    plugins/     vuetify (theme/brand colours) + i18n (vue-i18n)
docker-compose.yml
```

The app ships with two pages: **Users** (a table backed by the API) and
**Settings** (switches the interface language between English and French). The UI
is localized with `vue-i18n` — strings live in `src/locales/*.json` and are read
with `t('...')`, never hard-coded. These pages are intentionally simple: they show
you the conventions to follow.

## How the pieces talk

```
Browser ──HTTP──> FastAPI (api) ──SQL──> PostgreSQL
                      │
                      └──enqueue──> Redis ──> Celery (worker) ──> PostgreSQL
                                                     │
                                                     └─ writes files to the shared `media` volume
                                                        which the api serves at /media
```
