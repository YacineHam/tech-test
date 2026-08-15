"""Celery application.

Run with:
    celery -A app.worker.celery_app worker --loglevel=info

The broker and result backend both point at Redis. Task modules are listed in
``include`` so the worker registers them on startup.
"""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "boilerplate",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.documents", "app.tasks.example"],
)

# Report a task as STARTED (not just PENDING) while it runs, so the UI can show
# progress.
celery_app.conf.task_track_started = True

# Keep retrying the broker connection on startup (Celery 6 default). Setting it
# explicitly silences the pending-deprecation warning and is the behaviour we
# want: the worker may boot before Redis is ready.
celery_app.conf.broker_connection_retry_on_startup = True
