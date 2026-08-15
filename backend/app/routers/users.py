from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)) -> list[schemas.UserRead]:
    """Return all users."""
    return crud.user.list_users(db)
