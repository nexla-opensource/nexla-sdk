from typing import Optional, Dict, Any, List
from pydantic import Field
from nexla_sdk.models.base import BaseModel


class LookupCreate(BaseModel):
    """Request model for creating a lookup."""
    name: str
    data_type: str
    map_primary_key: str
    description: Optional[str] = None
    data_defaults: Dict[str, Any] = Field(default_factory=dict)
    emit_data_default: bool = False
    data_map: Optional[List[Dict[str, Any]]] = None
    tags: List[str] = Field(default_factory=list)


class LookupUpdate(BaseModel):
    """Request model for updating a lookup."""
    name: Optional[str] = None
    description: Optional[str] = None
    map_primary_key: Optional[str] = None
    data_defaults: Optional[Dict[str, Any]] = None
    emit_data_default: Optional[bool] = None
    tags: Optional[List[str]] = None


class LookupEntriesUpsert(BaseModel):
    """Request model for upserting lookup entries."""
    entries: List[Dict[str, Any]]