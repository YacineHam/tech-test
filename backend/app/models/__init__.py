"""Importing the models here ensures they are registered on ``Base.metadata``
before ``create_all`` runs (see app.main)."""

from app.models.document import Document
from app.models.user import User

__all__ = ["Document", "User"]
