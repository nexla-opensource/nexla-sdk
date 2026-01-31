from typing import Optional

from nexla_sdk.models.base import BaseModel


class DocContainer(BaseModel):
    id: int
    name: Optional[str] = None
