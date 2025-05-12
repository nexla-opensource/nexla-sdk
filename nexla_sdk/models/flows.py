"""
Flow models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList, Status, ResourceType
from .access import AccessRole
from .sources import Source
from .destinations import DataSink
from .nexsets import DataSet
from .code_containers import CodeContainer
from .credentials import Credential
from .organizations import Organization
from .users import User
from .projects import Project


class FlowSchedule(BaseModel):
    """Flow schedule configuration"""
    schedule_type: str = Field(..., description="Schedule type (e.g., 'cron', 'interval')")
    cron_expression: Optional[str] = Field(None, description="Cron expression for cron schedules")
    interval_value: Optional[int] = Field(None, description="Interval value for interval schedules")
    interval_unit: Optional[str] = Field(None, description="Interval unit for interval schedules")
    timezone: Optional[str] = Field(None, description="Timezone for the schedule")


class FlowConfig(BaseModel):
    """Flow configuration details"""
    is_active: bool = Field(..., description="Whether the flow is active")
    schedule: Optional[FlowSchedule] = Field(None, description="Schedule configuration")
    options: Optional[Dict[str, Any]] = Field(None, description="Additional flow options")


class Sharer(BaseModel):
    """Sharer model for flow nodes"""
    id: Optional[Union[str, int]] = Field(None, description="Sharer ID")
    # Additional fields as needed


class SharerInfo(BaseModel):
    """Sharer information for flow nodes"""
    sharers: List[Sharer] = Field(default_factory=list, description="List of sharers")
    external_sharers: List[Sharer] = Field(default_factory=list, description="List of external sharers")


class FlowNode(BaseModel):
    """Flow node model representing a node in the flow chain"""
    id: Optional[Union[str, int]] = Field(None, description="Flow node ID")
    parent_node_id: Optional[Union[str, int]] = Field(
        None,
        description="Flow id of the parent flow node if this node is not the root node in the flow chain."
    )
    parent_data_set_id: Optional[Union[str, int]] = Field(
        None, description="ID of the parent dataset in the flow"
    )
    origin_node_id: Optional[Union[str, int]] = Field(
        None, description="Flow id of the root node in the flow chain."
    )
    data_source_id: Optional[Union[str, int]] = Field(
        None,
        description="The ID of the data source this flow node is linked to if this is a flow node for a data source."
    )
    data_source: Optional[Dict[str, Any]] = Field(
        None, description="Information about the data source associated with this node"
    )
    data_set_id: Optional[Union[str, int]] = Field(
        None,
        description="The ID of the Nexset this flow node is linked to if this is flow node for a Nexset."
    )
    data_sink_id: Optional[Union[str, int]] = Field(
        None,
        description="The ID of the data sink this flow node is linked to if this is a flow node for a data sink."
    )
    data_sinks: Optional[List[Union[int, str, Dict[str, Any]]]] = Field(
        default_factory=list, description="Data sinks associated with this node"
    )
    sharers: Optional[SharerInfo] = Field(
        None, description="Information about sharers for this node"
    )
    shared_origin_node_id: Optional[Union[str, int]] = Field(None, description="Shared origin node ID")
    runtime_status: Optional[str] = Field(None, description="Runtime status of the flow node")
    node_type: Optional[str] = Field(None, description="Type of the node")
    status: Optional[str] = Field(None, description="Status of the flow node")
    project_id: Optional[Union[str, int]] = Field(None, description="Project ID associated with this flow")
    flow_type: Optional[str] = Field(None, description="Type of the flow")
    ingestion_mode: Optional[str] = Field(None, description="Ingestion mode of the flow")
    managed: Optional[bool] = Field(None, description="Whether the flow is managed")
    name: Optional[str] = Field(None, description="Name of the flow")
    description: Optional[str] = Field(None, description="Description of the flow")
    linked_flows: Optional[List[Union[str, int]]] = Field(None, description="Linked flows")
    children: Optional[List["FlowNode"]] = Field(
        None,
        description="Each element of this array is a flow node that is directly linked to this flow node."
    )
    
    # Support additional fields without validation errors
    class Config:
        extra = "ignore"


class FlowResponse(BaseModel):
    """Flow response model containing the flow and related resources"""
    flows: List[FlowNode] = Field(..., description="List of flow nodes")
    code_containers: Optional[List[Dict[str, Any]]] = Field(None, description="Code containers linked to flow nodes")
    data_sources: Optional[List[Dict[str, Any]]] = Field(None, description="Data sources linked to flow nodes")
    data_sets: Optional[List[Dict[str, Any]]] = Field(None, description="Data sets linked to flow nodes")
    data_sinks: Optional[List[Dict[str, Any]]] = Field(None, description="Data sinks linked to flow nodes")
    data_credentials: Optional[List[Dict[str, Any]]] = Field(None, description="Credentials referenced by flow nodes")
    shared_data_sets: Optional[List[Any]] = Field(default_factory=list, description="Shared data sets metadata")
    orgs: Optional[List[Dict[str, Any]]] = Field(None, description="Organizations")
    users: Optional[List[Dict[str, Any]]] = Field(None, description="Users")
    projects: Optional[List[Dict[str, Any]]] = Field(None, description="Projects linked to flows")
    triggered_flows: Optional[List[Any]] = Field(default_factory=list, description="Triggered flows")
    triggering_flows: Optional[List[Any]] = Field(default_factory=list, description="Triggering flows")
    linked_flows: Optional[List[Any]] = Field(default_factory=list, description="Linked flows")
    
    # Support additional fields without validation errors
    class Config:
        extra = "ignore"


class Flow(Resource):
    """Flow resource model (legacy model kept for backward compatibility)"""
    flow_type: str = Field(..., description="Type of the flow")
    source_id: Optional[str] = Field(None, description="ID of the source in this flow")
    sink_id: Optional[str] = Field(None, description="ID of the sink in this flow")
    dataset_id: Optional[str] = Field(None, description="ID of the dataset in this flow")
    config: FlowConfig = Field(..., description="Flow configuration")
    status: Optional[Status] = Field(None, description="Flow status information")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Flow metrics")
    tags: Optional[List[str]] = Field(None, description="Tags associated with the flow")
    

class FlowList(BaseModel):
    """Updated model for flow list API response"""
    flows: List[FlowNode] = Field(..., description="List of flow nodes")
    triggered_flows: Optional[List[Any]] = Field(default_factory=list, description="Triggered flows")
    triggering_flows: Optional[List[Any]] = Field(default_factory=list, description="Triggering flows") 
    linked_flows: Optional[List[Any]] = Field(default_factory=list, description="Linked flows")
    
    # Support additional fields without validation errors
    class Config:
        extra = "ignore"


class FlowCondensed(BaseModel):
    """Condensed flow information (legacy model kept for backward compatibility)"""
    id: str = Field(..., description="Flow ID")
    name: str = Field(..., description="Flow name")
    is_active: bool = Field(..., description="Whether the flow is active")
    source_id: Optional[str] = Field(None, description="ID of the source in this flow")
    sink_id: Optional[str] = Field(None, description="ID of the sink in this flow")
    dataset_id: Optional[str] = Field(None, description="ID of the dataset in this flow") 