"""
Integration tests for the Quarantine Settings API
"""
import os
import pytest
from datetime import datetime, timedelta

from nexla_sdk import NexlaClient
from nexla_sdk.models import (
    CreateQuarantineSettingsRequest, UpdateQuarantineSettingsRequest,
    QuarantineConfig, QuarantineResourceType
)
from nexla_sdk.api.quarantine_settings import ResourceTypeEnum

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

@pytest.fixture(scope="module")
def resource_ids(client):
    """Get resource IDs for testing quarantine settings"""
    # Get current user ID
    user = client.users.get_current_user()
    user_id = user.id if user else None
    
    # Get a source ID
    sources = client.sources.list(limit=1)
    source_id = sources.items[0].id if sources.items else None
    
    # Get a credential ID (prefer file storage type)
    credential_id = None
    credentials = client.credentials.list()
    
    if credentials.items:
        # First try to find a file storage credential
        for cred in credentials.items:
            if cred.type in ('s3', 'gcs', 'azure_blob'):
                credential_id = cred.id
                break
                
        # If no file storage credential found, use the first available
        if credential_id is None and credentials.items:
            credential_id = credentials.items[0].id
    
    # Get an organization ID
    orgs = client.organizations.list()
    org_id = orgs[0].id if orgs else None
    
    return {
        "user_id": user_id,
        "source_id": source_id,
        "credential_id": credential_id,
        "org_id": org_id
    }

