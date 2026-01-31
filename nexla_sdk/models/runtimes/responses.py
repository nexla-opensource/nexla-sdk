from datetime import datetime
from typing import Any, Dict, Optional

from nexla_sdk.models.base import BaseModel


class Runtime(BaseModel):
    """Response model for Custom Runtime aligned with OpenAPI Runtime schema."""

    id: int
    name: str
    description: Optional[str] = None
    active: Optional[bool] = None
    dockerpath: Optional[str] = None
    managed: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None
    # Optional owner/org mirrors other resources' patterns
    owner: Optional[Dict[str, Any]] = None
    org: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
