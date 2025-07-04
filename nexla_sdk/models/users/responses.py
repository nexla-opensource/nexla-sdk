from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import Field
from nexla_sdk.models.base import BaseModel


class DefaultOrg(BaseModel):
    """User's default organization."""
    id: int
    name: str


class OrgMembership(BaseModel):
    """Organization membership details."""
    id: int
    name: str
    is_admin: Optional[bool] = Field(default=None, alias="isAdmin")
    org_membership_status: str  # ACTIVE, DEACTIVATED


class User(BaseModel):
    """User response model."""
    id: int
    email: str
    full_name: str
    super_user: Optional[bool] = Field(default=None, alias="superUser")
    impersonated: bool
    default_org: DefaultOrg
    user_tier: Optional[str] = None  # FREE, TRIAL, PAID, FREE_FOREVER
    status: str  # ACTIVE, DEACTIVATED, SOURCE_COUNT_CAPPED, etc.
    account_locked: bool
    org_memberships: List[OrgMembership]
    
    email_verified_at: Optional[datetime] = None
    tos_signed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class AccountSummary(BaseModel):
    """User account summary."""
    data_sources: Dict[str, Dict[str, int]]
    data_sets: Dict[str, Dict[str, int]]
    data_sinks: Dict[str, Dict[str, int]]
    data_maps: Dict[str, Dict[str, int]]


class UserExpanded(User):
    """User with expanded account summary."""
    account_summary: Optional[AccountSummary] = None


class UserSettings(BaseModel):
    """User settings."""
    id: str
    owner: Dict[str, Any]
    org: Dict[str, Any]
    user_settings_type: str
    settings: Dict[str, Any]
