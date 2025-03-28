"""
Organization models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList


class Organization(Resource):
    """Organization resource model"""
    display_name: Optional[str] = Field(None, description="Display name for the organization")
    domain: Optional[str] = Field(None, description="Organization domain")
    logo_url: Optional[str] = Field(None, description="Logo URL")
    owner_id: Optional[str] = Field(None, description="Owner user ID")


class OrganizationList(PaginatedList[Organization]):
    """Paginated list of organizations"""
    pass


class OrganizationSettings(BaseModel):
    """Organization settings"""
    org_id: str = Field(..., description="Organization ID")
    settings: Dict[str, Any] = Field(..., description="Organization settings")


class OrganizationMember(BaseModel):
    """Organization member"""
    user_id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    name: Optional[str] = Field(None, description="User name")
    role: str = Field(..., description="User role in the organization")
    joined_at: Optional[datetime] = Field(None, description="When the user joined")
    status: Optional[str] = Field(None, description="User status") 