from datetime import datetime
from typing import Dict, List, Optional

from pydantic import Field

from nexla_sdk.models.base import BaseModel
from nexla_sdk.models.users.responses import User


class OrgTier(BaseModel):
    """Organization tier information."""

    id: int
    name: str
    display_name: str
    record_count_limit: int
    record_count_limit_time: str
    data_source_count_limit: int
    trial_period_days: Optional[int] = None


class Organization(BaseModel):
    """Organization response model."""

    id: int
    name: str
    email_domain: Optional[str] = None
    access_roles: List[str]
    owner: Optional[User] = None
    status: Optional[str] = None
    members_default_access_role: Optional[str] = None
    default_reusable_code_container_access_role: Optional[str] = None
    require_org_admin_to_publish: Optional[bool] = None
    require_org_admin_to_subscribe: Optional[bool] = None
    enable_nexla_password_login: Optional[bool] = None

    description: Optional[str] = None
    email: Optional[str] = None
    client_identifier: Optional[str] = None
    org_webhook_host: Optional[str] = None
    default_cluster_id: Optional[int] = None
    billing_owner: Optional[User] = None
    admins: List[User] = Field(default_factory=list)
    org_tier: Optional[OrgTier] = Field(default=None, alias="account_tier")
    account_tier_display_name: Optional[str] = None
    account_tier_name: Optional[str] = None
    email_domain_verified_at: Optional[datetime] = None
    name_verified_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OrgMember(BaseModel):
    """Organization member information."""

    id: int
    full_name: str
    email: str
    is_admin: bool = Field(..., alias="is_admin?")
    access_role: Optional[List[str]] = None
    org_membership_status: str
    user_status: str


class AccountSummary(BaseModel):
    """Organization account summary statistics."""

    org_id: int
    data_sources: Dict[str, int]
    data_sets: Dict[str, Dict[str, int]]
    data_sinks: Dict[str, int]


class CustodianUser(BaseModel):
    """Simplified user view for organization custodians endpoints."""

    id: int
    email: Optional[str] = None
    full_name: Optional[str] = None
