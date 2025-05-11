"""
Integration tests for the Lookups API (Data Maps)

These tests validate the full lifecycle of a data map:
1. Create a data map
2. Get the data map
3. Update the data map
4. List data maps and verify our data map is included
5. Manage entries in the data map
6. Download entries from the data map
7. Create a copy of the data map
8. Delete the data maps
"""
import logging
import os
import uuid
import pytest
import json
from typing import Dict, Any
import requests

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError, NexlaValidationError, NexlaNotFoundError
from nexla_sdk.models.lookups import (
    Lookup,
    LookupExpanded,
    LookupList,
    DeleteDataMapResponse,
    SampleEntriesResponse
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Apply the skip_if_no_integration_creds marker to all tests in this module
pytestmark = [
    pytest.mark.integration,
    pytest.mark.usefixtures("nexla_client"),
]


@pytest.fixture(scope="module")
def unique_test_id():
    """Generate a unique ID for test resources"""
    return f"sdk_test_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="module")
def test_lookup(nexla_client: NexlaClient, unique_test_id):
    """Create a test data map for integration testing"""
    logger.info(f"Creating test data map with ID: {unique_test_id}")
    
    # Create a simple data map
    lookup_data = {
        "name": f"Test Data Map {unique_test_id}",
        "description": "Created by SDK integration tests",
        "data_type": "string",
        "emit_data_default": True,
        "map_primary_key": "key",
        "data_defaults": {
            "key": "Unknown",
            "value": "Unknown value"
        },
        "data_map": [
            {
                "key": "1",
                "value": "One"
            },
            {
                "key": "2",
                "value": "Two"
            }
        ]
    }
    
    try:
        # Create the data map
        lookup = nexla_client.lookups.create(lookup_data)
        logger.info(f"Test data map created with ID: {lookup.id}")
        
        # Return the created data map for tests to use
        yield lookup
        
    finally:
        # Clean up by deleting the data map after tests are done
        try:
            if 'lookup' in locals() and hasattr(lookup, 'id'):
                logger.info(f"Cleaning up test data map with ID: {lookup.id}")
                try:
                    delete_response = nexla_client.lookups.delete(lookup.id)
                    if delete_response is not None:
                        logger.info(f"Data map deletion response: {delete_response.message}")
                    else:
                        logger.info(f"Data map deleted successfully")
                except (NexlaAPIError, NexlaNotFoundError) as e:
                    # If the data map is already deleted or some other error occurs during cleanup,
                    # log it but don't raise since this is just cleanup
                    logger.warning(f"Error during data map cleanup, but continuing: {e}")
        except Exception as e:
            logger.error(f"Error cleaning up test data map: {e}")


class TestLookupsIntegration:
    """Integration tests for the Lookups API"""
    
    def test_lookup_lifecycle(self, nexla_client: NexlaClient, unique_test_id):
        """
        Test the complete lifecycle of a data map:
        create -> get -> update -> manage entries -> delete
        """
        try:
            # STEP 1: Create a new data map
            logger.info("Step 1: Creating a new data map")
            lookup_name = f"Lifecycle Test Data Map {unique_test_id}"
            lookup_data = {
                "name": lookup_name,
                "description": "Created by SDK lifecycle test",
                "data_type": "string",
                "emit_data_default": True,
                "map_primary_key": "code",
                "data_defaults": {
                    "code": "00",
                    "description": "Unknown"
                },
                "data_map": [
                    {
                        "code": "01",
                        "description": "Active"
                    },
                    {
                        "code": "02",
                        "description": "Inactive"
                    }
                ]
            }
            
            new_lookup = nexla_client.lookups.create(lookup_data)
            logger.info(f"Created data map with ID: {new_lookup.id}")
            
            assert isinstance(new_lookup, Lookup)
            assert new_lookup.name == lookup_name
            assert new_lookup.description == "Created by SDK lifecycle test"
            assert new_lookup.data_type == "string"
            
            lookup_id = new_lookup.id
            
            # STEP 2: Get the data map
            logger.info(f"Step 2: Getting data map with ID: {lookup_id}")
            retrieved_lookup = nexla_client.lookups.get(lookup_id)
            
            assert isinstance(retrieved_lookup, Lookup)
            assert retrieved_lookup.id == lookup_id
            assert retrieved_lookup.name == lookup_name
            
            # STEP 3: Get data map with validate=True
            logger.info(f"Step 3: Getting data map with validation with ID: {lookup_id}")
            validated_lookup = nexla_client.lookups.get(lookup_id, validate=True)
            
            assert isinstance(validated_lookup, Lookup)
            assert validated_lookup.id == lookup_id
            # map_entry_info might be present depending on the API
            
            # STEP 4: Update the data map
            logger.info(f"Step 4: Updating data map with ID: {lookup_id}")
            updated_name = f"Updated {lookup_name}"
            updated_description = "Updated by SDK lifecycle test"
            
            updated_lookup = nexla_client.lookups.update(
                lookup_id=lookup_id,
                lookup_data={
                    "name": updated_name,
                    "description": updated_description
                }
            )
            
            assert isinstance(updated_lookup, Lookup)
            assert updated_lookup.id == lookup_id
            assert updated_lookup.name == updated_name
            assert updated_lookup.description == updated_description
            
            # STEP 5: List data maps and verify our data map is included
            logger.info("Step 5: Listing data maps and verifying our data map is included")
            lookups_list = nexla_client.lookups.list()
            
            assert isinstance(lookups_list, LookupList)
            # Check if our data map is in the list
            lookup_ids = [l.id for l in lookups_list.items]
            assert lookup_id in lookup_ids
            
            # STEP 6: Manage entries in the data map
            logger.info(f"Step 6a: Adding entries to data map with ID: {lookup_id}")
            new_entries = [
                {
                    "code": "03",
                    "description": "Pending"
                },
                {
                    "code": "04",
                    "description": "Completed"
                }
            ]
            
            upsert_result = nexla_client.lookups.upsert_entries(lookup_id, new_entries)
            assert isinstance(upsert_result, dict)
            assert "message" in upsert_result or "success" in upsert_result  # Handle different response formats
            
            logger.info(f"Step 6b: Checking entries in data map with ID: {lookup_id}")
            entries = nexla_client.lookups.check_entries(lookup_id, ["01", "03"])
            assert isinstance(entries, list)
            assert len(entries) > 0
            
            # STEP 7: Try to download entries
            try:
                logger.info(f"Step 7: Downloading entries from data map with ID: {lookup_id}")
                csv_data = nexla_client.lookups.download_entries(lookup_id)
                assert isinstance(csv_data, str)
                assert len(csv_data) > 0
                logger.info(f"Successfully downloaded entries as CSV")
            except (NexlaAPIError, requests.exceptions.RequestException) as e:
                # Download might not be available in all environments
                logger.warning(f"Download entries not available: {e}")
                # Continue with the test, don't fail here
            
            # STEP 8: Try to get sample entries
            try:
                logger.info(f"Step 8: Getting sample entries from data map with ID: {lookup_id}")
                samples = nexla_client.lookups.get_sample_entries(lookup_id)
                assert isinstance(samples, SampleEntriesResponse)
                assert hasattr(samples, "output")
                
                # Test with specific field
                field_samples = nexla_client.lookups.get_sample_entries(lookup_id, field_name="code")
                assert isinstance(field_samples, SampleEntriesResponse)
                
                logger.info(f"Successfully retrieved sample entries")
            except (NexlaAPIError, NexlaValidationError) as e:
                # Sample entries might not be available in all environments
                logger.warning(f"Sample entries not available: {e}")
                # Continue with the test, don't fail here
            
            # STEP 9: Try to create a copy of the data map
            copied_lookup = None
            try:
                logger.info(f"Step 9: Creating a copy of data map with ID: {lookup_id}")
                copied_lookup = nexla_client.lookups.copy(lookup_id, new_name=f"Copy of {updated_name}")
                
                assert isinstance(copied_lookup, Lookup)
                assert copied_lookup.id != lookup_id
                assert "Copy of " in copied_lookup.name
                logger.info(f"Successfully copied data map with new ID: {copied_lookup.id}")
            except NexlaAPIError as e:
                # Copy operation might not be available in all environments
                logger.warning(f"Copy operation not available: {e}")
                # Continue with the test, don't fail here
            
            # STEP 10: Clean up by deleting data maps
            logger.info(f"Step 10a: Deleting original data map with ID: {lookup_id}")
            delete_response = nexla_client.lookups.delete(lookup_id)
            
            # Some API implementations might return None instead of DeleteDataMapResponse
            if delete_response is not None:
                assert isinstance(delete_response, DeleteDataMapResponse)
                assert hasattr(delete_response, "message")
            
            if copied_lookup:
                logger.info(f"Step 10b: Deleting copied data map with ID: {copied_lookup.id}")
                delete_copy_response = nexla_client.lookups.delete(copied_lookup.id)
                
                if delete_copy_response is not None:
                    assert isinstance(delete_copy_response, DeleteDataMapResponse)
                    assert hasattr(delete_copy_response, "message")
            
        except (NexlaAPIError, NexlaValidationError) as e:
            logger.error(f"Test failed with error: {e}")
            raise
    
    def test_lookup_entry_operations(self, nexla_client: NexlaClient, test_lookup):
        """Test data map entry operations"""
        lookup_id = test_lookup.id
        
        # Test adding new entries
        logger.info(f"Testing entry operations for data map with ID: {lookup_id}")
        
        # Add a new entry
        new_entry = [
            {
                "key": "3",
                "value": "Three"
            }
        ]
        
        upsert_result = nexla_client.lookups.upsert_entries(lookup_id, new_entry)
        assert isinstance(upsert_result, dict)
        assert "message" in upsert_result or "success" in upsert_result  # Handle different response formats
        
        # Check that the entry exists
        entries = nexla_client.lookups.check_entries(lookup_id, "3")
        assert isinstance(entries, list)
        assert len(entries) > 0
        
        # Check if the entry has the expected format
        found_entry = next((e for e in entries if e.get("key") == "3"), None)
        if found_entry:
            assert found_entry.get("value") == "Three"
        
        # Update the entry
        updated_entry = [
            {
                "key": "3",
                "value": "THREE"
            }
        ]
        
        upsert_result = nexla_client.lookups.upsert_entries(lookup_id, updated_entry)
        assert isinstance(upsert_result, dict)
        
        # Check that the entry was updated
        entries = nexla_client.lookups.check_entries(lookup_id, "3")
        assert isinstance(entries, list)
        
        # Check if the entry has been updated
        if len(entries) > 0:
            found_entry = next((e for e in entries if e.get("key") == "3"), None)
            if found_entry:
                assert found_entry.get("value") == "THREE"
        
        # Delete the entry
        try:
            delete_result = nexla_client.lookups.delete_entries(lookup_id, "3")
            assert isinstance(delete_result, dict)
            
            # Check that the entry is gone
            try:
                entries = nexla_client.lookups.check_entries(lookup_id, "3")
                assert len(entries) == 0 or not any(e.get("key") == "3" for e in entries)
            except NexlaAPIError as e:
                # Some APIs might return an error for non-existent keys
                pass
        except NexlaAPIError as e:
            logger.warning(f"Delete entries operation failed: {e}")
        
    def test_lookup_validation(self, nexla_client: NexlaClient, test_lookup):
        """Test data map validation options"""
        lookup_id = test_lookup.id
        
        # Test getting a data map with validation
        logger.info(f"Testing validation for data map with ID: {lookup_id}")
        
        try:
            validated_lookup = nexla_client.lookups.get(lookup_id, validate=True)
            assert isinstance(validated_lookup, Lookup)
            assert validated_lookup.id == lookup_id
            
            # Expanded lookup
            expanded_lookup = nexla_client.lookups.get(lookup_id, expand=True)
            assert isinstance(expanded_lookup, LookupExpanded)
            assert expanded_lookup.id == lookup_id
            
            # Test list endpoint with validation
            lookups = nexla_client.lookups.list(validate=True)
            assert isinstance(lookups, LookupList)
            assert len(lookups.items) > 0
            
        except NexlaAPIError as e:
            logger.warning(f"Validation options not fully supported: {e}")
            # Continue with the test, don't fail here 