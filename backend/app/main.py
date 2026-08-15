"""FastAPI application entrypoint.

Run with:
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import models  # noqa: F401  (registers models on Base.metadata)
from app.core.config import settings
from app.core.database import Base, engine
from app.routers import users
from app.seed import seed


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # For a boilerplate we create tables directly. A real service would use
    # Alembic migrations instead.
    Base.metadata.create_all(bind=engine)
    os.makedirs(settings.media_dir, exist_ok=True)
    seed()
    yield


app = FastAPI(title="reciTAL Boilerplate API", lifespan=lifespan)

# The SPA runs on a different origin (localhost:5173) so we allow CORS. Wide-open
# here because it is a local dev boilerplate.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generated files (e.g. PDF thumbnails) are served from /media.
os.makedirs(settings.media_dir, exist_ok=True)
app.mount("/media", StaticFiles(directory=settings.media_dir), name="media")

app.include_router(users.router)


@app.get("/api/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
