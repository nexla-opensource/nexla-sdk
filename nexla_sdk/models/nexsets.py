"""
Nexset models for the Nexla SDK (Data Sets)
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList, Status
from .access import Owner, Organization, AccessRole


class FlowType(str, Enum):
    """Flow type enumeration"""
    STREAMING = "streaming"
    BATCH = "batch"


class SchemaAttribute(BaseModel):
    """Schema attribute definition"""
    name: str = Field(..., description="Attribute name")
    type: str = Field(..., description="Attribute data type")
    nullable: bool = Field(default=True, description="Whether the attribute can be null")
    primary_key: Optional[bool] = Field(None, description="Whether this is a primary key")
    description: Optional[str] = Field(None, description="Attribute description")
    format: Optional[str] = Field(None, description="Format specification for the attribute")
    nested_attributes: Optional[List["SchemaAttribute"]] = Field(None, description="Nested attributes for complex types")


class NexsetSchema(BaseModel):
    """Nexset schema definition"""
    attributes: List[SchemaAttribute] = Field(..., description="List of schema attributes")
    version: Optional[int] = Field(None, description="Schema version")
    source_format: Optional[str] = Field(None, description="Source data format")
    options: Optional[Dict[str, Any]] = Field(None, description="Schema options")


class DataSource(BaseModel):
    """Data source information"""
    id: int = Field(..., description="Data source ID")
    owner_id: Optional[int] = Field(None, description="Owner ID")
    org_id: Optional[int] = Field(None, description="Organization ID")
    name: str = Field(..., description="Data source name")
    description: Optional[str] = Field(None, description="Data source description")
    status: str = Field(..., description="Data source status")
    source_type: str = Field(..., description="Source type")
    connector: Optional[Dict[str, Any]] = Field(None, description="Connector information")
    vendor_id: Optional[Union[str, int]] = Field(None, description="Vendor ID")
    # Additional fields that might appear in API responses
    origin_node_id: Optional[Union[str, int]] = Field(None, description="Origin node ID")


class ParentDataSet(BaseModel):
    """Parent data set information"""
    id: int = Field(..., description="Data set ID")
    owner_id: int = Field(..., description="Owner ID")
    org_id: int = Field(..., description="Organization ID") 
    name: str = Field(..., description="Data set name")
    description: Optional[str] = Field(None, description="Data set description")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class DataSink(BaseModel):
    """Data sink information"""
    id: int = Field(..., description="Data sink ID")
    owner_id: int = Field(..., description="Owner ID")
    org_id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="Data sink name")
    status: Optional[str] = Field(None, description="Data sink status")
    sink_type: Optional[str] = Field(None, description="Sink type")
    description: Optional[str] = Field(None, description="Data sink description")


class Nexset(Resource):
    """Nexset resource model (Data Set)"""
    schema_: Optional[NexsetSchema] = Field(None, alias="schema", description="Nexset schema")
    status: Optional[Union[Status, str]] = Field(None, description="Nexset status information")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Nexset metrics")
    tags: Optional[List[str]] = Field(None, description="Tags associated with the nexset")
    owner: Optional[Owner] = Field(None, description="Owner information")
    org: Optional[Organization] = Field(None, description="Organization information")
    owner_id: Optional[Union[str, int]] = Field(None, description="Owner user ID")
    org_id: Optional[Union[str, int]] = Field(None, description="Organization ID")
    flow_node_id: Optional[Union[str, int]] = Field(None, description="Flow node ID this nexset is linked to")
    origin_node_id: Optional[Union[str, int]] = Field(None, description="Origin node ID in the flow")
    data_source_id: Optional[int] = Field(None, description="Data source ID if applicable")
    data_source: Optional[DataSource] = Field(None, description="Data source information")
    parent_data_set_id: Optional[Union[str, int]] = Field(None, description="Parent data set ID if this is derived")
    parent_data_sets: Optional[List[ParentDataSet]] = Field(None, description="Parent data sets information")
    code_container_id: Optional[Union[str, int]] = Field(None, description="Code container ID if applicable")
    data_sink_ids: Optional[List[Union[str, int]]] = Field(None, description="IDs of data sinks using this nexset")
    data_sinks: Optional[List[DataSink]] = Field(None, description="Data sinks information")
    public: Optional[bool] = Field(None, description="Whether the nexset is public")
    managed: Optional[bool] = Field(None, description="Whether the nexset is managed")
    access_roles: Optional[List[str]] = Field(None, description="Access roles for this nexset")
    transform_id: Optional[int] = Field(None, description="ID of the transform entity used for this nexset")
    output_schema: Optional[Dict[str, Any]] = Field(None, description="JSON schema of this nexset's output")
    copied_from_id: Optional[Union[str, int]] = Field(None, description="ID of the nexset this was copied from")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    flow_type: Optional[str] = Field(None, description="Flow type of the origin node")


class NexsetList(PaginatedList[Nexset]):
    """Paginated list of nexsets"""
    pass


class DataSet(Nexset):
    """Enhanced Data Set model (compatible with Flow API responses)"""
    id: Union[str, int] = Field(..., description="Data set ID")
    owner_id: Union[str, int] = Field(..., description="Owner ID")
    org_id: Union[str, int] = Field(..., description="Organization ID")
    flow_node_id: Union[str, int] = Field(..., description="Flow node ID")
    origin_node_id: Union[str, int] = Field(..., description="Origin node ID")
    name: str = Field(..., description="Data set name")
    description: Optional[str] = Field(None, description="Data set description")
    status: Union[Status, str] = Field(..., description="Status of the data set")
    data_source_id: Optional[Union[str, int]] = Field(None, description="Data source ID")
    parent_data_set_id: Optional[Union[str, int]] = Field(None, description="Parent data set ID")
    code_container_id: Optional[Union[str, int]] = Field(None, description="Code container ID")
    data_sink_ids: List[Union[str, int]] = Field(default_factory=list, description="Data sink IDs")
    public: bool = Field(..., description="Whether the data set is public")
    managed: bool = Field(..., description="Whether the data set is managed")
    access_roles: List[str] = Field(default_factory=list, description="Access roles for this data set")
    tags: List[str] = Field(default_factory=list, description="Tags associated with this data set")
    copied_from_id: Optional[Union[str, int]] = Field(None, description="ID of the data set this was copied from")


class NexsetSample(BaseModel):
    """Sample data from a nexset"""
    records: List[Dict[str, Any]] = Field(..., description="Sample records")
    total: int = Field(..., description="Total number of records in the sample")
    schema_: Optional[NexsetSchema] = Field(None, alias="schema", description="Schema of the sample data")


class NexsetMetadata(BaseModel):
    """Nexset metadata information"""
    sourceType: str = Field(..., description="Source type")
    ingestTime: int = Field(..., description="Ingestion timestamp")
    sourceOffset: int = Field(..., description="Source offset")
    sourceKey: str = Field(..., description="Source key")
    topic: Optional[str] = Field(None, description="Topic name")
    resourceType: str = Field(..., description="Resource type")
    resourceId: int = Field(..., description="Resource ID")
    trackerId: Dict[str, str] = Field(..., description="Tracker ID information")
    eof: Optional[bool] = Field(None, description="End of file indicator")
    lastModified: Optional[int] = Field(None, description="Last modified timestamp")
    runId: Optional[int] = Field(None, description="Run ID")
    tags: Optional[Dict[str, str]] = Field(None, description="Tags information")
    flow_type: Optional[str] = Field(None, description="Flow type")


class NexsetSampleWithMetadata(BaseModel):
    """Sample data from a nexset with metadata"""
    rawMessage: Dict[str, Any] = Field(..., description="Raw message content")
    nexlaMetaData: NexsetMetadata = Field(..., description="Nexla metadata")


class NexsetCharacteristics(BaseModel):
    """Nexset characteristics information"""
    record_count: Optional[int] = Field(None, description="Total number of records")
    file_size: Optional[int] = Field(None, description="Total size in bytes")
    attributes: Optional[Dict[str, Dict[str, Any]]] = Field(None, description="Attribute statistics")
    data_quality: Optional[Dict[str, Any]] = Field(None, description="Data quality metrics") 