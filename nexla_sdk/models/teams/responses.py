from typing import List, Optional
from datetime import datetime
from pydantic import Field
from nexla_sdk.models.base import BaseModel
from nexla_sdk.models.common import Owner, Organization


class TeamMember(BaseModel):
    """Team member information."""
    id: int
    email: str
    admin: bool


class Team(BaseModel):
    """Team response model."""
    id: int
    name: str
    description: str
    owner: Owner
    org: Organization
    member: bool
    members: List[TeamMember]
    access_roles: List[str]
    
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
