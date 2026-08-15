"""Data-access layer for users.

Keeping queries out of the routers means the HTTP layer stays thin and the same
functions can be reused from tasks, tests or scripts.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def list_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.id)))
