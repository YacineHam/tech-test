from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document


def list_documents(db: Session) -> list[Document]:
   return list(
        db.scalars(
            select(Document).order_by(Document.uploaded_at.desc(), Document.id.desc())
        )
    )


def get_document(db: Session, document_id: int) -> Document | None:
    return db.get(Document, document_id)


def create_document(db: Session, *, name: str, file_path: str, size_bytes: int) -> Document:
    document = Document(name=name, file_path=file_path, size_bytes=size_bytes)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document
