from typing import Optional, Union, List, Dict, Any
from datetime import datetime
from nexla_sdk.models.base import BaseModel


class UserCreate(BaseModel):
    """Request model for creating a user."""
    full_name: str
    email: str
    default_org_id: Optional[int] = None
    status: Optional[str] = None
    user_tier_id: Optional[int] = None
    user_tier: Optional[str] = None
    password: Optional[str] = None
    tos_signed_at: Optional[datetime] = None
    admin: Optional[Union[str, bool, List[Dict[str, Any]]]] = None


class UserUpdate(BaseModel):
    """Request model for updating a user."""
    name: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None
    user_tier_id: Optional[int] = None
    user_tier: Optional[str] = None
    password: Optional[str] = None
    password_confirmation: Optional[str] = None
    password_current: Optional[str] = None
    tos_signed_at: Optional[datetime] = None
    admin: Optional[Union[str, bool, List[Dict[str, Any]]]] = None