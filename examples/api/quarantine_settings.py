"""
Example usage of the Quarantine Settings API
"""
import os
from pprint import pprint

from nexla_sdk.models import (
    CreateQuarantineSettingsRequest, UpdateQuarantineSettingsRequest,
    QuarantineConfig, QuarantineResourceType
)
from nexla_sdk.api.quarantine_settings import ResourceTypeEnum

from client import nexla_client

def run_quarantine_settings_examples():
    """Run through examples of using the Quarantine Settings API"""
    client = nexla_client
    
    # First, get your user ID and a credential ID to use
    print("\n=== Getting user information ===")
    current_user = client.users.get_current_user()
    user_id = current_user.id
    print(f"Using user ID: {user_id}")
    
    # Get credentials to use for quarantine settings
    print("\n=== Getting credentials ===")
    credentials = client.credentials.list()
    if not credentials.items:
        print("No credentials found for quarantine settings")
        return
    
    # Find an S3 or file storage credential
    credential = None
    for cred in credentials.items:
        if cred.type in ('s3', 'gcs', 'azure_blob'):
            credential = cred
            break
    
    if not credential:
        print("No suitable file storage credentials found (S3, GCS, Azure Blob)")
        return
    
    credential_id = credential.id
    print(f"Using credential ID: {credential_id} (type: {credential.type})")
    
    # Try to get existing quarantine settings
    print(f"\n=== Checking existing quarantine settings for user {user_id} ===")
    try:
        existing_settings = client.quarantine_settings.get_user_quarantine_settings(user_id)
        print(f"Found existing quarantine settings with ID: {existing_settings.id}")
        print(f"Current settings: {existing_settings.config}")
        
        # Update existing quarantine settings
        print(f"\n=== Updating quarantine settings for user {user_id} ===")
        
        # Prepare update settings request
        update_request = UpdateQuarantineSettingsRequest(
            config=QuarantineConfig(
                start_cron="0 0 * 1/1 * ? *",
                path=f"test/nexla/{user_id}/updated"
            )
        )
        
        updated_settings = client.quarantine_settings.update_quarantine_settings(
            user_id, update_request
        )
        
        print(f"Updated settings: {updated_settings.config}")
        
    except Exception as e:
        print(f"No existing quarantine settings found: {e}")
        
        # Create new quarantine settings
        print(f"\n=== Creating new quarantine settings for user {user_id} ===")
        
        # Prepare create settings request
        create_request = CreateQuarantineSettingsRequest(
            data_credentials_id=credential_id,
            config=QuarantineConfig(
                start_cron="0 0 * 1/1 * ? *",
                path=f"test/nexla/{user_id}"
            )
        )
        
        try:
            new_settings = client.quarantine_settings.create_quarantine_settings(
                user_id, create_request
            )
            
            print(f"Created new quarantine settings with ID: {new_settings.id}")
            print(f"Settings: {new_settings.config}")
        except Exception as e:
            print(f"Failed to create quarantine settings: {e}")
    
    # Get a source ID to test resource quarantine settings
    print("\n=== Getting a source to set up quarantine settings ===")
    sources = client.sources.list(limit=1)
    if not sources.items:
        print("No sources found to set up quarantine settings")
        return
    
    source_id = sources.items[0].id
    print(f"Using source ID: {source_id}")
    
    # Create or update quarantine settings for a source
    print(f"\n=== Setting up quarantine settings for source {source_id} ===")
    
    # Check if source already has quarantine settings
    try:
        source_settings = client.quarantine_settings.get_quarantine_settings(
            ResourceTypeEnum.DATA_SOURCES, source_id
        )
        print(f"Found existing source quarantine settings with ID: {source_settings.id}")
        
        # Update source quarantine settings
        source_update_request = UpdateQuarantineSettingsRequest(
            config=QuarantineConfig(
                start_cron="0 0 * 1/1 * ? *",
                path=f"test/nexla/source/{source_id}/updated"
            )
        )
        
        updated_source_settings = client.quarantine_settings.update_resource_quarantine_settings(
            ResourceTypeEnum.DATA_SOURCES, source_id, source_update_request
        )
        
        print(f"Updated source settings: {updated_source_settings.config}")
        
    except Exception as e:
        print(f"No existing source quarantine settings: {e}")
        
        # Create new source quarantine settings
        source_create_request = CreateQuarantineSettingsRequest(
            data_credentials_id=credential_id,
            config=QuarantineConfig(
                start_cron="0 0 * 1/1 * ? *", 
                path=f"test/nexla/source/{source_id}"
            )
        )
        
        try:
            new_source_settings = client.quarantine_settings.create_resource_quarantine_settings(
                ResourceTypeEnum.DATA_SOURCES, source_id, source_create_request
            )
            
            print(f"Created new source quarantine settings with ID: {new_source_settings.id}")
            print(f"Settings: {new_source_settings.config}")
        except Exception as e:
            print(f"Failed to create source quarantine settings: {e}")
    
    # List all quarantine settings
    print("\n=== Listing all quarantine settings ===")
    try:
        all_settings = client.quarantine_settings.list_quarantine_settings()
        print(f"Found {len(all_settings)} quarantine settings")
        
        for i, setting in enumerate(all_settings):
            print(f"\nSetting {i+1}:")
            print(f"  ID: {setting.id}")
            print(f"  Resource Type: {setting.resource_type}")
            print(f"  Resource ID: {setting.resource_id}")
            print(f"  Path: {setting.config.path}")
        
        # Filter by resource type
        print("\n=== Listing quarantine settings for users ===")
        user_settings = client.quarantine_settings.list_quarantine_settings(
            resource_type=QuarantineResourceType.USER
        )
        print(f"Found {len(user_settings)} user quarantine settings")
        
        # Filter by resource type and ID
        print(f"\n=== Listing quarantine settings for user {user_id} ===")
        specific_user_settings = client.quarantine_settings.list_quarantine_settings(
            resource_type=QuarantineResourceType.USER,
            resource_id=user_id
        )
        print(f"Found {len(specific_user_settings)} quarantine settings for user {user_id}")
    
    except Exception as e:
        print(f"Failed to list quarantine settings: {e}")
    
    # Get quarantine samples for the source
    print(f"\n=== Getting quarantine samples for source {source_id} ===")
    try:
        from datetime import datetime, timedelta
        
        # Calculate start and end times for the past 30 days
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)
        
        quarantine_samples = client.sources.get_quarantine_samples(
            source_id=source_id,
            page=1,
            per_page=10,
            start_time=start_time,
            end_time=end_time
        )
        
        if "output" in quarantine_samples and "data" in quarantine_samples["output"]:
            samples = quarantine_samples["output"]["data"]
            print(f"Found {len(samples)} quarantine samples")
            
            if samples:
                sample = samples[0]
                print("\n=== Sample error record ===")
                if "error" in sample:
                    print(f"Error message: {sample['error'].get('message', 'N/A')}")
                if "rawMessage" in sample:
                    print(f"Raw message: {sample['rawMessage']}")
        else:
            print("No quarantine samples found or unexpected response format")
            
    except Exception as e:
        print(f"Failed to get quarantine samples: {e}")
    
    # Clean up test settings (optional)
    print("\n=== Cleaning up test quarantine settings ===")
    try:
        # Delete user quarantine settings
        client.quarantine_settings.delete_quarantine_settings(user_id)
        print(f"Deleted user {user_id} quarantine settings")
        
        # Delete source quarantine settings
        client.quarantine_settings.delete_resource_quarantine_settings(
            ResourceTypeEnum.DATA_SOURCES, source_id
        )
        print(f"Deleted source {source_id} quarantine settings")
    except Exception as e:
        print(f"Failed to delete quarantine settings: {e}")

if __name__ == "__main__":
    run_quarantine_settings_examples() 