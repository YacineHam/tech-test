from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class DocumentRead(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    size_bytes: int
    status: Literal["processing", "ready", "failed"]
    number_of_pages: int | None
    thumbnail_path: str | None
    uploaded_at: datetime
