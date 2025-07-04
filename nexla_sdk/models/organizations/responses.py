from typing import List, Optional, Dict, Any
from datetime import datetime
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
    trial_period_days: int


class Organization(BaseModel):
    """Organization response model."""
    id: int
    name: str
    email_domain: str
    access_roles: List[str]
    owner: User
    status: str
    members_default_access_role: str
    default_reusable_code_container_access_role: str
    require_org_admin_to_publish: bool
    require_org_admin_to_subscribe: bool
    enable_nexla_password_login: bool
    
    description: Optional[str] = None
    email: Optional[str] = None
    client_identifier: Optional[str] = None
    org_webhook_host: Optional[str] = None
    default_cluster_id: Optional[int] = None
    billing_owner: Optional[User] = None
    admins: List[User] = Field(default_factory=list)
    org_tier: Optional[OrgTier] = None
    email_domain_verified_at: Optional[datetime] = None
    name_verified_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OrgMember(BaseModel):
    """Organization member information."""
    id: int
    full_name: str
    email: str
    is_admin: bool
    access_role: List[str]
    org_membership_status: str
    user_status: str