"""
Team models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr

from .common import Resource, PaginatedList
from .access import AccessRole
from .users import UserDetail


class TeamMember(BaseModel):
    """Team member model"""
    id: int = Field(..., description="Unique ID of the user")
    email: Optional[str] = Field(None, description="User email")
    admin: bool = Field(False, description="Whether the user is an administrator of this team")


class TeamOwner(BaseModel):
    """Team owner model"""
    id: int = Field(..., description="Owner user ID")
    full_name: str = Field(..., description="Owner full name")
    email: str = Field(..., description="Owner email")
    email_verified_at: Optional[datetime] = Field(None, description="When the email was verified")


class TeamOrganization(BaseModel):
    """Team organization model"""
    id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    email_domain: str = Field(..., description="Organization email domain")
    email: Optional[str] = Field(None, description="Organization email")
    client_identifier: Optional[str] = Field(None, description="Client identifier")
    org_webhook_host: Optional[str] = Field(None, description="Organization webhook host")


class Team(Resource):
    """Team resource model"""
    name: str = Field(..., description="Team name")
    description: Optional[str] = Field(None, description="Team description")
    owner: Optional[TeamOwner] = Field(None, description="Team owner information")
    org: Optional[TeamOrganization] = Field(None, description="Team organization information")
    member: Optional[bool] = Field(None, description="Whether the authenticated user is a member of this team")
    members: Optional[List[TeamMember]] = Field(None, description="Team members")
    access_roles: Optional[List[AccessRole]] = Field(None, description="Access roles for the team")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    tags: Optional[List[str]] = Field(None, description="Team tags")


class TeamList(BaseModel):
    """Paginated list of teams"""
    items: List[Team] = Field(default_factory=list, description="List of teams")
    total: int = Field(default=0, description="Total number of teams")
    page: Optional[int] = Field(None, description="Current page number")
    per_page: Optional[int] = Field(None, description="Number of items per page")


class TeamMemberList(BaseModel):
    """Team members list with operations response"""
    members: List[TeamMember] = Field(..., description="Team members") 