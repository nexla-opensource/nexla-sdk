"""
Common models used across the Nexla SDK
"""
from typing import List, Dict, Any, Generic, TypeVar, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ResourceID(BaseModel):
    """Resource identifier"""
    id: str = Field(..., description="Unique identifier for the resource")


class Resource(ResourceID):
    """Base resource model with common fields"""
    name: str = Field(..., description="Name of the resource")
    description: Optional[str] = Field(None, description="Description of the resource")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp") 
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    created_by: Optional[str] = Field(None, description="User ID who created this resource")
    updated_by: Optional[str] = Field(None, description="User ID who last updated this resource")


T = TypeVar('T')


class PaginatedList(BaseModel, Generic[T]):
    """Generic paginated list of resources"""
    items: List[T] = Field(..., description="List of resources")
    total: int = Field(..., description="Total number of resources")
    limit: int = Field(..., description="Maximum number of resources per page")
    offset: int = Field(..., description="Offset of the current page")


class Status(BaseModel):
    """Status information for a resource"""
    status: str = Field(..., description="Current status of the resource")
    message: Optional[str] = Field(None, description="Status message")
    last_run_at: Optional[datetime] = Field(None, description="Last run timestamp")
    next_run_at: Optional[datetime] = Field(None, description="Next scheduled run timestamp") 