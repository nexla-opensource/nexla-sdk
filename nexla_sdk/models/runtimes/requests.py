from typing import Optional, Dict, Any

from nexla_sdk.models.base import BaseModel


class RuntimeCreate(BaseModel):
    """Create payload for Custom Runtime matching OpenAPI RuntimePayload."""
    name: str
    description: Optional[str] = None
    active: Optional[bool] = None
    dockerpath: Optional[str] = None
    managed: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None


class RuntimeUpdate(BaseModel):
    """Update payload for Custom Runtime matching OpenAPI RuntimePayload."""
    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    dockerpath: Optional[str] = None
    managed: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None
