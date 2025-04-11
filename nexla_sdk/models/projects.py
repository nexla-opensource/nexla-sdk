"""
Project models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList
from .access import Owner, Organization, AccessRole


class ProjectFlowType(str, Enum):
    """Project flow types"""
    SOURCE = "source"
    NEXSET = "nexset"
    SINK = "sink"


class FlowNode(BaseModel):
    """Flow node in a project flow"""
    id: int = Field(..., description="Unique identifier of this flow")
    parent_node_id: Optional[int] = Field(None, description="Flow id of the parent flow node if this node is not the root node in the flow chain")
    origin_node_id: int = Field(..., description="Flow id of the root node in the flow chain")
    data_source_id: Optional[int] = Field(None, description="The ID of the data source this flow node is linked to if this is a flow node for a data source")
    data_set_id: Optional[int] = Field(None, description="The ID of the Nexset this flow node is linked to if this is flow node for a Nexset")
    data_sink_id: Optional[int] = Field(None, description="The ID of the data sink this flow node is linked to if this is a flow node for a data sink")
    shared_origin_node_id: Optional[int] = Field(None, description="Shared origin node ID")
    status: str = Field(..., description="Flow status")
    project_id: Optional[int] = Field(None, description="Project ID this flow belongs to")
    flow_type: str = Field(..., description="Flow type")
    ingestion_mode: str = Field(..., description="Ingestion mode")
    name: str = Field(..., description="Flow name")
    description: str = Field(..., description="Flow description")
    children: Optional[List['FlowNode']] = Field(None, description="Child flow nodes")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class DataFlow(BaseModel):
    """Data flow model (deprecated)"""
    id: int = Field(..., description="Unique identifier of this flow")
    project_id: int = Field(..., description="Unique identifier of the project this flow belongs to")
    data_source_id: Optional[int] = Field(None, description="The ID of the data source which is the root node of this flow chain")
    data_set_id: Optional[int] = Field(None, description="The ID of the Nexset which is the root node of this flow chain")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")


class ProjectResource(BaseModel):
    """Project resource reference"""
    resource_id: str = Field(..., description="Resource ID")
    resource_type: str = Field(..., description="Resource type (e.g., 'flow', 'data_source')")
    name: Optional[str] = Field(None, description="Resource name")
    added_at: Optional[datetime] = Field(None, description="When the resource was added to the project")


class Project(Resource):
    """Project resource model"""
    resources_count: Optional[int] = Field(None, description="Number of resources in the project")
    owner: Optional[Owner] = Field(None, description="Owner information")
    org: Optional[Organization] = Field(None, description="Organization information")
    data_flows: Optional[List[DataFlow]] = Field(None, description="List of all flows that are part of this project (deprecated)")
    flows: Optional[List[DataFlow]] = Field(None, description="List of all flows that are part of this project")
    access_roles: Optional[List[AccessRole]] = Field(None, description="Access roles for this project")
    tags: Optional[List[str]] = Field(None, description="Project tags")
    copied_from_id: Optional[str] = Field(None, description="ID of the project this was copied from")


class ProjectList(PaginatedList[Project]):
    """Paginated list of projects"""
    pass


class ProjectResources(BaseModel):
    """Project resources list"""
    project_id: str = Field(..., description="Project ID")
    resources: List[ProjectResource] = Field(..., description="Project resources")
    total: int = Field(..., description="Total number of resources")


class ProjectFlowResponse(BaseModel):
    """Flow response for project flows endpoint"""
    flows: List[FlowNode] = Field(..., description="List of flow nodes")
    code_containers: Optional[List[Dict[str, Any]]] = Field(None, description="All code containers linked to flow nodes")
    data_sources: Optional[List[Dict[str, Any]]] = Field(None, description="All data sources linked to flow nodes")
    data_sets: Optional[List[Dict[str, Any]]] = Field(None, description="All Nexsets linked to flow nodes")
    data_sinks: Optional[List[Dict[str, Any]]] = Field(None, description="All data sinks linked to flow nodes")
    data_credentials: Optional[List[Dict[str, Any]]] = Field(None, description="All credentials referenced by flow nodes")
    shared_data_sets: Optional[List[Dict[str, Any]]] = Field(None, description="Metadata about parent Nexsets")
    orgs: Optional[List[Dict[str, Any]]] = Field(None, description="Organizations information")
    users: Optional[List[Dict[str, Any]]] = Field(None, description="Users information")
    projects: Optional[List[Dict[str, Any]]] = Field(None, description="Projects information")


class ProjectFlowRequest(BaseModel):
    """Request body for project flows endpoints"""
    flows: List[int] = Field(..., description="List of flow IDs to add/replace")


class ProjectDataFlowRequest(BaseModel):
    """Request body for project data flows endpoints (deprecated)"""
    data_flows: List[Dict[str, int]] = Field(..., description="List of data flows to add/replace")


class CreateProjectRequest(BaseModel):
    """Request body for creating a project"""
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    data_flows: Optional[List[Dict[str, int]]] = Field(None, description="Initial data flows to add") 