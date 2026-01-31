from datetime import datetime
from typing import Optional

from nexla_sdk.models.base import BaseModel


class ApprovalRequest(BaseModel):
    id: int
    status: Optional[str] = None
    request_type: Optional[str] = None
    requester_id: Optional[int] = None
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    reason: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
