"""
Notification models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList, ResourceType
from .access import AccessRole, Owner, Organization


class NotificationLevel(str, Enum):
    """Notification level types"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    RECOVERED = "RECOVERED"
    RESOLVED = "RESOLVED"


class NotificationSettingStatus(str, Enum):
    """Notification setting status types"""
    PAUSED = "PAUSED"
    ACTIVE = "ACTIVE"


class NotificationResourceType(str, Enum):
    """Notification resource type"""
    ORG = "ORG"
    USER = "USER"
    DATA_FLOW = "DATA_FLOW"
    CUSTOM_DATA_FLOW = "CUSTOM_DATA_FLOW"
    SOURCE = "SOURCE"
    DATASET = "DATASET"
    SINK = "SINK"


class NotificationEventType(str, Enum):
    """Notification event type"""
    SHARE = "SHARE"
    CREATE = "CREATE"
    DELETE = "DELETE"
    UPDATE = "UPDATE"
    ACTIVATE = "ACTIVATE"
    PAUSE = "PAUSE"
    METRICS = "METRICS"
    RESETPASS = "RESETPASS"
    ERROR_AGGREGATED = "ERROR_AGGREGATED"
    ERROR = "ERROR"
    MONITOR = "MONITOR"
    WRITE = "WRITE"
    EMPTY_DATA = "EMPTY_DATA"
    READ_START = "READ_START"
    READ_DONE = "READ_DONE"
    WRITE_START = "WRITE_START"
    WRITE_DONE = "WRITE_DONE"


class NotificationCategory(str, Enum):
    """Notification category"""
    PLATFORM = "PLATFORM"
    SYSTEM = "SYSTEM"
    DATA = "DATA"


class NotificationChannel(str, Enum):
    """Notification channel"""
    APP = "APP"
    EMAIL = "EMAIL"
    SMS = "SMS"
    SLACK = "SLACK"
    WEBHOOKS = "WEBHOOKS"


class Notification(BaseModel):
    """Notification model"""
    id: int = Field(..., description="Notification ID")
    owner: Owner = Field(..., description="Owner information")
    org: Organization = Field(..., description="Organization information")
    access_roles: List[AccessRole] = Field(..., description="List of access roles")
    level: NotificationLevel = Field(..., description="Notification level")
    resource_id: int = Field(..., description="Resource ID")
    resource_type: ResourceType = Field(..., description="Resource type")
    message_id: int = Field(..., description="Message ID")
    message: str = Field(..., description="Notification message")
    read_at: Optional[datetime] = Field(None, description="When the notification was read")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")


class NotificationList(PaginatedList[Notification]):
    """Paginated list of notifications"""
    pass


class NotificationCount(BaseModel):
    """Notification count model"""
    count: int = Field(..., description="Total number of notifications")


class NotificationType(BaseModel):
    """Notification type model"""
    id: int = Field(..., description="Notification type ID")
    name: str = Field(..., description="Notification type name")
    description: str = Field(..., description="Notification type description")
    category: NotificationCategory = Field(..., description="Notification category")
    default: bool = Field(..., description="Whether this is a default notification type")
    status: bool = Field(..., description="Whether the notification type is active")
    event_type: NotificationEventType = Field(..., description="Event type")
    resource_type: NotificationResourceType = Field(..., description="Resource type")


class NotificationChannelSetting(BaseModel):
    """Notification channel setting model"""
    id: int = Field(..., description="Channel setting ID")
    owner_id: int = Field(..., description="Owner ID")
    org_id: int = Field(..., description="Organization ID")
    channel: NotificationChannel = Field(..., description="Notification channel")
    config: Dict[str, Any] = Field(..., description="Channel configuration properties")


