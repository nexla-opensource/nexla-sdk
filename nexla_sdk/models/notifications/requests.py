from typing import Any, Dict, Optional

from pydantic import Field

from nexla_sdk.models.base import BaseModel


class NotificationChannelSettingCreate(BaseModel):
    """Request model for creating notification channel setting."""

    channel: str  # APP, EMAIL, SMS, SLACK, WEBHOOKS
    config: Dict[str, Any]


class NotificationChannelSettingUpdate(BaseModel):
    """Request model for updating notification channel setting."""

    channel: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class NotificationSettingCreate(BaseModel):
    """Request model for creating notification setting."""

    channel: str
    notification_type_id: int
    status: Optional[str] = None  # PAUSED, ACTIVE
    config: Dict[str, Any] = Field(default_factory=dict)
    notification_resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    notification_channel_setting_id: Optional[int] = None


class NotificationSettingUpdate(BaseModel):
    """Request model for updating notification setting."""

    channel: Optional[str] = None
    status: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    notification_resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    checked: Optional[bool] = None
    notification_channel_setting_id: Optional[int] = None
    notification_type_id: Optional[int] = None
