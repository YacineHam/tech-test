"""Insert a bit of demo data so the Users table is not empty on first run.

Idempotent: does nothing if the table already contains rows.
"""

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.user import User

_USERS = [
    {"name": "Camille Durand", "email": "camille.durand@reciTAL.example", "role": "Admin"},
    {"name": "Lucas Martin", "email": "lucas.martin@reciTAL.example", "role": "Reviewer"},
    {"name": "Emma Bernard", "email": "emma.bernard@reciTAL.example", "role": "Reviewer"},
    {"name": "Hugo Petit", "email": "hugo.petit@reciTAL.example", "role": "Viewer"},
    {"name": "Léa Moreau", "email": "lea.moreau@reciTAL.example", "role": "Admin"},
    {"name": "Nathan Laurent", "email": "nathan.laurent@reciTAL.example", "role": "Viewer"},
    {"name": "Chloé Simon", "email": "chloe.simon@reciTAL.example", "role": "Reviewer"},
    {"name": "Gabriel Michel", "email": "gabriel.michel@reciTAL.example", "role": "Viewer"},
]


def seed() -> None:
    db = SessionLocal()
    try:
        if db.scalar(select(User).limit(1)) is None:
            db.add_all(User(**row) for row in _USERS)
            db.commit()
    finally:
        db.close()
