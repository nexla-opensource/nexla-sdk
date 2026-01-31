from typing import List, Optional

from pydantic import Field

from nexla_sdk.models.base import BaseModel


class TeamMemberRequest(BaseModel):
    """Request model for team member."""

    # Can identify by ID or email
    id: Optional[int] = None
    email: Optional[str] = None
    admin: bool = False


class TeamCreate(BaseModel):
    """Request model for creating a team."""

    name: str
    description: Optional[str] = None
    members: List[TeamMemberRequest] = Field(default_factory=list)


class TeamUpdate(BaseModel):
    """Request model for updating a team."""

    name: Optional[str] = None
    description: Optional[str] = None
    members: Optional[List[TeamMemberRequest]] = None


class TeamMemberList(BaseModel):
    """Request model for team member operations."""

    members: List[TeamMemberRequest]
