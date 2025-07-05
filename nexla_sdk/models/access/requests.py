from typing import List, Optional, Union, Literal
from pydantic import Field
from nexla_sdk.models.base import BaseModel
from nexla_sdk.models.enums import AccessRole
from nexla_sdk.models.access.enums import AccessorType


class UserAccessorRequest(BaseModel):
    """Request model for USER type accessor."""
    type: Literal[AccessorType.USER] = AccessorType.USER
    id: Optional[int] = Field(None, description="Unique ID of the user")
    email: Optional[str] = Field(None, description="Email of the user")
    org_id: Optional[int] = Field(None, description="Organization ID for cross-org access")
    access_roles: List[AccessRole] = Field(description="List of access roles")


class TeamAccessorRequest(BaseModel):
    """Request model for TEAM type accessor."""
    type: Literal[AccessorType.TEAM] = AccessorType.TEAM
    id: Optional[int] = Field(None, description="Unique ID of the team")
    name: Optional[str] = Field(None, description="Name of the team")
    access_roles: List[AccessRole] = Field(description="List of access roles")


class OrgAccessorRequest(BaseModel):
    """Request model for ORG type accessor."""
    type: Literal[AccessorType.ORG] = AccessorType.ORG
    id: Optional[int] = Field(None, description="Unique ID of the organization")
    client_identifier: Optional[str] = Field(None, description="Client identifier for the organization")
    email_domain: Optional[str] = Field(None, description="Email domain for the organization")
    access_roles: List[AccessRole] = Field(description="List of access roles")


# Union type for any accessor request
AccessorRequest = Union[UserAccessorRequest, TeamAccessorRequest, OrgAccessorRequest]


class AccessorsRequest(BaseModel):
    """Request model for accessor operations."""
    accessors: List[AccessorRequest] = Field(description="List of accessor requests")


# Type aliases for easier usage
AccessorRequestList = List[AccessorRequest] 