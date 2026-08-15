from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.database import get_db

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("", response_model=list[schemas.DocumentRead])
def list_documents(db: Session = Depends(get_db)) -> list[schemas.DocumentRead]:
    """Return all documents, newest first."""
    return crud.document.list_documents(db)
