"""
Organization models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr

from .common import Resource, PaginatedList
from .access import AccessRole
from .users import UserStatus, UserDetail


class OrgMembershipStatus(str, Enum):
    """Organization membership status types"""
    ACTIVE = "ACTIVE"
    DEACTIVATED = "DEACTIVATED"


class DefaultOrg(BaseModel):
    """Default organization information"""
    id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")


class OrgMembership(BaseModel):
    """Organization membership information"""
    id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    is_admin: Optional[bool] = Field(None, description="Whether the user is an admin in this organization")
    org_membership_status: str = Field(..., description="Membership status in this organization")


class AdminSummary(BaseModel):
    """Admin user summary"""
    id: int = Field(..., description="User ID")
    full_name: str = Field(..., description="User full name")
    email: EmailStr = Field(..., description="User email")


class OrgTier(BaseModel):
    """Organization tier information"""
    id: int = Field(..., description="Tier ID")
    name: str = Field(..., description="Tier name")
    display_name: str = Field(..., description="Tier display name")
    record_count_limit: int = Field(..., description="Record count limit")
    record_count_limit_time: str = Field(..., description="Record count limit timeframe")
    data_source_count_limit: int = Field(..., description="Data source count limit")
    trial_period_days: int = Field(..., description="Trial period in days")


class Organization(Resource):
    """Organization resource model"""
    name: str = Field(..., description="Organization name")
    description: Optional[str] = Field(None, description="Organization description")
    cluster_id: Optional[int] = Field(None, description="Cluster ID")
    new_cluster_id: Optional[int] = Field(None, description="New cluster ID")
    cluster_status: Optional[str] = Field(None, description="Cluster status")
    email_domain: str = Field(..., description="Organization email domain")
    email: Optional[str] = Field(None, description="Organization email")
    client_identifier: Optional[str] = Field(None, description="Client identifier")
    org_webhook_host: str = Field(..., description="Organization webhook host")
    default_cluster_id: Optional[int] = Field(None, description="Default cluster ID")
    access_roles: List[AccessRole] = Field(..., description="Access roles for the organization")
    owner: UserDetail = Field(..., description="Organization owner")
    billing_owner: UserDetail = Field(..., description="Organization billing owner")
    admins: List[AdminSummary] = Field(..., description="Organization administrators")
    org_tier: Optional[OrgTier] = Field(None, description="Organization tier")
    members_default_access_role: str = Field(..., description="Default access role for new members")
    status: str = Field(..., description="Organization status")
    default_reusable_code_container_access_role: str = Field(..., description="Default access role for reusable code containers")
    require_org_admin_to_publish: bool = Field(..., description="Whether org admin approval is required to publish")
    require_org_admin_to_subscribe: bool = Field(..., description="Whether org admin approval is required to subscribe")
    email_domain_verified_at: Optional[datetime] = Field(None, description="When the email domain was verified")
    name_verified_at: Optional[datetime] = Field(None, description="When the organization name was verified")
    enable_nexla_password_login: bool = Field(..., description="Whether Nexla password login is enabled")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")


class OrganizationList(List[Organization]):
    """List of organizations"""
    pass


class OrganizationMember(BaseModel):
    """Organization member"""
    id: int = Field(..., description="User ID")
    full_name: str = Field(..., description="User full name")
    email: str = Field(..., description="User email")
    is_admin: Optional[bool] = Field(None, description="Whether the user is an admin")
    access_role: List[AccessRole] = Field(..., description="User's access roles in the organization")
    org_membership_status: OrgMembershipStatus = Field(..., description="User's membership status")
    user_status: UserStatus = Field(..., description="User's account status")


class OrganizationMemberList(List[OrganizationMember]):
    """List of organization members"""
    pass


class MemberInfo(BaseModel):
    """Member information for update operations"""
    id: Optional[int] = Field(None, description="User ID")
    email: Optional[EmailStr] = Field(None, description="User email")
    access_role: Optional[List[AccessRole]] = Field(None, description="User's access roles")


class UpdateOrganizationRequest(BaseModel):
    """Request to update an organization"""
    name: Optional[str] = Field(None, description="Organization name")
    owner_id: Optional[int] = Field(None, description="Owner user ID")
    billing_owner_id: Optional[int] = Field(None, description="Billing owner user ID")
    email_domain: Optional[str] = Field(None, description="Organization email domain")
    client_identifier: Optional[str] = Field(None, description="Client identifier")
    enable_nexla_password_login: Optional[bool] = Field(None, description="Whether to enable Nexla password login")


class UpdateOrganizationMembersRequest(BaseModel):
    """Request to update organization members"""
    members: List[MemberInfo] = Field(..., description="Members to update")


class DeleteOrganizationMembersRequest(BaseModel):
    """Request to delete organization members"""
    members: List[MemberInfo] = Field(..., description="Members to delete")


class DeleteResponse(BaseModel):
    """Generic delete response"""
    code: str = Field(..., description="Response status code")
    message: str = Field(..., description="Response status text") 