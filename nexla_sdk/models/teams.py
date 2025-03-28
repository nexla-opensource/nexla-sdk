"""
Team models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList


class TeamMember(BaseModel):
    """Team member model"""
    user_id: str = Field(..., description="User ID")
    team_id: str = Field(..., description="Team ID")
    role: str = Field(..., description="Member role ('admin', 'member')")
    email: Optional[str] = Field(None, description="User email")
    name: Optional[str] = Field(None, description="User name")
    added_at: Optional[datetime] = Field(None, description="When the user was added to the team")


class Team(Resource):
    """Team resource model"""
    members_count: Optional[int] = Field(None, description="Number of members in the team")
    owner_id: Optional[str] = Field(None, description="Owner user ID")
    org_id: Optional[str] = Field(None, description="Organization ID")


class TeamList(PaginatedList[Team]):
    """Paginated list of teams"""
    pass


class TeamMembers(BaseModel):
    """Team members list"""
    team_id: str = Field(..., description="Team ID")
    members: List[TeamMember] = Field(..., description="Team members")
    total: int = Field(..., description="Total number of members") 