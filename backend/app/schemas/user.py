from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    """What the API returns for a user. ``from_attributes`` lets us build it
    straight from a SQLAlchemy row."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: str
    created_at: datetime
