"""
Access role models for the Nexla SDK
"""
from enum import Enum
from typing import Optional, List, Dict, Any, Union, Literal
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class AccessRole(str, Enum):
    """
    Access role types
    
    This property reflects all the permissions the user/team/organization has to a resource.
    
    1. COLLABORATOR: The user/team/organization can view the resource but not make any 
                     modifications to it.
    2. OPERATOR: The user/team/organization can view the resource and can activate/pause it, 
                 but not make any other modifications to it.
    3. ADMIN: The user/team/organization has complete administrative rights to this resource.
    4. OWNER: This user created the resource and has complete administrative rights to it.
    """
    COLLABORATOR = "collaborator"
    OPERATOR = "operator"
    ADMIN = "admin"
    OWNER = "owner"


class Owner(BaseModel):
    """Owner information for a resource"""
    id: int = Field(..., description="Owner ID")
    full_name: str = Field(..., description="Owner's full name")
    email: EmailStr = Field(..., description="Owner's email address")


class Organization(BaseModel):
    """Organization information for a resource"""
    id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    email_domain: str = Field(..., description="Organization email domain")
    email: Optional[str] = Field(None, description="Organization email")
    client_identifier: Optional[str] = Field(None, description="Client identifier")


class Team(BaseModel):
    """Team information"""
    id: int = Field(..., description="Team ID")
    name: str = Field(..., description="Team name")
    description: Optional[str] = Field(None, description="Team description")
    org_id: int = Field(..., description="Organization ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class AccessControlEntry(BaseModel):
    """Access control entry for a resource"""
    id: int = Field(..., description="Access control entry ID")
    resource_id: int = Field(..., description="Resource ID")
    resource_type: str = Field(..., description="Resource type")
    access_role: AccessRole = Field(..., description="Access role")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    # Target can be a user, team, or organization
    user_id: Optional[int] = Field(None, description="User ID if target is a user")
    team_id: Optional[int] = Field(None, description="Team ID if target is a team")
    org_id: Optional[int] = Field(None, description="Organization ID if target is an organization")


class AccessControlList(BaseModel):
    """List of access control entries for a resource"""
    items: List[AccessControlEntry] = Field(..., description="Access control entries")
    total: int = Field(..., description="Total number of entries")


# New access control models for the API endpoints

class OrgAccessor(BaseModel):
    """Organization accessor information"""
    type: Literal["ORG"] = Field("ORG", description="Type of accessor")
    email_domain: str = Field(..., description="Organization email domain")
    client_identifier: Optional[str] = Field(None, description="Client identifier")


class TeamAccessor(BaseModel):
    """Team accessor information"""
    type: Literal["TEAM"] = Field("TEAM", description="Type of accessor")
    name: str = Field(..., description="Team name")


class UserAccessor(BaseModel):
    """User accessor information"""
    type: Literal["USER"] = Field("USER", description="Type of accessor")
    email: str = Field(..., description="User email")


class AccessorBase(BaseModel):
    """Base accessor model with access roles"""
    access_roles: List[AccessRole] = Field(..., description="Access roles for this accessor")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class Accessor(BaseModel):
    """Combined accessor model for API responses"""
    type: str = Field(..., description="Type of accessor: ORG, TEAM, or USER")
    email_domain: Optional[str] = Field(None, description="Organization email domain if type is ORG")
    client_identifier: Optional[str] = Field(None, description="Client identifier if type is ORG")
    name: Optional[str] = Field(None, description="Team name if type is TEAM")
    email: Optional[str] = Field(None, description="User email if type is USER")
    access_roles: List[AccessRole] = Field(..., description="Access roles for this accessor")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class AccessorRequestBase(BaseModel):
    """Base model for accessor request inputs"""
    type: str = Field(..., description="Type of accessor: USER, TEAM, or ORG")
    id: Optional[int] = Field(None, description="Unique ID of the user, team, or organization")
    email: Optional[str] = Field(None, description="User email, only required if type is USER and id not provided")
    org_id: Optional[int] = Field(None, description="Organization ID context for user access permission")


class AccessorRequest(AccessorRequestBase):
    """Accessor request model with access roles"""
    access_roles: List[AccessRole] = Field(..., description="Access roles to grant")


class AccessorsRequest(BaseModel):
    """Request model for accessor endpoints"""
    accessors: List[AccessorRequest] = Field(..., description="List of accessors to set for the resource") 