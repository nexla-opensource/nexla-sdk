"""
Destination models for the Nexla SDK (Data Sinks)
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList, Status


class DestinationConfig(BaseModel):
    """Data destination configuration"""
    connector_type: str = Field(..., description="Type of connector (e.g., 'file', 'database')")
    credential_id: Optional[str] = Field(None, description="ID of the credential used by this destination")
    options: Dict[str, Any] = Field(default_factory=dict, description="Connector-specific options")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Connection parameters")
    format_options: Optional[Dict[str, Any]] = Field(None, description="Data format options")
    mapping: Optional[Dict[str, Any]] = Field(None, description="Field mapping configuration")


class Destination(Resource):
    """Data destination resource model (Data Sink)"""
    config: DestinationConfig = Field(..., description="Destination configuration")
    status: Optional[Status] = Field(None, description="Destination status information")
    stats: Optional[Dict[str, Any]] = Field(None, description="Destination statistics")
    tags: Optional[List[str]] = Field(None, description="Tags associated with the destination")
    owner_id: Optional[str] = Field(None, description="Owner user ID")
    org_id: Optional[str] = Field(None, description="Organization ID")


class DestinationList(PaginatedList[Destination]):
    """Paginated list of destinations"""
    pass


class DestinationExpanded(Destination):
    """Expanded destination with additional details"""
    flows: Optional[List[Dict[str, Any]]] = Field(None, description="Flows associated with this destination")
    datasets: Optional[List[Dict[str, Any]]] = Field(None, description="Datasets associated with this destination")
    credential: Optional[Dict[str, Any]] = Field(None, description="Credential details") 