from typing import Any, Dict, List, Optional

from nexla_sdk.models.base import BaseModel


class OrgOwnerRequest(BaseModel):
    """Request model for specifying an org owner."""

    full_name: str
    email: str


class OrgMemberCreateRequest(BaseModel):
    """Request model for creating an org member."""

    full_name: str
    email: str
    admin: bool = False


class OrganizationCreate(BaseModel):
    """Request model for creating an organization."""

    name: str
    email_domain: str
    owner: Optional[OrgOwnerRequest] = None
    owner_id: Optional[int] = None
    description: Optional[str] = None
    billing_owner: Optional[OrgOwnerRequest] = None
    billing_owner_id: Optional[int] = None
    email: Optional[str] = None
    account_tier_id: Optional[int] = None
    members: Optional[List[OrgMemberCreateRequest]] = None


class OrganizationUpdate(BaseModel):
    """Request model for updating an organization."""

    name: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[OrgOwnerRequest] = None
    owner_id: Optional[int] = None
    billing_owner: Optional[OrgOwnerRequest] = None
    billing_owner_id: Optional[int] = None
    email: Optional[str] = None
    members: Optional[List[OrgMemberCreateRequest]] = None


class OrgMemberUpdate(BaseModel):
    """Request model for updating org member."""

    id: Optional[int] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    admin: Optional[bool] = None
    access_role: Optional[str] = None


class OrgMemberList(BaseModel):
    """Request model for updating org members."""

    members: List[OrgMemberUpdate]


class OrgMemberDeleteRequest(BaseModel):
    """Request model for deleting a single org member."""

    id: Optional[int] = None
    email: Optional[str] = None
    delegate_owner_id: Optional[int] = None


class OrgMemberDelete(BaseModel):
    """Request model for deleting org members."""

    members: List[OrgMemberDeleteRequest]


class OrgMemberActivateDeactivateRequest(BaseModel):
    """Request model for activating/deactivating org members."""

    members: List[Dict[str, Any]]
