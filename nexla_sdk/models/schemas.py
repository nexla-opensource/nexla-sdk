"""
Data Schema Models
"""
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList
from .access import Owner, Organization


class SchemaProperty(BaseModel):
    """Schema property definition in the JSON schema format"""
    type: str = Field(..., description="Property type")
    properties: Optional[Dict[str, "SchemaProperty"]] = Field(None, description="Nested properties for object types")
    items: Optional[Dict[str, Any]] = Field(None, description="Items definition for array types")
    format: Optional[str] = Field(None, description="Format specification")
    pattern: Optional[str] = Field(None, description="Pattern for string validation")
    minimum: Optional[float] = Field(None, description="Minimum value for numbers")
    maximum: Optional[float] = Field(None, description="Maximum value for numbers")
    enum: Optional[List[Any]] = Field(None, description="Enumeration of allowed values")


class SchemaRoot(BaseModel):
    """JSON Schema root definition"""
    properties: Dict[str, SchemaProperty] = Field(..., description="Schema properties")
    type: str = Field(..., description="Schema type")
    schema_: Optional[str] = Field(None, alias="$schema", description="JSON Schema version")
    schema_id: Optional[Union[int, str]] = Field(None, alias="$schema-id", description="Schema ID")


class SchemaAnnotation(BaseModel):
    """Schema annotation information"""
    description: Optional[str] = Field(None, description="Description of the field")
    properties: Optional[Dict[str, "SchemaAnnotation"]] = Field(None, description="Nested annotations for object types")
    type: Optional[str] = Field(None, description="Type information")


class SchemaValidation(BaseModel):
    """Schema validation rules"""
    properties: Optional[Dict[str, Any]] = Field(None, description="Validation rules for properties")
    type: Optional[str] = Field(None, description="Type information")


class DataSample(BaseModel):
    """Data sample for schema"""
    value: Dict[str, Any] = Field(..., description="Sample data value")


class DataSchema(Resource):
    """Data Schema resource model"""
    owner: Optional[Owner] = Field(None, description="Owner information")
    org: Optional[Organization] = Field(None, description="Organization information")
    version: Optional[int] = Field(None, description="Schema version")
    name: Optional[str] = Field(None, description="Schema name")
    description: Optional[str] = Field(None, description="Schema description")
    access_roles: Optional[List[str]] = Field(None, description="Access roles for this schema")
    detected: Optional[bool] = Field(None, description="Whether the schema was automatically detected")
    managed: Optional[bool] = Field(None, description="Whether the schema is managed")
    template: Optional[bool] = Field(None, description="Whether this is a template schema")
    schema: Optional[SchemaRoot] = Field(None, description="Schema definition (JSON Schema format)")
    annotations: Optional[SchemaAnnotation] = Field(None, description="Schema annotations")
    validations: Optional[SchemaValidation] = Field(None, description="Schema validations")
    data_samples: Optional[List[DataSample]] = Field(None, description="Data samples")
    data_sets: Optional[List[int]] = Field(None, description="IDs of data sets using this schema")
    tags: Optional[List[str]] = Field(None, description="Tags associated with the schema")


class SchemaList(PaginatedList[DataSchema]):
    """List of DataSchema objects"""
    pass 