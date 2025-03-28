"""
Lookup models for the Nexla SDK (Data Maps)
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList


class DataMapEntry(BaseModel):
    """Data map entry (key-value pair)"""
    key: str = Field(..., description="Entry key")
    value: Any = Field(..., description="Entry value")
    description: Optional[str] = Field(None, description="Entry description")
    tags: Optional[List[str]] = Field(None, description="Entry tags")


class DataMap(Resource):
    """Data map resource model (Lookup)"""
    entries_count: Optional[int] = Field(None, description="Number of entries in the map")
    is_active: bool = Field(default=True, description="Whether the data map is active")
    source_id: Optional[str] = Field(None, description="Source ID if map is loaded from a source")
    owner_id: Optional[str] = Field(None, description="Owner user ID")
    org_id: Optional[str] = Field(None, description="Organization ID")


class DataMapList(PaginatedList[DataMap]):
    """Paginated list of data maps"""
    pass


class DataMapEntries(BaseModel):
    """Data map entries"""
    map_id: str = Field(..., description="Data map ID")
    entries: List[DataMapEntry] = Field(..., description="Map entries")
    total: int = Field(..., description="Total number of entries")


class LookupResult(BaseModel):
    """Result of a lookup operation"""
    key: str = Field(..., description="Lookup key")
    value: Optional[Any] = Field(None, description="Lookup value")
    found: bool = Field(..., description="Whether the key was found") 