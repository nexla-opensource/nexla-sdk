"""
Flow models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList, Status


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


class Flow(Resource):
    """Flow resource model"""
    flow_type: str = Field(..., description="Type of the flow")
    source_id: Optional[str] = Field(None, description="ID of the source in this flow")
    sink_id: Optional[str] = Field(None, description="ID of the sink in this flow")
    dataset_id: Optional[str] = Field(None, description="ID of the dataset in this flow")
    config: FlowConfig = Field(..., description="Flow configuration")
    status: Optional[Status] = Field(None, description="Flow status information")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Flow metrics")
    tags: Optional[List[str]] = Field(None, description="Tags associated with the flow")
    

class FlowList(PaginatedList[Flow]):
    """Paginated list of flows"""
    pass


class FlowCondensed(BaseModel):
    """Condensed flow information"""
    id: str = Field(..., description="Flow ID")
    name: str = Field(..., description="Flow name")
    is_active: bool = Field(..., description="Whether the flow is active")
    source_id: Optional[str] = Field(None, description="ID of the source in this flow")
    sink_id: Optional[str] = Field(None, description="ID of the sink in this flow")
    dataset_id: Optional[str] = Field(None, description="ID of the dataset in this flow") 