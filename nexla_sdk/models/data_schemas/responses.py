from typing import Optional

from nexla_sdk.models.base import BaseModel


class DataSchema(BaseModel):
    id: int
    name: Optional[str] = None
