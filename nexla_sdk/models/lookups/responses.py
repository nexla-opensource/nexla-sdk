from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import Field
from nexla_sdk.models.base import BaseModel
from nexla_sdk.models.common import Owner, Organization


class Lookup(BaseModel):
    """Lookup (data map) response model."""
    id: int
    name: str
    description: str
    map_primary_key: str
    owner: Owner
    org: Organization
    access_roles: List[str]
    public: bool
    managed: bool
    data_type: str
    emit_data_default: bool
    use_versioning: bool
    
    data_format: Optional[str] = None
    data_sink_id: Optional[int] = None
    data_defaults: Dict[str, Any] = Field(default_factory=dict)
    data_set_id: Optional[int] = None
    map_entry_count: Optional[int] = None
    map_entry_schema: Optional[Dict[str, Any]] = None
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None