from typing import List, Optional, Union, Literal
from datetime import datetime
from pydantic import Field
from nexla_sdk.models.base import BaseModel
from nexla_sdk.models.enums import AccessRole
from nexla_sdk.models.access.enums import AccessorType


class UserAccessorResponse(BaseModel):
    """Response model for USER type accessor."""
    type: Literal[AccessorType.USER] = AccessorType.USER
    id: Optional[int] = Field(None, description="Unique ID of the user")
    email: Optional[str] = Field(None, description="Email of the user")
    org_id: Optional[int] = Field(None, description="Organization ID for cross-org access")
    access_roles: List[AccessRole] = Field(description="List of access roles")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class TeamAccessorResponse(BaseModel):
    """Response model for TEAM type accessor."""
    type: Literal[AccessorType.TEAM] = AccessorType.TEAM
    id: Optional[int] = Field(None, description="Unique ID of the team")
    name: Optional[str] = Field(None, description="Name of the team")
    access_roles: List[AccessRole] = Field(description="List of access roles")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class OrgAccessorResponse(BaseModel):
    """Response model for ORG type accessor."""
    type: Literal[AccessorType.ORG] = AccessorType.ORG
    id: Optional[int] = Field(None, description="Unique ID of the organization")
    client_identifier: Optional[str] = Field(None, description="Client identifier for the organization")
    email_domain: Optional[str] = Field(None, description="Email domain for the organization")
    access_roles: List[AccessRole] = Field(description="List of access roles")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


# Union type for any accessor response
AccessorResponse = Union[UserAccessorResponse, TeamAccessorResponse, OrgAccessorResponse]


# Type aliases for easier usage
AccessorResponseList = List[AccessorResponse]