class NotificationSetting(BaseModel):
    """Notification setting model"""
    id: int = Field(..., description="Notification setting ID")
    org_id: int = Field(..., description="Organization ID")
    owner_id: int = Field(..., description="Owner ID")
    channel: NotificationChannel = Field(..., description="Notification channel")
    notification_resource_type: NotificationResourceType = Field(..., description="Resource type")
    resource_id: Optional[int] = Field(None, description="Resource ID")
    config: Optional[Dict[str, Any]] = Field(None, description="Configuration properties")
    priority: int = Field(..., description="Priority level")
    status: NotificationSettingStatus = Field(..., description="Notification setting status")
    notification_type_id: int = Field(..., description="Notification type ID")
    name: str = Field(..., description="Notification setting name")
    description: str = Field(..., description="Notification setting description")
    code: int = Field(..., description="Notification code")
    category: str = Field(..., description="Notification category")
    event_type: NotificationEventType = Field(..., description="Event type")
    resource_type: NotificationResourceType = Field(..., description="Resource type")


class CreateNotificationChannelSettingRequest(BaseModel):
    """Request model for creating a notification channel setting"""
    channel: NotificationChannel = Field(..., description="Notification channel")
    config: Dict[str, Any] = Field(..., description="Channel configuration properties")


class UpdateNotificationChannelSettingRequest(BaseModel):
    """Request model for updating a notification channel setting"""
    channel: Optional[NotificationChannel] = Field(None, description="Notification channel")
    config: Optional[Dict[str, Any]] = Field(None, description="Channel configuration properties")


class CreateNotificationSettingRequest(BaseModel):
    """Request model for creating a notification setting"""
    channel: NotificationChannel = Field(..., description="Notification channel")
    status: Optional[NotificationSettingStatus] = Field(None, description="Notification setting status")
    config: Optional[Dict[str, Any]] = Field(None, description="Configuration properties")
    notification_resource_type: Optional[NotificationResourceType] = Field(None, description="Resource type")
    resource_id: Optional[int] = Field(None, description="Resource ID")
    checked: Optional[bool] = Field(None, description="Whether the notification is checked")
    notification_channel_setting_id: Optional[int] = Field(None, description="Notification channel setting ID")
    notification_type_id: int = Field(..., description="Notification type ID")


class UpdateNotificationSettingRequest(BaseModel):
    """Request model for updating a notification setting"""
    channel: Optional[NotificationChannel] = Field(None, description="Notification channel")
    status: Optional[NotificationSettingStatus] = Field(None, description="Notification setting status")
    config: Optional[Dict[str, Any]] = Field(None, description="Configuration properties")
    notification_resource_type: Optional[NotificationResourceType] = Field(None, description="Resource type")
    resource_id: Optional[int] = Field(None, description="Resource ID")
    checked: Optional[bool] = Field(None, description="Whether the notification is checked")
    notification_channel_setting_id: Optional[int] = Field(None, description="Notification channel setting ID")
    notification_type_id: Optional[int] = Field(None, description="Notification type ID")


class NotificationSettingExpanded(BaseModel):
    """Expanded notification setting with resource details"""
    setting_id: int = Field(..., description="Setting ID")
    org_id: int = Field(..., description="Organization ID")
    owner_id: int = Field(..., description="Owner ID")
    channel: NotificationChannel = Field(..., description="Notification channel")
    resource_type: NotificationResourceType = Field(..., description="Resource type")
    resource_id: int = Field(..., description="Resource ID")
    setting_config: Optional[str] = Field(None, description="Setting configuration")
    priority: int = Field(..., description="Priority level")
    status: NotificationSettingStatus = Field(..., description="Notification setting status")
    notification_type_id: int = Field(..., description="Notification type ID")
    setting_created_at: str = Field(..., description="Setting creation timestamp")
    setting_updated_at: str = Field(..., description="Setting update timestamp")
    notification_type_name: str = Field(..., description="Notification type name")
    notification_type_description: str = Field(..., description="Notification type description")
    notification_type_code: int = Field(..., description="Notification type code")
    notification_type_category: str = Field(..., description="Notification type category")
    notification_type_event_type: NotificationEventType = Field(..., description="Notification type event type")
    resource_owner_id: int = Field(..., description="Resource owner ID")
    resource_org_id: int = Field(..., description="Resource organization ID")
    resource_name: str = Field(..., description="Resource name")
    resource_description: str = Field(..., description="Resource description")
    resource_status: str = Field(..., description="Resource status") 