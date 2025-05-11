"""
Integration tests for the Notifications API
"""
import os
import time
from datetime import datetime
import pytest

from nexla_sdk import NexlaClient
from nexla_sdk.models import (
    NotificationLevel, NotificationResourceType, NotificationEventType,
    CreateNotificationChannelSettingRequest, NotificationChannel,
    CreateNotificationSettingRequest, UpdateNotificationSettingRequest,
    NotificationSettingStatus
)

# Skip tests if environment variables are missing
missing_vars = []
if "NEXLA_SERVICE_KEY" not in os.environ:
    missing_vars.append("NEXLA_SERVICE_KEY")

SKIP_REASON = f"Missing environment variables: {', '.join(missing_vars)}" if missing_vars else ""
SKIP_TESTS = bool(missing_vars)

@pytest.fixture(scope="module")
def client():
    """Create a Nexla client for testing"""
    if SKIP_TESTS:
        pytest.skip(SKIP_REASON)
    return NexlaClient(service_key=os.environ["NEXLA_SERVICE_KEY"])

@pytest.mark.skipif(SKIP_TESTS, reason=SKIP_REASON)
class TestNotifications:
    """Tests for the Notifications API"""
    
    def test_get_notifications(self, client):
        """Test getting notifications"""
        # Get all notifications
        notifications = client.notifications.get_notifications()
        assert isinstance(notifications, list)
        
        # Get unread notifications
        unread_notifications = client.notifications.get_notifications(read=0)
        assert isinstance(unread_notifications, list)
        
        # Get notifications by level
        error_notifications = client.notifications.get_notifications(level=NotificationLevel.ERROR)
        assert isinstance(error_notifications, list)
    
    def test_get_notification_count(self, client):
        """Test getting notification count"""
        count = client.notifications.get_notification_count()
        assert hasattr(count, "count")
        assert isinstance(count.count, int)
        
        # Get unread notification count
        unread_count = client.notifications.get_notification_count(read=0)
        assert hasattr(unread_count, "count")
        assert isinstance(unread_count.count, int)
    
    def test_notification_read_unread(self, client):
        """Test marking notifications as read/unread"""
        # Get notification to work with
        notifications = client.notifications.get_notifications(limit=1)
        
        # If there are no notifications, we'll skip this test
        if not notifications:
            pytest.skip("No notifications available for testing")
        
        notification_id = notifications[0].id
        
        # Mark as read
        read_result = client.notifications.mark_notifications_read([notification_id])
        assert isinstance(read_result, dict)
        
        # Get the notification to verify
        notification = client.notifications.get_notification(notification_id)
        assert notification.id == notification_id
        
        # Mark as unread
        unread_result = client.notifications.mark_notifications_unread([notification_id])
        assert isinstance(unread_result, dict)
        
        # Get the notification to verify
        notification = client.notifications.get_notification(notification_id)
        assert notification.id == notification_id
    
    def test_get_notification_types(self, client):
        """Test getting notification types"""
        notification_types = client.notifications.get_notification_types()
        assert isinstance(notification_types, list)
        
        # If there are types, test the specific type endpoint
        if notification_types:
            notification_type = notification_types[0]
            
            specific_type = client.notifications.get_notification_type(
                event_type=notification_type.event_type,
                resource_type=notification_type.resource_type
            )
            
            assert specific_type.id == notification_type.id
    
    def test_notification_channel_settings(self, client):
        """Test notification channel settings CRUD operations"""
        # List channel settings
        channel_settings = client.notifications.list_notification_channel_settings()
        assert isinstance(channel_settings, list)
        
        # Create a new channel setting
        test_email = f"test_{int(time.time())}@example.com"
        new_channel_setting = client.notifications.create_notification_channel_setting(
            CreateNotificationChannelSettingRequest(
                channel=NotificationChannel.EMAIL,
                config={"email": test_email}
            )
        )
        
        assert new_channel_setting.channel == NotificationChannel.EMAIL
        assert new_channel_setting.config.get("email") == test_email
        
        channel_setting_id = new_channel_setting.id
        
        try:
            # Get the channel setting
            retrieved_setting = client.notifications.get_notification_channel_setting(channel_setting_id)
            assert retrieved_setting.id == channel_setting_id
            assert retrieved_setting.channel == NotificationChannel.EMAIL
            
            # Update the channel setting
            updated_email = f"updated_{int(time.time())}@example.com"
            updated_setting = client.notifications.update_notification_channel_setting(
                channel_setting_id,
                UpdateNotificationChannelSettingRequest(
                    config={"email": updated_email}
                )
            )
            
            assert updated_setting.id == channel_setting_id
            assert updated_setting.config.get("email") == updated_email
        
        finally:
            # Clean up - delete the channel setting
            delete_result = client.notifications.delete_notification_channel_setting(channel_setting_id)
            assert isinstance(delete_result, dict)
    
    def test_notification_settings(self, client):
        """Test notification settings CRUD operations"""
        # This test requires notification types, so get them first
        notification_types = client.notifications.get_notification_types()
        if not notification_types:
            pytest.skip("No notification types available for testing")
        
        notification_type_id = notification_types[0].id
        
        # List notification settings
        notification_settings = client.notifications.list_notification_settings()
        assert isinstance(notification_settings, list)
        
        # Create a new notification setting
        new_setting = client.notifications.create_notification_setting(
            CreateNotificationSettingRequest(
                channel=NotificationChannel.APP,
                notification_type_id=notification_type_id
            )
        )
        
        assert new_setting.channel == NotificationChannel.APP
        assert new_setting.notification_type_id == notification_type_id
        
        setting_id = new_setting.id
        
        try:
            # Get the notification setting
            retrieved_setting = client.notifications.get_notification_setting(setting_id)
            assert retrieved_setting.id == setting_id
            
            # Update the notification setting
            updated_setting = client.notifications.update_notification_setting(
                setting_id,
                UpdateNotificationSettingRequest(
                    status=NotificationSettingStatus.PAUSED
                )
            )
            
            assert updated_setting.id == setting_id
            assert updated_setting.status == NotificationSettingStatus.PAUSED
            
            # List notification settings by type
            settings_by_type = client.notifications.list_notification_settings_by_type(
                notification_type_id=notification_type_id
            )
            
            assert isinstance(settings_by_type, list)
            
            # With expand=True
            expanded_settings = client.notifications.list_notification_settings_by_type(
                notification_type_id=notification_type_id,
                expand=True
            )
            
            assert isinstance(expanded_settings, list)
        
        finally:
            # Clean up - delete the notification setting
            delete_result = client.notifications.delete_notification_setting(setting_id)
            assert isinstance(delete_result, dict) 