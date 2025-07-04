from typing import List, Optional
from datetime import datetime
from pydantic import Field
from nexla_sdk.models.base import BaseModel
from nexla_sdk.models.common import Owner, Organization


class ProjectDataFlow(BaseModel):
    """Project data flow information."""
    id: int
    project_id: int
    data_source_id: Optional[int] = None
    data_set_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Project(BaseModel):
    """Project response model."""
    id: int
    owner: Owner
    org: Organization
    name: str
    description: str
    data_flows: List[ProjectDataFlow]
    flows: List[ProjectDataFlow]
    access_roles: List[str]
    
    tags: List[str] = Field(default_factory=list)
    copied_from_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
