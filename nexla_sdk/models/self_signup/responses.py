from datetime import datetime
from typing import Optional

from nexla_sdk.models.base import BaseModel


class SelfSignupRequest(BaseModel):
    id: int
    status: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    invite_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BlockedDomain(BaseModel):
    id: int
    domain: str
