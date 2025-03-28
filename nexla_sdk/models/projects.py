"""
Project models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList


class ProjectResource(BaseModel):
    """Project resource reference"""
    resource_id: str = Field(..., description="Resource ID")
    resource_type: str = Field(..., description="Resource type (e.g., 'flow', 'data_source')")
    name: Optional[str] = Field(None, description="Resource name")
    added_at: Optional[datetime] = Field(None, description="When the resource was added to the project")


class Project(Resource):
    """Project resource model"""
    resources_count: Optional[int] = Field(None, description="Number of resources in the project")
    owner_id: Optional[str] = Field(None, description="Owner user ID")
    org_id: Optional[str] = Field(None, description="Organization ID")


class ProjectList(PaginatedList[Project]):
    """Paginated list of projects"""
    pass


class ProjectResources(BaseModel):
    """Project resources list"""
    project_id: str = Field(..., description="Project ID")
    resources: List[ProjectResource] = Field(..., description="Project resources")
    total: int = Field(..., description="Total number of resources") 