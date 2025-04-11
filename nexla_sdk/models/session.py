"""
Session models for the Nexla SDK
"""
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

from .common import Resource
from .users import User, OrgMembershipStatus

class TokenType(str, Enum):
    """Token type options"""
    BEARER = "Bearer"

class Impersonator(BaseModel):
    """Impersonator details when a user is being impersonated"""
    id: int = Field(..., description="Impersonator user ID")
    full_name: str = Field(..., description="Impersonator full name")
    email: EmailStr = Field(..., description="Impersonator email")
    email_verified_at: Optional[datetime] = Field(None, description="When the impersonator's email was verified")
    org: Optional[int] = Field(None, description="Impersonator's organization ID")

class SessionUser(BaseModel):
    """User information for session"""
    id: int = Field(..., description="User ID")
    full_name: str = Field(..., description="User full name")
    email: EmailStr = Field(..., description="User email")
    org: int = Field(..., description="User's organization ID")
    impersonated: bool = Field(False, description="Whether the user is being impersonated")
    impersonator: Optional[Impersonator] = Field(None, description="Impersonator details if user is being impersonated")

class OrgMembership(BaseModel):
    """Organization membership details"""
    api_key: str = Field(..., description="API key for the organization")
    status: OrgMembershipStatus = Field(..., description="Status of the user's membership in the organization")
    is_admin: Optional[bool] = Field(None, description="Whether the user is an admin of this organization")

class Organization(BaseModel):
    """Organization details"""
    id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    email_domain: Optional[str] = Field(None, description="Organization email domain")
    email: Optional[EmailStr] = Field(None, description="Organization email")
    client_identifier: Optional[str] = Field(None, description="Client identifier")
    org_webhook_host: Optional[str] = Field(None, description="Organization webhook host")

class LoginResponse(BaseModel):
    """Response for successful login"""
    access_token: str = Field(..., description="Access token for authentication")
    token_type: TokenType = Field(..., description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: SessionUser = Field(..., description="User information")
    org_membership: OrgMembership = Field(..., description="Organization membership details")
    org: Organization = Field(..., description="Organization details")

class LogoutResponse(BaseModel):
    """Response for successful logout"""
    pass 