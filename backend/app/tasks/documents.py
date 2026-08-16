"""Document processing task.

Reading a PDF and rendering its first page is exactly the kind of work the
example task warns about: too slow for a request handler. The API only saves
the file and creates the row; this task fills in the extracted metadata.

Runs in the worker container, which shares the media volume with the API, so
it reads the uploaded PDF from MEDIA_DIR and writes the thumbnail next to it.
"""

import logging
import os
import time

import pymupdf
import redis
from celery.signals import task_postrun

from app import crud
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.document import STATUS_FAILED, STATUS_READY
from app.worker import celery_app

logger = logging.getLogger(__name__)

_THUMBNAILS_SUBDIR = "thumbnails"

_THUMBNAIL_SCALE = 0.4


@celery_app.task(name="documents.process")
def process_document(document_id: int) -> None:

    db = SessionLocal()
    try:
        document = crud.document.get_document(db, document_id)
        if document is None:
            logger.warning("document %s no longer exists, skipping", document_id)
            return

        time.sleep(3)

        try:
            pdf_path = os.path.join(settings.media_dir, document.file_path)
            with pymupdf.open(pdf_path) as pdf:
                document.number_of_pages = pdf.page_count
                if pdf.page_count > 0:
                    document.thumbnail_path = _render_thumbnail(pdf, document.file_path)
            document.status = STATUS_READY
        except Exception:
            logger.exception("processing failed for document %s", document_id)
            document.status = STATUS_FAILED

        db.commit()
    finally:
        db.close()


def _render_thumbnail(pdf: pymupdf.Document, file_path: str) -> str:
    """Render the first page as a PNG under MEDIA_DIR and return its relative path"""
    stem, _ = os.path.splitext(os.path.basename(file_path))
    relative_path = os.path.join(_THUMBNAILS_SUBDIR, f"{stem}.png")
    destination = os.path.join(settings.media_dir, relative_path)
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    matrix = pymupdf.Matrix(_THUMBNAIL_SCALE, _THUMBNAIL_SCALE)
    pdf[0].get_pixmap(matrix=matrix).save(destination)
    return relative_path


@task_postrun.connect(sender=process_document)
def on_document_complete(sender=None, args=None, **kwargs):
    if args:
        doc_id = args[0]
        r = redis.from_url(settings.redis_url)
        r.publish(f"doc:{doc_id}:done", "1")
