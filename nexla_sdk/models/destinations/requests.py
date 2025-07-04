from typing import Optional, Dict, Any
from nexla_sdk.models.base import BaseModel


class DestinationCreate(BaseModel):
    """Request model for creating a destination."""
    name: str
    sink_type: str
    sink_config: Dict[str, Any]
    data_credentials_id: int
    data_set_id: int
    description: Optional[str] = None


class DestinationUpdate(BaseModel):
    """Request model for updating a destination."""
    name: Optional[str] = None
    description: Optional[str] = None
    sink_config: Optional[Dict[str, Any]] = None
    data_credentials_id: Optional[int] = None
    data_set_id: Optional[int] = None


class DestinationCopyOptions(BaseModel):
    """Options for copying a destination."""
    reuse_data_credentials: bool = False
    copy_access_controls: bool = False
    owner_id: Optional[int] = None
    org_id: Optional[int] = None