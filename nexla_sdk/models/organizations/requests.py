from typing import Optional, List, Union
from pydantic import Field
from nexla_sdk.models.base import BaseModel


class OrganizationUpdate(BaseModel):
    """Request model for updating an organization."""
    name: Optional[str] = None
    owner_id: Optional[int] = None
    billing_owner_id: Optional[int] = None
    email_domain: Optional[str] = None
    client_identifier: Optional[str] = None
    enable_nexla_password_login: Optional[bool] = None


class OrgMemberUpdate(BaseModel):
    """Request model for updating org member."""
    # Can identify by ID or email
    id: Optional[int] = None
    email: Optional[str] = None
    access_role: List[str] = Field(default_factory=list)


class OrgMemberList(BaseModel):
    """Request model for updating org members."""
    members: List[OrgMemberUpdate]


class OrgMemberDelete(BaseModel):
    """Request model for deleting org members."""
    members: List[Union[dict, OrgMemberUpdate]]