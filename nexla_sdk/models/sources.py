"""
Source models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList, Status


class SourceConfig(BaseModel):
    """Data source configuration"""
    connector_type: str = Field(..., description="Type of connector (e.g., 'file', 'rest_api')")
    credential_id: Optional[str] = Field(None, description="ID of the credential used by this source")
    options: Dict[str, Any] = Field(default_factory=dict, description="Connector-specific options")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Connection parameters")
    format_options: Optional[Dict[str, Any]] = Field(None, description="Data format options")


class Source(Resource):
    """Data source resource model"""
    config: SourceConfig = Field(..., description="Source configuration")
    status: Optional[Status] = Field(None, description="Source status information")
    stats: Optional[Dict[str, Any]] = Field(None, description="Source statistics")
    tags: Optional[List[str]] = Field(None, description="Tags associated with the source")
    owner_id: Optional[str] = Field(None, description="Owner user ID")
    org_id: Optional[str] = Field(None, description="Organization ID")


class SourceList(PaginatedList[Source]):
    """Paginated list of sources"""
    pass


class SourceExpanded(Source):
    """Expanded source with additional details"""
    flows: Optional[List[Dict[str, Any]]] = Field(None, description="Flows associated with this source")
    datasets: Optional[List[Dict[str, Any]]] = Field(None, description="Datasets associated with this source")
    credential: Optional[Dict[str, Any]] = Field(None, description="Credential details") 