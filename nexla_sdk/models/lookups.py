"""
Lookup models for the Nexla SDK (Data Maps)
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, root_validator

from .common import Resource, PaginatedList
from .access import AccessRole, Owner, Organization


class DataType(str, Enum):
    """Data type enum for Data Maps"""
    STRING = "string"
    NUMBER = "number"


class DataMapEntry(BaseModel):
    """Data map entry (key-value pair)"""
    key: str = Field(..., description="Entry key")
    value: Any = Field(..., description="Entry value")
    description: Optional[str] = Field(None, description="Entry description")
    tags: Optional[List[str]] = Field(None, description="Entry tags")


class DataMap(Resource):
    """Data map resource model (Lookup)"""
    description: Optional[str] = Field(None, description="Description of the data map")
    public_map: Optional[bool] = Field(None, description="Whether the data map is public")
    managed: Optional[bool] = Field(None, description="Whether the data map is managed")
    data_type: Optional[str] = Field(None, description="Data type of the map entries")
    data_format: Optional[str] = Field(None, description="Format of the data")
    data_sink_id: Optional[str] = Field(None, description="ID of the data sink if this is a dynamic map")
    emit_data_default: Optional[bool] = Field(None, description="Whether to emit default values for missing keys")
    use_versioning: Optional[bool] = Field(None, description="Whether to use versioning for this map")
    map_primary_key: Optional[str] = Field(None, description="Primary key field name for lookups")
    data_defaults: Optional[Dict[str, Any]] = Field(None, description="Default values for keys")
    is_active: bool = Field(default=True, description="Whether the data map is active")
    source_id: Optional[str] = Field(None, description="Source ID if map is loaded from a source")
    owner: Optional[Owner] = Field(None, description="Owner of the data map")
    org: Optional[Organization] = Field(None, description="Organization of the data map")
    access_roles: Optional[List[str]] = Field(None, description="Access roles for this data map")
    data_set_id: Optional[int] = Field(None, description="Associated data set ID")
    map_entry_schema: Optional[Dict[str, Any]] = Field(None, description="Schema of the map entries")
    map_entry_info: Optional[Dict[str, Any]] = Field(None, description="Information about map entries (counts, caching)")
    map_entry_count: Optional[int] = Field(None, description="Number of entries in the map")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    tags: Optional[List[str]] = Field(None, description="Tags for the data map")


# Alias classes for API compatibility
Lookup = DataMap
LookupExpanded = DataMap


class DataMapList(PaginatedList[DataMap]):
    """Paginated list of data maps"""
    pass


# Alias class for API compatibility  
LookupList = DataMapList


class DataMapEntries(BaseModel):
    """Data map entries"""
    map_id: str = Field(..., description="Data map ID")
    entries: List[DataMapEntry] = Field(..., description="Map entries")
    total: int = Field(..., description="Total number of entries")


class DataMapEntryBatch(BaseModel):
    """Batch of data map entries for update operations"""
    entries: List[Dict[str, Any]] = Field(..., description="Data map entries to upsert")


class CreateDataMapRequest(BaseModel):
    """Request to create a new data map"""
    name: str = Field(..., description="Name of the data map")
    description: Optional[str] = Field(None, description="Description of the data map")
    data_type: str = Field(..., description="Data type of map entries")
    map_primary_key: Optional[str] = Field(None, description="Primary key field for lookups")
    data_defaults: Optional[Dict[str, Any]] = Field(None, description="Default values for keys")
    emit_data_default: Optional[bool] = Field(None, description="Whether to emit default values for missing keys")
    tags: Optional[List[str]] = Field(None, description="Tags for the data map")
    data_map: Optional[List[Dict[str, Any]]] = Field(None, description="Initial data map entries")


class UpdateDataMapRequest(BaseModel):
    """Request to update a data map"""
    name: Optional[str] = Field(None, description="Name of the data map")
    description: Optional[str] = Field(None, description="Description of the data map")
    map_primary_key: Optional[str] = Field(None, description="Primary key field for lookups")
    data_defaults: Optional[Dict[str, Any]] = Field(None, description="Default values for keys")
    emit_data_default: Optional[bool] = Field(None, description="Whether to emit default values for missing keys")
    tags: Optional[List[str]] = Field(None, description="Tags for the data map")
    data_map: Optional[List[Dict[str, Any]]] = Field(None, description="Data map entries to replace existing entries")


class DeleteDataMapResponse(BaseModel):
    """Response from deleting a data map"""
    code: str = Field(..., description="Response status code")
    message: str = Field(..., description="Response status text")


class LookupResult(BaseModel):
    """Result of a lookup operation"""
    key: str = Field(..., description="Lookup key")
    value: Optional[Any] = Field(None, description="Lookup value")
    found: bool = Field(..., description="Whether the key was found")


class SampleEntriesRequest(BaseModel):
    """Request for sample entries from a lookup"""
    field_name: str = Field(..., description="Field name to filter on, or '*' for all fields")


class SampleEntriesResponse(BaseModel):
    """Response for sample entries request"""
    status: Optional[int] = Field(None, description="Response status code")
    message: Optional[str] = Field(None, description="Response message")
    output: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(None, description="Output containing sample entries")
    
    @root_validator(pre=True)
    def handle_direct_output(cls, values):
        """Handle cases where the API returns the entries list directly"""
        # If we get a list directly instead of a response object
        if isinstance(values, list):
            return {"status": 200, "message": "OK", "output": values}
        # If output is not explicitly provided but response has entries
        if "output" not in values and "entries" in values:
            values["output"] = values.pop("entries")
        return values 