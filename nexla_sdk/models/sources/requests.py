"""Request models for sources."""
from typing import Optional, Dict, Any, List
from nexla_sdk.models.base import BaseModel


class SourceCreate(BaseModel):
    """Request model for creating a source."""
    name: str
    source_type: str
    source_config: Dict[str, Any]
    data_credentials_id: int
    description: Optional[str] = None


class SourceUpdate(BaseModel):
    """Request model for updating a source."""
    name: Optional[str] = None
    description: Optional[str] = None
    source_config: Optional[Dict[str, Any]] = None
    data_credentials_id: Optional[int] = None


class SourceCopyOptions(BaseModel):
    """Options for copying a source."""
    reuse_data_credentials: bool = False
    copy_access_controls: bool = False
    owner_id: Optional[int] = None
    org_id: Optional[int] = None
