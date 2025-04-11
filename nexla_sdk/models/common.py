"""
Common models used across the Nexla SDK
"""
from typing import List, Dict, Any, Generic, TypeVar, Optional, Union
from datetime import datetime
from enum import Enum, auto
from pydantic import BaseModel, Field


class ResourceID(BaseModel):
    """Resource identifier"""
    id: str = Field(..., description="Unique identifier for the resource")


T = TypeVar('T')


class PaginatedList(BaseModel, Generic[T]):
    """Generic paginated list response"""
    items: List[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items available")
    page: Optional[int] = Field(None, description="Current page number")
    page_size: Optional[int] = Field(None, description="Number of items per page")
    

class Status(BaseModel):
    """Resource status information"""
    state: str = Field(..., description="Current state of the resource")
    message: Optional[str] = Field(None, description="Status message")
    last_updated: Optional[datetime] = Field(None, description="Last status update timestamp")


class Resource(BaseModel):
    """Base resource model"""
    id: Union[str, int] = Field(..., description="Unique identifier for the resource")
    name: str = Field(..., description="Name of the resource")
    description: Optional[str] = Field(None, description="Description of the resource")
    created_at: Optional[datetime] = Field(None, description="Resource creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class ResourceType(str, Enum):
    """Resource types"""
    FLOW = "flow"
    DATA_SOURCE = "data_source"
    DATA_SET = "data_set"
    DATA_SINK = "data_sink"
    CODE_CONTAINER = "code_container"
    DATA_CREDENTIAL = "data_credential"
    PROJECT = "project"
    TRANSFORM = "transform"


class ConnectorType(str, Enum):
    """Connector types for data sources and sinks"""
    FILE = "file"
    DATABASE = "database"
    API = "api"
    STREAMING = "streaming"
    CLOUD_STORAGE = "cloud_storage" 