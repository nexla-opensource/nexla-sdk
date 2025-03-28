"""
User models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

from .common import Resource, PaginatedList


class User(BaseModel):
    """User model"""
    id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    name: Optional[str] = Field(None, description="User name")
    first_name: Optional[str] = Field(None, description="User first name")
    last_name: Optional[str] = Field(None, description="User last name")
    role: Optional[str] = Field(None, description="User role")
    is_active: bool = Field(default=True, description="Whether the user is active")
    org_id: Optional[str] = Field(None, description="Organization ID")
    created_at: Optional[datetime] = Field(None, description="User creation timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")


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