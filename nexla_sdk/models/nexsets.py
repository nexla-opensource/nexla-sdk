"""
Nexset models for the Nexla SDK (Data Sets)
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList, Status


class SchemaAttribute(BaseModel):
    """Nexset schema attribute definition"""
    name: str = Field(..., description="Attribute name")
    data_type: str = Field(..., description="Data type")
    nullable: bool = Field(default=True, description="Whether the attribute can be null")
    primary_key: bool = Field(default=False, description="Whether this is a primary key")
    description: Optional[str] = Field(None, description="Attribute description")
    default_value: Optional[Any] = Field(None, description="Default value for the attribute")
    format: Optional[str] = Field(None, description="Format specification")
    constraints: Optional[Dict[str, Any]] = Field(None, description="Attribute constraints")
    tags: Optional[List[str]] = Field(None, description="Attribute tags")
    transform_id: Optional[str] = Field(None, description="ID of transform to apply")


class NexsetSchema(BaseModel):
    """Nexset schema definition"""
    attributes: List[SchemaAttribute] = Field(..., description="List of schema attributes")
    version: Optional[int] = Field(None, description="Schema version")
    source_format: Optional[str] = Field(None, description="Source data format")
    options: Optional[Dict[str, Any]] = Field(None, description="Schema options")


class Nexset(Resource):
    """Nexset resource model (Data Set)"""
    schema: Optional[NexsetSchema] = Field(None, description="Nexset schema")
    status: Optional[Status] = Field(None, description="Nexset status information")
    statistics: Optional[Dict[str, Any]] = Field(None, description="Nexset statistics")
    source_id: Optional[str] = Field(None, description="Source ID associated with this nexset")
    tags: Optional[List[str]] = Field(None, description="Tags associated with the nexset")
    owner_id: Optional[str] = Field(None, description="Owner user ID")
    org_id: Optional[str] = Field(None, description="Organization ID")


class NexsetList(PaginatedList[Nexset]):
    """Paginated list of nexsets"""
    pass


class NexsetSample(BaseModel):
    """Sample data from a nexset"""
    records: List[Dict[str, Any]] = Field(..., description="Sample records")
    total: int = Field(..., description="Total number of records in the sample")
    schema: Optional[NexsetSchema] = Field(None, description="Schema of the sample data")


class NexsetCharacteristics(BaseModel):
    """Nexset characteristics information"""
    record_count: Optional[int] = Field(None, description="Total number of records")
    file_size: Optional[int] = Field(None, description="Total size in bytes")
    attributes: Optional[Dict[str, Dict[str, Any]]] = Field(None, description="Attribute statistics")
    data_quality: Optional[Dict[str, Any]] = Field(None, description="Data quality metrics") 