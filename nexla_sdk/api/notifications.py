"""
Notifications API for the Nexla SDK
"""
from typing import List, Optional, Union, Dict, Any, Literal
from datetime import datetime

# Import the types without creating a circular import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..client import NexlaClient

from ..models.notifications import (
    Notification, NotificationList, NotificationCount, NotificationType,
    NotificationChannelSetting, NotificationSetting, NotificationSettingExpanded,
    CreateNotificationChannelSettingRequest, UpdateNotificationChannelSettingRequest,
    CreateNotificationSettingRequest, UpdateNotificationSettingRequest,
    NotificationLevel, NotificationResourceType, NotificationEventType
)
from .base import BaseAPI


class NotificationsApi(BaseAPI):
    """API client for notifications endpoints"""

    def get_notifications(
        self,
        read: Optional[int] = None,
        level: Optional[NotificationLevel] = None,
        from_timestamp: Optional[int] = None,
        to_timestamp: Optional[int] = None
    ) -> List[Notification]:
        """
        Get all notifications in the authenticated user's account.

        Args:
            read: Set to 0 to fetch only unread notifications, 1 to fetch only read notifications.
            level: Filter by notification level (DEBUG, INFO, WARN, ERROR, RECOVERED, RESOLVED).
            from_timestamp: Filter notifications starting from timestamp (unix timestamp).
            to_timestamp: Filter notifications ending at timestamp (unix timestamp).

        Returns:
            List of notification objects.
        """
        params = {}
        if read is not None:
            params["read"] = read
        if level is not None:
            params["level"] = level.value
        if from_timestamp is not None:
            params["from"] = from_timestamp
        if to_timestamp is not None:
            params["to"] = to_timestamp

        response = self._get("/notifications", params=params)
        return [Notification(**item) for item in response]

    def get_notification(self, notification_id: int) -> Notification:
        """
        Get a specific notification by ID.

        Args:
            notification_id: The unique ID of the notification.

        Returns:
            Notification object.
        """
        return self._get(f"/notifications/{notification_id}", model_class=Notification)

    def delete_notification(self, notification_id: int) -> Dict[str, Any]:
        """
        Delete a specific notification by ID.

        Args:
            notification_id: The unique ID of the notification.

        Returns:
            Response indicating success.
        """
        return self._delete(f"/notifications/{notification_id}")

    def delete_all_notifications(self) -> Dict[str, Any]:
        """
        Delete all notifications belonging to the authenticated user.

        Returns:
            Response indicating success.
        """
        return self._delete("/notifications/all")

    def get_notification_count(self, read: Optional[int] = None) -> NotificationCount:
        """
        Get the total number of notifications in the authenticated user's account.

        Args:
            read: Set to 0 to count only unread notifications, 1 to count only read notifications.

        Returns:
            Notification count object.
        """
        params = {}
        if read is not None:
            params["read"] = read

        return self._get("/notifications/count", params=params, model_class=NotificationCount)

    def mark_notifications_read(
        self,
        notification_ids: Optional[List[int]] = None,
        mark_all: bool = False
    ) -> Dict[str, Any]:
        """
        Mark one, multiple, or all notifications as read.

        Args:
            notification_ids: List of notification IDs to mark as read.
            mark_all: Whether to mark all notifications as read.

        Returns:
            Response indicating success.
        """
        params = {}
        if mark_all:
            params["notification_id"] = "all"
            data = None
        else:
            data = notification_ids

        return self._put("/notifications/mark_read", params=params, json=data)

    def mark_notifications_unread(
        self,
        notification_ids: Optional[List[int]] = None,
        mark_all: bool = False
    ) -> Dict[str, Any]:
        """
        Mark one, multiple, or all notifications as unread.

        Args:
            notification_ids: List of notification IDs to mark as unread.
            mark_all: Whether to mark all notifications as unread.

        Returns:
            Response indicating success.
        """
        params = {}
        if mark_all:
            params["notification_id"] = "all"
            data = None
        else:
            data = notification_ids

        return self._put("/notifications/mark_unread", params=params, json=data)

    def get_notification_types(self, status: Optional[str] = None) -> List[NotificationType]:
        """
        Get all notification types supported by Nexla in this environment.

        Args:
            status: Filter by status (ACTIVE, PAUSE).

        Returns:
            List of notification type objects.
        """
        params = {}
        if status is not None:
            params["status"] = status

        response = self._get("/notification_types", params=params)
        return [NotificationType(**item) for item in response]

    def get_notification_type(
        self,
        event_type: NotificationEventType,
        resource_type: NotificationResourceType
    ) -> NotificationType:
        """
        Get a specific notification type by event type and resource type.

        Args:
            event_type: The event type.
            resource_type: The resource type.

        Returns:
            Notification type object.
        """
        params = {
            "event_type": event_type.value,
            "resource_type": resource_type.value
        }

        return self._get("/notification_types/list", params=params, model_class=NotificationType)

    def list_notification_channel_settings(self) -> List[NotificationChannelSetting]:
        """
        List all notification channel settings in the authenticated user's account.

        Returns:
            List of notification channel setting objects.
        """
        response = self._get("/notification_channel_settings")
        return [NotificationChannelSetting(**item) for item in response]

    def create_notification_channel_setting(
        self,
        request: CreateNotificationChannelSettingRequest
    ) -> NotificationChannelSetting:
        """
        Create a new configuration for a notification channel.

        Args:
            request: Request object for creating a notification channel setting.

        Returns:
            Newly created notification channel setting.
        """
        return self._post(
            "/notification_channel_settings", 
            json=request.dict(exclude_none=True), 
            
            model_class=NotificationChannelSetting
        )

    def get_notification_channel_setting(
        self,
        notification_channel_setting_id: int
    ) -> NotificationChannelSetting:
        """
        Get a specific notification channel setting by ID.

        Args:
            notification_channel_setting_id: The unique ID of the notification channel setting.

        Returns:
            Notification channel setting object.
        """
        return self._get(
            f"/notification_channel_settings/{notification_channel_setting_id}", 
            
            model_class=NotificationChannelSetting
        )

    def update_notification_channel_setting(
        self,
        notification_channel_setting_id: int,
        request: UpdateNotificationChannelSettingRequest
    ) -> NotificationChannelSetting:
        """
        Update a notification channel setting.

        Args:
            notification_channel_setting_id: The unique ID of the notification channel setting.
            request: Request object for updating a notification channel setting.

        Returns:
            Updated notification channel setting.
        """
        return self._put(
            f"/notification_channel_settings/{notification_channel_setting_id}",
            json=request.dict(exclude_none=True),
           
            model_class=NotificationChannelSetting
        )

    def delete_notification_channel_setting(
        self,
        notification_channel_setting_id: int
    ) -> Dict[str, Any]:
        """
        Delete a notification channel setting.

        Args:
            notification_channel_setting_id: The unique ID of the notification channel setting.

        Returns:
            Response indicating success.
        """
        return self._delete(f"/notification_channel_settings/{notification_channel_setting_id}")

    def list_notification_settings(
        self,
        event_type: Optional[NotificationEventType] = None,
        resource_type: Optional[NotificationResourceType] = None,
        status: Optional[str] = None
    ) -> List[NotificationSetting]:
        """
        List all notification settings in the authenticated user's account.

        Args:
            event_type: Filter by event type.
            resource_type: Filter by resource type.
            status: Filter by status (PAUSED, ACTIVE).

        Returns:
            List of notification setting objects.
        """
        params = {}
        if event_type is not None:
            params["event_type"] = event_type.value
        if resource_type is not None:
            params["resource_type"] = resource_type.value
        if status is not None:
            params["status"] = status

        response = self._get("/notification_settings", params=params)
        return [NotificationSetting(**item) for item in response]

    def create_notification_setting(
        self,
        request: CreateNotificationSettingRequest
    ) -> NotificationSetting:
        """
        Create a setting to designate whether, when, and how a specific notification should be fired.

        Args:
            request: Request object for creating a notification setting.

        Returns:
            Newly created notification setting.
        """
        return self._post(
            "/notification_settings", 
            json=request.dict(exclude_none=True), 
            
            model_class=NotificationSetting
        )

    def get_notification_setting(
        self,
        notification_setting_id: int
    ) -> NotificationSetting:
        """
        Get a specific notification setting by ID.

        Args:
            notification_setting_id: The unique ID of the notification setting.

        Returns:
            Notification setting object.
        """
        return self._get(
            f"/notification_settings/{notification_setting_id}", 
            
            model_class=NotificationSetting
        )

    def update_notification_setting(
        self,
        notification_setting_id: int,
        request: UpdateNotificationSettingRequest
    ) -> NotificationSetting:
        """
        Update a notification setting.

        Args:
            notification_setting_id: The unique ID of the notification setting.
            request: Request object for updating a notification setting.

        Returns:
            Updated notification setting.
        """
        return self._put(
            f"/notification_settings/{notification_setting_id}",
            json=request.dict(exclude_none=True),
           
            model_class=NotificationSetting
        )

    def delete_notification_setting(
        self,
        notification_setting_id: int
    ) -> Dict[str, Any]:
        """
        Delete a notification setting.

        Args:
            notification_setting_id: The unique ID of the notification setting.

        Returns:
            Response indicating success.
        """
        return self._delete(f"/notification_settings/{notification_setting_id}")

    def list_notification_settings_by_type(
        self,
        notification_type_id: int,
        expand: Optional[bool] = None
    ) -> List[NotificationSettingExpanded]:
        """
        Get all notification settings for a specific notification type.

        Args:
            notification_type_id: The unique ID of the notification type.
            expand: Whether to expand the response with additional details.

        Returns:
            List of expanded notification setting objects.
        """
        params = {}
        if expand is not None:
            params["expand"] = expand

        response = self._get(
            f"/notification_settings/notification_types/{notification_type_id}",
            params=params,
           
        )
        return [NotificationSettingExpanded(**item) for item in response]

    def list_resource_notification_settings(
        self,
        resource_type: NotificationResourceType,
        resource_id: int,
        expand: Optional[bool] = None,
        filter_overridden_settings: Optional[bool] = None,
        notification_type_id: Optional[int] = None
    ) -> List[NotificationSetting]:
        """
        Get all notification settings for a specific resource.

        Args:
            resource_type: The resource type.
            resource_id: The resource ID.
            expand: Whether to expand the response with additional details.
            filter_overridden_settings: Whether to filter overridden settings.
            notification_type_id: Filter by notification type ID.

        Returns:
            List of notification setting objects.
        """
        params = {}
        if expand is not None:
            params["expand"] = expand
        if filter_overridden_settings is not None:
            params["filter_overridden_settings"] = filter_overridden_settings
        if notification_type_id is not None:
            params["notification_type_id"] = notification_type_id

        response = self._get(
            f"/notification_settings/{resource_type.value}/{resource_id}",
            params=params,
           
        )
        return [NotificationSetting(**item) for item in response] 