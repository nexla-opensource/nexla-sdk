"""
User models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr, model_validator

from .common import Resource, PaginatedList
from .metrics import MetricsStatus
from .access import AccessRole

class UserStatus(str, Enum):
    """User status types"""
    ACTIVE = "ACTIVE"
    DEACTIVATED = "DEACTIVATED"
    SOURCE_COUNT_CAPPED = "SOURCE_COUNT_CAPPED"
    SOURCE_DATA_CAPPED = "SOURCE_DATA_CAPPED"
    TRIAL_EXPIRED = "TRIAL_EXPIRED"


class UserTier(str, Enum):
    """User tier types"""
    FREE = "FREE"
    TRIAL = "TRIAL"
    PAID = "PAID"
    FREE_FOREVER = "FREE_FOREVER"


class OrgMembershipStatus(str, Enum):
    """Organization membership status types"""
    ACTIVE = "ACTIVE"
    DEACTIVATED = "DEACTIVATED"


class DefaultOrg(BaseModel):
    """User's default organization"""
    id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")


class OrgMembership(BaseModel):
    """User's organization membership"""
    id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    is_admin: Optional[bool] = Field(None, description="Whether the user is an admin of this organization")
    org_membership_status: OrgMembershipStatus = Field(..., description="Status of the user's membership in this organization")


class ResourceCounts(BaseModel):
    """Resource counts for user account summary"""
    total: int = Field(..., description="Total count")
    owner: int = Field(..., description="Count where user is owner")
    collaborator: int = Field(..., description="Count where user is collaborator")
    active: Optional[int] = Field(None, description="Count of active resources")
    paused: Optional[int] = Field(None, description="Count of paused resources")
    draft: Optional[int] = Field(None, description="Count of draft resources")


class ResourceSummary(BaseModel):
    """Summary for a resource type"""
    counts: ResourceCounts = Field(..., description="Resource counts")


class AccountSummary(BaseModel):
    """User account summary information"""
    data_sources: ResourceSummary = Field(..., description="Data sources summary")
    data_sets: ResourceSummary = Field(..., description="Data sets summary")
    data_sinks: Optional[ResourceSummary] = Field(None, description="Data sinks summary")
    data_maps: Optional[ResourceSummary] = Field(None, description="Data maps summary")
    
    @model_validator(mode='before')
    @classmethod
    def ensure_all_fields(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure all required fields are present with defaults if missing"""
        if isinstance(data, dict):
            # Ensure data_sinks exists
            if "data_sinks" not in data:
                data["data_sinks"] = {"counts": {"total": 0, "owner": 0, "collaborator": 0}}
            # Ensure data_maps exists
            if "data_maps" not in data:
                data["data_maps"] = {"counts": {"total": 0, "owner": 0, "collaborator": 0}}
        return data


class UserDetail(BaseModel):
    """Detailed user information"""
    id: int = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    full_name: str = Field(..., description="User full name")
    super_user: Optional[bool] = Field(None, description="Whether the user is a super user")
    impersonated: bool = Field(..., description="Whether the user is being impersonated")
    default_org: Optional[DefaultOrg] = Field(None, description="User's default organization")
    user_tier: Optional[UserTier] = Field(None, description="User tier")
    status: UserStatus = Field(..., description="User status")
    account_locked: bool = Field(..., description="Whether the user account is locked")
    org_memberships: Optional[List[OrgMembership]] = Field(None, description="User's organization memberships")
    email_verified_at: Optional[datetime] = Field(None, description="When the email was verified")
    tos_signed_at: Optional[datetime] = Field(None, description="When the terms of service were signed")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")


class UserDetailExpanded(UserDetail):
    """User detail with expanded account information"""
    account_summary: AccountSummary = Field(..., description="User account summary")


class User(UserDetail):
    """User model"""
    @model_validator(mode='before')
    @classmethod
    def extract_user_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract user data from response if it's nested in a 'user' field"""
        if isinstance(data, dict) and "user" in data and isinstance(data["user"], dict):
            return data["user"]
        return data


class UserList(PaginatedList[User]):
    """Paginated list of users"""
    pass


class UserPreferences(BaseModel):
    """User preferences"""
    user_id: str = Field(..., description="User ID")
    preferences: Dict[str, Any] = Field(..., description="User preferences")


class UserSession(BaseModel):
    """User session information"""
    token: str = Field(..., description="Session token")
    user: User = Field(..., description="User information")
    expires_at: datetime = Field(..., description="Token expiration timestamp")


class CreateUserRequest(BaseModel):
    """Request model for creating a user"""
    full_name: str = Field(..., description="User's full name")
    email: EmailStr = Field(..., description="User's email")
    default_org_id: Optional[int] = Field(None, description="Default organization ID")
    status: Optional[UserStatus] = Field(None, description="User status")
    user_tier_id: Optional[int] = Field(None, description="User tier ID")
    user_tier: Optional[str] = Field(None, description="User tier")
    password: Optional[str] = Field(None, description="User password")
    tos_signed_at: Optional[datetime] = Field(None, description="When terms of service were signed")
    admin: Optional[Union[str, bool, List[Dict[str, Any]]]] = Field(None, description="Admin privileges")


class UpdateUserRequest(BaseModel):
    """Request model for updating a user"""
    name: Optional[str] = Field(None, description="User's name")
    email: Optional[EmailStr] = Field(None, description="User's email")
    status: Optional[UserStatus] = Field(None, description="User status")
    user_tier_id: Optional[int] = Field(None, description="User tier ID")
    user_tier: Optional[str] = Field(None, description="User tier")
    password: Optional[str] = Field(None, description="User password")
    password_confirmation: Optional[str] = Field(None, description="Password confirmation")
    password_current: Optional[str] = Field(None, description="Current password")
    tos_signed_at: Optional[datetime] = Field(None, description="When terms of service were signed")
    admin: Optional[Union[str, bool, List[Dict[str, Any]]]] = Field(None, description="Admin privileges") 