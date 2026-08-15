"""Example Celery task — a template to copy.

The point of this file is to show the pattern: anything that takes more than a
fraction of a second (network calls, parsing a file, rendering an image, talking
to a slow third party) must NOT run inside a request handler, because it would
block the API worker and time out the browser. Push it to a task instead and let
the `worker` container do the work.

A task can open its own DB session (it runs in a different process from the API,
so it cannot reuse the request's session):

    from app.core.database import SessionLocal

    @celery_app.task(name="...")
    def my_task(...):
        db = SessionLocal()
        try:
            ...
            db.commit()
        finally:
            db.close()
"""

import time

from app.worker import celery_app


@celery_app.task(name="example.slow_job")
def slow_job(seconds: int = 5) -> str:
    """Pretend to do something slow. Returns once it is done."""
    time.sleep(seconds)
    return f"done after {seconds}s"
