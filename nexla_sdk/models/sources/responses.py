from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import Field
from nexla_sdk.models.base import BaseModel
from nexla_sdk.models.common import Owner, Organization, Connector
from nexla_sdk.models.credentials.responses import Credential


class DataSetBrief(BaseModel):
    """Brief dataset information."""
    id: int
    owner_id: int
    org_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RunInfo(BaseModel):
    """Run information."""
    id: int
    created_at: datetime


class Source(BaseModel):
    """Data source response model."""
    id: int
    name: str
    status: str
    source_type: str
    connector_type: Optional[str] = None
    owner: Optional[Owner] = None
    org: Optional[Organization] = None
    access_roles: Optional[List[str]] = None
    managed: Optional[bool] = None
    auto_generated: Optional[bool] = None
    connector: Optional[Connector] = None
    
    description: Optional[str] = None
    ingest_method: Optional[str] = None
    source_format: Optional[str] = None
    source_config: Optional[Dict[str, Any]] = None
    poll_schedule: Optional[str] = None
    code_container_id: Optional[int] = None
    data_credentials_id: Optional[int] = None
    data_credentials: Optional[Credential] = None
    data_sets: List[DataSetBrief] = Field(default_factory=list)
    api_keys: List[Dict[str, Any]] = Field(default_factory=list)
    run_ids: List[RunInfo] = Field(default_factory=list)
    copied_from_id: Optional[int] = None
    flow_type: Optional[str] = None
    has_template: Optional[bool] = None
    vendor_endpoint: Optional[Dict[str, Any]] = None
    vendor: Optional[Dict[str, Any]] = None
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
