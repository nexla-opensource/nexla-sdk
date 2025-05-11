"""
Example usage of the Notifications API
"""
from datetime import datetime, timedelta
import time
from pprint import pprint

from nexla_sdk.models import (
    NotificationLevel, NotificationResourceType, NotificationEventType,
    CreateNotificationChannelSettingRequest, NotificationChannel,
    CreateNotificationSettingRequest, UpdateNotificationSettingRequest,
    NotificationSettingStatus
)

from client import nexla_client

def run_notification_examples():
    """Run through examples of using the Notifications API"""
    client = nexla_client
    
    print("\n=== Listing all notifications ===")
    # List all notifications
    notifications = client.notifications.get_notifications()
    print(f"Found {len(notifications)} notifications")
    
    # List only unread notifications
    unread_notifications = client.notifications.get_notifications(read=0)
    print(f"Found {len(unread_notifications)} unread notifications")
    
    # List notifications with level filter
    error_notifications = client.notifications.get_notifications(level=NotificationLevel.ERROR)
    print(f"Found {len(error_notifications)} error notifications")
    
    # Get a notification count
    notification_count = client.notifications.get_notification_count(read=0)
    print(f"Unread notification count: {notification_count.count}")
    
    # If there are any notifications, mark one as read and then unread
    if unread_notifications:
        notification_id = unread_notifications[0].id
        print(f"\n=== Marking notification {notification_id} as read ===")
        client.notifications.mark_notifications_read([notification_id])
        
        # Get the notification to verify it's read
        notification = client.notifications.get_notification(notification_id)
        print(f"Notification {notification_id} read status: {notification.read_at is not None}")
        
        print(f"\n=== Marking notification {notification_id} as unread ===")
        client.notifications.mark_notifications_unread([notification_id])
        
        # Get the notification to verify it's unread
        notification = client.notifications.get_notification(notification_id)
        print(f"Notification {notification_id} read status: {notification.read_at is not None}")
    
    # Get notification types
    print("\n=== Listing notification types ===")
    notification_types = client.notifications.get_notification_types()
    print(f"Found {len(notification_types)} notification types")
    
    # If there are notification types, get a specific one
    if notification_types:
        notification_type = notification_types[0]
        print(f"\n=== Getting notification type by event and resource type ===")
        try:
            specific_type = client.notifications.get_notification_type(
                event_type=notification_type.event_type,
                resource_type=notification_type.resource_type
            )
            print(f"Found notification type: {specific_type.name}")
        except Exception as e:
            print(f"Failed to get specific notification type: {e}")
    
    # List notification channel settings
    print("\n=== Listing notification channel settings ===")
    channel_settings = client.notifications.list_notification_channel_settings()
    print(f"Found {len(channel_settings)} notification channel settings")
    
    # Create a new notification channel setting for testing
    print("\n=== Creating a new notification channel setting ===")
    try:
        new_channel_setting = client.notifications.create_notification_channel_setting(
            CreateNotificationChannelSettingRequest(
                channel=NotificationChannel.EMAIL,
                config={"email": "test@example.com"}
            )
        )
        channel_setting_id = new_channel_setting.id
        print(f"Created new channel setting with ID: {channel_setting_id}")
        
        # Get the channel setting
        print(f"\n=== Getting notification channel setting {channel_setting_id} ===")
        retrieved_setting = client.notifications.get_notification_channel_setting(channel_setting_id)
        print(f"Retrieved channel setting: {retrieved_setting.channel}")
        
        # Update the channel setting
        print(f"\n=== Updating notification channel setting {channel_setting_id} ===")
        updated_setting = client.notifications.update_notification_channel_setting(
            channel_setting_id,
            UpdateNotificationChannelSettingRequest(
                config={"email": "updated@example.com"}
            )
        )
        print(f"Updated channel setting: {updated_setting.config}")
        
        # Delete the channel setting
        print(f"\n=== Deleting notification channel setting {channel_setting_id} ===")
        delete_result = client.notifications.delete_notification_channel_setting(channel_setting_id)
        print(f"Delete result: {delete_result}")
    except Exception as e:
        print(f"Error in notification channel setting operations: {e}")
    
    # List notification settings
    print("\n=== Listing notification settings ===")
    notification_settings = client.notifications.list_notification_settings()
    print(f"Found {len(notification_settings)} notification settings")
    
    # If there are notification types, create a notification setting
    if notification_types:
        print("\n=== Creating a notification setting ===")
        try:
            notification_setting = client.notifications.create_notification_setting(
                CreateNotificationSettingRequest(
                    channel=NotificationChannel.APP,
                    notification_type_id=notification_types[0].id
                )
            )
            setting_id = notification_setting.id
            print(f"Created notification setting with ID: {setting_id}")
            
            # Get the notification setting
            print(f"\n=== Getting notification setting {setting_id} ===")
            retrieved_setting = client.notifications.get_notification_setting(setting_id)
            print(f"Retrieved setting: {retrieved_setting.name}")
            
            # Update the notification setting
            print(f"\n=== Updating notification setting {setting_id} ===")
            updated_setting = client.notifications.update_notification_setting(
                setting_id,
                UpdateNotificationSettingRequest(
                    status=NotificationSettingStatus.PAUSED
                )
            )
            print(f"Updated setting status: {updated_setting.status}")
            
            # List notification settings by type
            print(f"\n=== Listing notification settings by type {notification_types[0].id} ===")
            settings_by_type = client.notifications.list_notification_settings_by_type(
                notification_type_id=notification_types[0].id,
                expand=True
            )
            print(f"Found {len(settings_by_type)} settings for type {notification_types[0].id}")
            
            # Delete the notification setting
            print(f"\n=== Deleting notification setting {setting_id} ===")
            delete_result = client.notifications.delete_notification_setting(setting_id)
            print(f"Delete result: {delete_result}")
        except Exception as e:
            print(f"Error in notification setting operations: {e}")

if __name__ == "__main__":
    run_notification_examples() 