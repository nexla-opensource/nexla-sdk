"""
Code Container models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList
from .access import AccessRole


class CodeType(str, Enum):
    """Code type enumeration"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    SQL = "sql"
    CUSTOM = "custom"
    JOLT_STANDARD = "jolt_standard"
    JOLT_CUSTOM = "jolt_custom"


class CodeEncoding(str, Enum):
    """Code encoding enumeration"""
    NONE = "none"
    UTF8 = "utf-8"
    BASE64 = "base64"


class OutputType(str, Enum):
    """Output type enumeration"""
    DATASET = "dataset"
    TRANSFORM = "transform"
    VALIDATION = "validation"
    RECORD = "record"
    ATTRIBUTE = "attribute"


class CodeContainer(Resource):
    """Code container model"""
    owner_id: str = Field(..., description="Owner ID")
    org_id: str = Field(..., description="Organization ID")
    data_credentials_id: Optional[str] = Field(None, description="Credentials ID for this container")
    public: bool = Field(..., description="Whether the container is public")
    managed: bool = Field(..., description="Whether the container is managed")
    reusable: bool = Field(..., description="Whether the container is reusable")
    resource_type: str = Field(..., description="Resource type")
    output_type: str = Field(..., description="Output type")
    code_type: str = Field(..., description="Code type")
    code_encoding: str = Field(..., description="Code encoding")
    access_roles: List[str] = Field(default_factory=list, description="Access roles for this container")
    tags: List[str] = Field(default_factory=list, description="Tags associated with this container")
    copied_from_id: Optional[str] = Field(None, description="ID of the container this was copied from")


class CodeContainerList(PaginatedList[CodeContainer]):
    """Paginated list of code containers"""
    pass


class CodeContainerContent(BaseModel):
    """Code container content"""
    id: str = Field(..., description="Container ID")
    code: str = Field(..., description="The actual code content")
    code_type: str = Field(..., description="Code type")
    code_encoding: str = Field(..., description="Code encoding")
    version: Optional[int] = Field(None, description="Version number")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp") 