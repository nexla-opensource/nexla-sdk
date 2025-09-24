from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import Field
from nexla_sdk.models.base import BaseModel
from nexla_sdk.models.common import FlowNode
from nexla_sdk.models.sources.responses import Source
from nexla_sdk.models.nexsets.responses import Nexset
from nexla_sdk.models.destinations.responses import Destination
from nexla_sdk.models.credentials.responses import Credential


class FlowMetrics(BaseModel):
    """Flow metrics information."""
    origin_node_id: int
    records: int
    size: int
    errors: int
    reporting_date: datetime
    run_id: int


class FlowElements(BaseModel):
    """Flow elements containing all resources."""
    code_containers: List[Dict[str, Any]] = Field(default_factory=list)
    data_sources: List[Source] = Field(default_factory=list)
    data_sets: List[Nexset] = Field(default_factory=list)
    data_sinks: List[Destination] = Field(default_factory=list)
    data_credentials: List[Credential] = Field(default_factory=list)
    shared_data_sets: List[Dict[str, Any]] = Field(default_factory=list)
    orgs: List[Dict[str, Any]] = Field(default_factory=list)
    users: List[Dict[str, Any]] = Field(default_factory=list)
    projects: List[Dict[str, Any]] = Field(default_factory=list)


class FlowResponse(BaseModel):
    """Flow response model."""
    flows: List[FlowNode]
    # Include flow elements when not flows_only
    code_containers: Optional[List[Dict[str, Any]]] = None
    data_sources: Optional[List[Source]] = None
    data_sets: Optional[List[Nexset]] = None
    data_sinks: Optional[List[Destination]] = None
    data_credentials: Optional[List[Credential]] = None
    shared_data_sets: Optional[List[Dict[str, Any]]] = None
    orgs: Optional[List[Dict[str, Any]]] = None
    users: Optional[List[Dict[str, Any]]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    metrics: Optional[List[FlowMetrics]] = None