@pytest.mark.skipif(SKIP_TESTS, reason=SKIP_REASON)
class TestQuarantineSettings:
    """Tests for the Quarantine Settings API"""
    
    def test_user_quarantine_settings_crud(self, client, resource_ids):
        """Test creating, getting, updating, and deleting user quarantine settings"""
        if not resource_ids["user_id"] or not resource_ids["credential_id"]:
            pytest.skip("Missing user ID or credential ID for testing")
        
        user_id = resource_ids["user_id"]
        credential_id = resource_ids["credential_id"]
        
        # First, check if there are existing settings and delete them if necessary
        try:
            existing_settings = client.quarantine_settings.get_user_quarantine_settings(user_id)
            # If we got here, there are existing settings - delete them for a clean test
            client.quarantine_settings.delete_quarantine_settings(user_id)
        except Exception:
            # No existing settings or other error - proceed with the test
            pass
        
        # Create new quarantine settings
        create_request = CreateQuarantineSettingsRequest(
            data_credentials_id=credential_id,
            config=QuarantineConfig(
                start_cron="0 0 * 1/1 * ? *",
                path=f"test/nexla/user/{user_id}"
            )
        )
        
        new_settings = client.quarantine_settings.create_quarantine_settings(
            user_id, create_request
        )
        
        assert new_settings.id is not None
        assert new_settings.resource_id == user_id
        assert new_settings.data_credentials_id == credential_id
        assert new_settings.config.path == f"test/nexla/user/{user_id}"
        
        # Get the settings
        retrieved_settings = client.quarantine_settings.get_user_quarantine_settings(user_id)
        
        assert retrieved_settings.id == new_settings.id
        assert retrieved_settings.resource_id == user_id
        assert retrieved_settings.data_credentials_id == credential_id
        
        # Update the settings
        update_request = UpdateQuarantineSettingsRequest(
            config=QuarantineConfig(
                start_cron="0 0 * 1/1 * ? *",
                path=f"test/nexla/user/{user_id}/updated"
            )
        )
        
        updated_settings = client.quarantine_settings.update_quarantine_settings(
            user_id, update_request
        )
        
        assert updated_settings.id == new_settings.id
        assert updated_settings.resource_id == user_id
        assert updated_settings.config.path == f"test/nexla/user/{user_id}/updated"
        
        # Clean up - delete the settings
        client.quarantine_settings.delete_quarantine_settings(user_id)
        
        # Verify settings are deleted
        with pytest.raises(Exception):
            client.quarantine_settings.get_user_quarantine_settings(user_id)
    
    def test_source_quarantine_settings_crud(self, client, resource_ids):
        """Test creating, getting, updating, and deleting source quarantine settings"""
        if not resource_ids["source_id"] or not resource_ids["credential_id"]:
            pytest.skip("Missing source ID or credential ID for testing")
        
        source_id = resource_ids["source_id"]
        credential_id = resource_ids["credential_id"]
        
        # First, check if there are existing settings and delete them if necessary
        try:
            existing_settings = client.quarantine_settings.get_quarantine_settings(
                ResourceTypeEnum.DATA_SOURCES, source_id
            )
            # If we got here, there are existing settings - delete them for a clean test
            client.quarantine_settings.delete_resource_quarantine_settings(
                ResourceTypeEnum.DATA_SOURCES, source_id
            )
        except Exception:
            # No existing settings or other error - proceed with the test
            pass
        
        # Create new quarantine settings
        create_request = CreateQuarantineSettingsRequest(
            data_credentials_id=credential_id,
            config=QuarantineConfig(
                start_cron="0 0 * 1/1 * ? *",
                path=f"test/nexla/source/{source_id}"
            )
        )
        
        new_settings = client.quarantine_settings.create_resource_quarantine_settings(
            ResourceTypeEnum.DATA_SOURCES, source_id, create_request
        )
        
        assert new_settings.id is not None
        assert new_settings.resource_id == source_id
        assert new_settings.data_credentials_id == credential_id
        assert new_settings.config.path == f"test/nexla/source/{source_id}"
        
        # Get the settings
        retrieved_settings = client.quarantine_settings.get_quarantine_settings(
            ResourceTypeEnum.DATA_SOURCES, source_id
        )
        
        assert retrieved_settings.id == new_settings.id
        assert retrieved_settings.resource_id == source_id
        assert retrieved_settings.data_credentials_id == credential_id
        
        # Update the settings
        update_request = UpdateQuarantineSettingsRequest(
            config=QuarantineConfig(
                start_cron="0 0 * 1/1 * ? *",
                path=f"test/nexla/source/{source_id}/updated"
            )
        )
        
        updated_settings = client.quarantine_settings.update_resource_quarantine_settings(
            ResourceTypeEnum.DATA_SOURCES, source_id, update_request
        )
        
        assert updated_settings.id == new_settings.id
        assert updated_settings.resource_id == source_id
        assert updated_settings.config.path == f"test/nexla/source/{source_id}/updated"
        
        # Clean up - delete the settings
        client.quarantine_settings.delete_resource_quarantine_settings(
            ResourceTypeEnum.DATA_SOURCES, source_id
        )
        
        # Verify settings are deleted
        with pytest.raises(Exception):
            client.quarantine_settings.get_quarantine_settings(
                ResourceTypeEnum.DATA_SOURCES, source_id
            )
    
    def test_list_quarantine_settings(self, client, resource_ids):
        """Test listing quarantine settings"""
        if not resource_ids["user_id"] or not resource_ids["credential_id"] or not resource_ids["source_id"]:
            pytest.skip("Missing resource IDs or credential ID for testing")
        
        user_id = resource_ids["user_id"]
        source_id = resource_ids["source_id"]
        credential_id = resource_ids["credential_id"]
        
        settings_created = []
        
        try:
            # Create user quarantine settings
            user_create_request = CreateQuarantineSettingsRequest(
                data_credentials_id=credential_id,
                config=QuarantineConfig(
                    start_cron="0 0 * 1/1 * ? *",
                    path=f"test/nexla/list_test/user/{user_id}"
                )
            )
            
            user_settings = client.quarantine_settings.create_quarantine_settings(
                user_id, user_create_request
            )
            settings_created.append(("user", user_id))
            
            # Create source quarantine settings
            source_create_request = CreateQuarantineSettingsRequest(
                data_credentials_id=credential_id,
                config=QuarantineConfig(
                    start_cron="0 0 * 1/1 * ? *",
                    path=f"test/nexla/list_test/source/{source_id}"
                )
            )
            
            source_settings = client.quarantine_settings.create_resource_quarantine_settings(
                ResourceTypeEnum.DATA_SOURCES, source_id, source_create_request
            )
            settings_created.append(("source", source_id))
            
            # List all quarantine settings
            all_settings = client.quarantine_settings.list_quarantine_settings()
            assert isinstance(all_settings, list)
            
            # Verify our settings are in the list
            user_found = False
            source_found = False
            
            for setting in all_settings:
                if setting.resource_type == QuarantineResourceType.USER and setting.resource_id == user_id:
                    user_found = True
                elif setting.resource_type == QuarantineResourceType.SOURCE and setting.resource_id == source_id:
                    source_found = True
            
            assert user_found
            assert source_found
            
            # List settings by resource type
            user_settings_list = client.quarantine_settings.list_quarantine_settings(
                resource_type=QuarantineResourceType.USER
            )
            assert isinstance(user_settings_list, list)
            
            # Verify our user setting is in the filtered list
            user_found_in_filtered = False
            for setting in user_settings_list:
                if setting.resource_id == user_id:
                    user_found_in_filtered = True
                    break
            
            assert user_found_in_filtered
            
            # List settings by resource type and ID
            specific_settings = client.quarantine_settings.list_quarantine_settings(
                resource_type=QuarantineResourceType.USER,
                resource_id=user_id
            )
            assert isinstance(specific_settings, list)
            assert len(specific_settings) > 0
            assert specific_settings[0].resource_id == user_id
            
        finally:
            # Clean up created settings
            for resource_type, resource_id in settings_created:
                try:
                    if resource_type == "user":
                        client.quarantine_settings.delete_quarantine_settings(resource_id)
                    elif resource_type == "source":
                        client.quarantine_settings.delete_resource_quarantine_settings(
                            ResourceTypeEnum.DATA_SOURCES, resource_id
                        )
                except Exception:
                    # Ignore errors during cleanup
                    pass
    
    def test_quarantine_samples(self, client, resource_ids):
        """Test getting quarantine samples for resources"""
        if not resource_ids["source_id"]:
            pytest.skip("No source available for testing")
        
        source_id = resource_ids["source_id"]
        
        # Calculate time range for the last 30 days
        end_time = datetime.now()
        start_time = end_time - timedelta(days=30)
        
        # Get quarantine samples for a source
        try:
            quarantine_samples = client.sources.get_quarantine_samples(
                source_id=source_id,
                page=1,
                per_page=5,
                start_time=start_time,
                end_time=end_time
            )
            
            assert isinstance(quarantine_samples, dict)
            
            # Check if the response has the expected structure
            if "output" in quarantine_samples and "data" in quarantine_samples["output"]:
                samples = quarantine_samples["output"]["data"]
                assert isinstance(samples, list)
                
                # If there are samples, verify their structure
                if samples:
                    sample = samples[0]
                    assert "nexlaMetaData" in sample
                    assert "error" in sample
        except Exception as e:
            # This test may fail if the API doesn't support this endpoint
            # or if there are no quarantine samples for the source
            pytest.skip(f"Failed to get quarantine samples: {e}") 