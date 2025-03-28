"""
Credential models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList


class CredentialDetails(BaseModel):
    """Credential details for different types of credentials"""
    credential_type: str = Field(..., description="Type of credential (e.g., 'aws_s3', 'database')")
    # Specific credential detail fields will vary by credential_type
    # Using a Dict[str, Any] to handle all possible combinations
    properties: Dict[str, Any] = Field(default_factory=dict, description="Credential properties")


class Credential(Resource):
    """Credential resource model"""
    credential_type: str = Field(..., description="Type of credential (e.g., 'aws_s3', 'database')")
    credential_details: CredentialDetails = Field(..., description="Credential details")
    is_encrypted: bool = Field(default=True, description="Whether sensitive fields are encrypted")
    owner_id: Optional[str] = Field(None, description="Owner user ID")
    org_id: Optional[str] = Field(None, description="Organization ID")


class CredentialList(PaginatedList[Credential]):
    """Paginated list of credentials"""
    pass


class DirectoryItem(BaseModel):
    """Directory tree item"""
    name: str = Field(..., description="Item name")
    path: str = Field(..., description="Full path to the item")
    type: str = Field(..., description="Item type (e.g., 'file', 'directory')")
    size: Optional[int] = Field(None, description="Size in bytes (for files)")
    last_modified: Optional[datetime] = Field(None, description="Last modified timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class DirectoryTree(BaseModel):
    """Directory/file tree for a credential"""
    path: str = Field(..., description="Base path for the tree")
    items: List[DirectoryItem] = Field(..., description="Items in the tree")
    credential_id: str = Field(..., description="Credential ID")


class ProbeResult(BaseModel):
    """Probe test result for a credential"""
    success: bool = Field(..., description="Whether the probe was successful")
    message: Optional[str] = Field(None, description="Status message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")


class DataSample(BaseModel):
    """Sample data from a data source"""
    records: List[Dict[str, Any]] = Field(..., description="Sample data records")
    schema: Optional[Dict[str, Any]] = Field(None, description="Schema information")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata") 