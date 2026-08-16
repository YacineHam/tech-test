import asyncio
import os
import shutil
import uuid

import redis
from fastapi import APIRouter, Depends, HTTPException, UploadFile, WebSocket
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.core.database import SessionLocal, get_db
from app.tasks.documents import process_document

router = APIRouter(prefix="/api/documents", tags=["documents"])

_DOCUMENTS_SUBDIR = "documents"

_PDF_MAGIC = b"%PDF-"


@router.get("", response_model=list[schemas.DocumentRead])
def list_documents(db: Session = Depends(get_db)) -> list[schemas.DocumentRead]:
    """Return all documents, newest first."""
    return crud.document.list_documents(db)


@router.post("", response_model=schemas.DocumentRead, status_code=201)
def upload_document(
    file: UploadFile, db: Session = Depends(get_db)
) -> schemas.DocumentRead:
    """Store an uploaded PDF and enqueue its processing.

    The request only saves the file and creates the row; page count and
    thumbnail extraction happen in a Celery task so the response stays fast.
    The returned document is in the "processing" state.
    """
    if file.file.read(len(_PDF_MAGIC)) != _PDF_MAGIC:
        raise HTTPException(status_code=415, detail="Only PDF files are accepted.")
    file.file.seek(0)

    relative_path = os.path.join(_DOCUMENTS_SUBDIR, f"{uuid.uuid4().hex}.pdf")
    destination = os.path.join(settings.media_dir, relative_path)
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as out:
        shutil.copyfileobj(file.file, out)

    document = crud.document.create_document(
        db,
        name=file.filename or "document.pdf",
        file_path=relative_path,
        size_bytes=os.path.getsize(destination),
    )

    process_document.delay(document.id)

    return document


@router.websocket("/ws/documents/{doc_id}")
async def ws_track_document(websocket: WebSocket, doc_id: int) -> None:
    await websocket.accept()
    db = SessionLocal()

    try:
        r = redis.from_url(settings.redis_url)
        pubsub = r.pubsub()
        pubsub.subscribe(f"doc:{doc_id}:done")

        def listen_for_signal():
            for message in pubsub.listen():
                if message["type"] == "message":
                    return True
            return False

        await asyncio.wait_for(asyncio.to_thread(listen_for_signal), timeout=300)

        document = crud.document.get_document(db, doc_id)
        if document:
            await websocket.send_json(
                schemas.DocumentRead.model_validate(document).model_dump(mode='json')
            )
    except Exception:
        pass
    finally:
        db.close()
        pubsub.close()
