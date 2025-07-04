from typing import Optional, List, Union
from pydantic import Field
from nexla_sdk.models.base import BaseModel


class ProjectFlowIdentifier(BaseModel):
    """Flow identifier for project."""
    data_source_id: Optional[int] = None
    data_set_id: Optional[int] = None


class ProjectCreate(BaseModel):
    """Request model for creating a project."""
    name: str
    description: Optional[str] = None
    data_flows: List[ProjectFlowIdentifier] = Field(default_factory=list)


class ProjectUpdate(BaseModel):
    """Request model for updating a project."""
    name: Optional[str] = None
    description: Optional[str] = None
    data_flows: Optional[List[ProjectFlowIdentifier]] = None


class ProjectFlowList(BaseModel):
    """Request model for managing project flows."""
    data_flows: Optional[List[ProjectFlowIdentifier]] = None
    flows: Optional[List[int]] = None  # Alternative using flow node IDs
