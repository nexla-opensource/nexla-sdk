from typing import Optional

from nexla_sdk.models.base import BaseModel


class ApprovalDecision(BaseModel):
    approved: bool
    reason: Optional[str] = None

