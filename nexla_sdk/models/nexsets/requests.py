"""Request models for nexsets."""
from typing import Optional, Dict, Any, List, Union
from pydantic import Field
from nexla_sdk.models.base import BaseModel


class NexsetCreate(BaseModel):
    """Request model for creating a nexset."""
    name: str
    parent_data_set_id: int
    has_custom_transform: bool
    
    # One of these must be provided based on has_custom_transform
    transform: Optional[Dict[str, Any]] = None
    transform_id: Optional[int] = None
    
    description: Optional[str] = None
    output_schema_annotations: Optional[Dict[str, Any]] = None
    output_schema_validation_enabled: bool = False
    output_validation_schema: Optional[Dict[str, Any]] = None
    data_sinks: List[Union[int, Dict[str, Any]]] = Field(default_factory=list)
    custom_config: Optional[Dict[str, Any]] = None
    tags: List[str] = Field(default_factory=list)


class NexsetUpdate(BaseModel):
    """Request model for updating a nexset."""
    name: Optional[str] = None
    description: Optional[str] = None
    has_custom_transform: Optional[bool] = None
    transform: Optional[Dict[str, Any]] = None
    transform_id: Optional[int] = None
    output_schema_annotations: Optional[Dict[str, Any]] = None
    output_schema_validation_enabled: Optional[bool] = None
    output_validation_schema: Optional[Dict[str, Any]] = None
    data_sinks: Optional[List[Union[int, Dict[str, Any]]]] = None
    custom_config: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None


class NexsetCopyOptions(BaseModel):
    """Options for copying a nexset."""
    copy_access_controls: bool = False
    owner_id: Optional[int] = None
    org_id: Optional[int] = None
