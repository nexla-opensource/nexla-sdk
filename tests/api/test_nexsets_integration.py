"""
Integration tests for the Nexsets API (Data Sets)

These tests validate the full lifecycle of a nexset (data set):
1. Create a nexset
2. Get the nexset
3. Update the nexset
4. Get the nexset schema
5. Update the nexset schema
6. List nexsets and verify our nexset is included
7. Add/remove tags
8. Get sample data
9. Delete the nexset
"""
import logging
import os
import uuid
import pytest
from typing import Dict, Any, List

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError
from nexla_sdk.models.nexsets import (
    Nexset,
    NexsetList,
    NexsetSchema,
    NexsetSample,
    NexsetCharacteristics
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
def simple_schema():
    """Return a simple schema for testing"""
    return {
        "attributes": [
            {
                "name": "id",
                "type": "integer",
                "nullable": False,
                "primary_key": True
            },
            {
                "name": "name",
                "type": "string",
                "nullable": True
            },
            {
                "name": "value",
                "type": "double",
                "nullable": True
            }
        ],
        "version": 1,
        "source_format": "csv"
    }


@pytest.fixture(scope="module")
def test_nexset(nexla_client: NexlaClient, unique_test_id, simple_schema):
    """Create a test nexset for integration testing"""
    logger.info(f"Creating test nexset with ID: {unique_test_id}")
    
    # Get an existing nexset to use as a parent
    try:
        # First try to find existing nexsets
        nexsets = nexla_client.nexsets.list(per_page=1)
        if nexsets and nexsets.items:
            parent_id = nexsets.items[0].id
            logger.info(f"Using existing nexset with ID {parent_id} as parent")
            
            # Create a simple nexset
            nexset_data = {
                "name": f"Test Nexset {unique_test_id}",
                "description": "Created by SDK integration tests",
                "parent_data_set_id": parent_id,
                "has_custom_transform": True,
                "transform": {
                    "version": 1,
                    "data_maps": [],
                    "transforms": [],
                    "custom": True
                }
            }
            
            # Create the nexset
            nexset = nexla_client.nexsets.create(nexset_data)
            logger.info(f"Test nexset created with ID: {nexset.id}")
            logger.debug(f"Nexset details: {nexset}")
            
            # Return the created nexset for tests to use
            yield nexset
            
            # Clean up by deleting the nexset after tests are done
            try:
                logger.info(f"Cleaning up test nexset with ID: {nexset.id}")
                delete_response = nexla_client.nexsets.delete(nexset.id)
                logger.info(f"Nexset deletion response: {delete_response}")
            except Exception as e:
                logger.error(f"Error cleaning up test nexset: {e}")
        else:
            logger.warning("No existing nexsets found to use as parent, skipping test")
            pytest.skip("No existing nexsets found to use as parent")
            yield None
    except Exception as e:
        logger.error(f"Error creating test nexset: {e}")
        pytest.skip(f"Error setting up test nexset: {e}")
        yield None


class TestNexsetsIntegration:
    """Integration tests for the Nexsets API"""
    
    def test_nexset_lifecycle(self, nexla_client: NexlaClient, unique_test_id, simple_schema):
        """
        Test the complete lifecycle of a nexset:
        create -> get -> update -> get schema -> update schema -> add tags -> delete
        """
        try:
            # First get an existing nexset to use as a parent
            nexsets = nexla_client.nexsets.list(per_page=1)
            if not nexsets or not nexsets.items:
                pytest.skip("No existing nexsets found to use as parent")
                return
                
            parent_id = nexsets.items[0].id
            logger.info(f"Using existing nexset with ID {parent_id} as parent")
            
            # STEP 1: Create a new nexset
            logger.info("Step 1: Creating a new nexset")
            nexset_name = f"Lifecycle Test Nexset {unique_test_id}"
            nexset_data = {
                "name": nexset_name,
                "description": "Created by SDK lifecycle test",
                "parent_data_set_id": parent_id,
                "has_custom_transform": True,
                "transform": {
                    "version": 1,
                    "data_maps": [],
                    "transforms": [],
                    "custom": True
                }
            }
            
            new_nexset = nexla_client.nexsets.create(nexset_data)
            logger.info(f"Created nexset with ID: {new_nexset.id}")
            logger.debug(f"New nexset details: {new_nexset}")
            
            assert isinstance(new_nexset, Nexset)
            assert hasattr(new_nexset, "id")
            assert hasattr(new_nexset, "name")
            if hasattr(new_nexset, "name"):  # Some API versions might return different objects
                assert new_nexset.name == nexset_name
            
            nexset_id = new_nexset.id
            
            # STEP 2: Get the nexset
            logger.info(f"Step 2: Getting nexset with ID: {nexset_id}")
            retrieved_nexset = nexla_client.nexsets.get(nexset_id)
            logger.debug(f"Retrieved nexset details: {retrieved_nexset}")
            
            assert isinstance(retrieved_nexset, Nexset)
            assert retrieved_nexset.id == nexset_id
            assert retrieved_nexset.name == nexset_name
            
            # STEP 3: Get nexset with expand=True (if supported)
            try:
                logger.info(f"Step 3: Getting expanded nexset with ID: {nexset_id}")
                expanded_nexset = nexla_client.nexsets.get(nexset_id, expand=True)
                logger.debug(f"Expanded nexset details: {expanded_nexset}")
                
                assert isinstance(expanded_nexset, Nexset)
                assert expanded_nexset.id == nexset_id
                # Expanded nexset should have more details
                assert hasattr(expanded_nexset, "schema_") or hasattr(expanded_nexset, "schema")
            except (NexlaAPIError, AttributeError) as e:
                # Some API versions might not support expand
                logger.warning(f"Expanded nexset details not supported: {e}")
            
            # STEP 4: Update the nexset
            logger.info(f"Step 4: Updating nexset with ID: {nexset_id}")
            updated_name = f"Updated {nexset_name}"
            updated_description = "Updated by SDK lifecycle test"
            
            updated_nexset = nexla_client.nexsets.update(
                dataset_id=nexset_id,
                dataset_data={
                    "name": updated_name,
                    "description": updated_description
                }
            )
            logger.debug(f"Updated nexset details: {updated_nexset}")
            
            assert isinstance(updated_nexset, Nexset)
            assert updated_nexset.id == nexset_id
            assert updated_nexset.name == updated_name
            assert updated_nexset.description == updated_description
            
            # STEP 5: Try to get nexset schema
            try:
                logger.info(f"Step 5: Trying to get schema for nexset with ID: {nexset_id}")
                schema = nexla_client.nexsets.get_schema(nexset_id)
                logger.debug(f"Nexset schema: {schema}")
                
                assert isinstance(schema, NexsetSchema)
                assert hasattr(schema, "attributes")
                assert len(schema.attributes) > 0
                
                # STEP 6: Try to update nexset schema (if supported and if schema exists)
                try:
                    logger.info(f"Step 6: Attempting to update schema for nexset with ID: {nexset_id}")
                    
                    # Add a new attribute to the schema
                    current_schema = schema.model_dump()
                    current_schema["attributes"].append({
                        "name": "timestamp",
                        "type": "timestamp",
                        "nullable": True
                    })
                    
                    updated_schema = nexla_client.nexsets.update_schema(nexset_id, current_schema)
                    logger.debug(f"Updated schema: {updated_schema}")
                    
                    assert isinstance(updated_schema, NexsetSchema)
                    assert len(updated_schema.attributes) == len(schema.attributes) + 1
                    assert any(attr.name == "timestamp" for attr in updated_schema.attributes)
                except (NexlaAPIError, AttributeError) as e:
                    # Schema update might not be supported for this type
                    logger.warning(f"Schema update not supported: {e}")
            except (NexlaAPIError, AttributeError) as e:
                # Schema might not be available for this type of nexset
                logger.warning(f"Schema not available: {e}")
            
            # STEP 7: List nexsets and verify our nexset is included
            logger.info("Step 7: Listing nexsets and verifying our nexset is included")
            nexsets_list = nexla_client.nexsets.list()
            logger.debug(f"Nexsets list first few items: {nexsets_list.items[:5] if len(nexsets_list.items) >= 5 else nexsets_list.items}")
            
            assert isinstance(nexsets_list, NexsetList)
            # Check if our nexset is in the list
            nexset_ids = [n.id for n in nexsets_list.items if hasattr(n, 'id')]
            assert nexset_id in nexset_ids
            
            # STEP 8: Add tags to the nexset (if supported)
            try:
                logger.info(f"Step 8a: Adding tags to nexset with ID: {nexset_id}")
                tags = ["sdk-test", unique_test_id]
                
                # Update nexset with tags
                tagged_nexset = nexla_client.nexsets.update(
                    dataset_id=nexset_id,
                    dataset_data={"tags": tags}
                )
                logger.debug(f"Nexset after adding tags: {tagged_nexset}")
                
                # Verify tags were added by getting the nexset
                nexset_with_tags = nexla_client.nexsets.get(nexset_id)
                logger.debug(f"Retrieved nexset with tags: {nexset_with_tags}")
                
                if hasattr(nexset_with_tags, "tags") and nexset_with_tags.tags:
                    for tag in tags:
                        assert tag in nexset_with_tags.tags
                        logger.info(f"Verified tag was added: {tag}")
                else:
                    logger.warning("Tags attribute not available or empty")
                
                # Remove tags
                logger.info(f"Step 8b: Removing tags from nexset with ID: {nexset_id}")
                untagged_nexset = nexla_client.nexsets.update(
                    dataset_id=nexset_id,
                    dataset_data={"tags": []}
                )
                logger.debug(f"Nexset after removing tags: {untagged_nexset}")
                
                # Verify tags were removed
                nexset_without_tags = nexla_client.nexsets.get(nexset_id)
                logger.debug(f"Retrieved nexset after removing tags: {nexset_without_tags}")
                
                if hasattr(nexset_without_tags, "tags"):
                    assert not nexset_without_tags.tags or len(nexset_without_tags.tags) == 0
                    logger.info("Verified all tags were removed")
                
            except (NexlaAPIError, AttributeError) as e:
                # Tag operations might not be supported
                logger.warning(f"Tag operations not supported: {e}")
            
            # STEP 9: Try to get sample data (if available)
            try:
                logger.info(f"Step 9: Trying to get sample data for nexset with ID: {nexset_id}")
                samples = nexla_client.nexsets.get_sample_data(nexset_id, limit=5)
                logger.debug(f"Sample data: {samples}")
                
                assert isinstance(samples, (NexsetSample, List))
                
                # Try to get characteristics (if available)
                try:
                    logger.info(f"Getting characteristics for nexset with ID: {nexset_id}")
                    characteristics = nexla_client.nexsets.get_characteristics(nexset_id)
                    logger.debug(f"Nexset characteristics: {characteristics}")
                    
                    assert isinstance(characteristics, NexsetCharacteristics)
                except (NexlaAPIError, AttributeError) as e:
                    logger.warning(f"Characteristics not available: {e}")
                
            except (NexlaAPIError, AttributeError) as e:
                # Sample data might not be available
                logger.warning(f"Sample data not available: {e}")
            
            # STEP 10: Delete the nexset
            logger.info(f"Step 10: Deleting nexset with ID: {nexset_id}")
            delete_response = nexla_client.nexsets.delete(nexset_id)
            logger.debug(f"Delete response: {delete_response}")
            
            # STEP 11: Verify the nexset is deleted by trying to get it (should fail)
            logger.info(f"Step 11: Verifying nexset is deleted by trying to get it")
            with pytest.raises(NexlaAPIError) as excinfo:
                nexla_client.nexsets.get(nexset_id)
                
            assert excinfo.value.status_code == 404 or 400 <= excinfo.value.status_code < 500
            
        except Exception as e:
            logger.error(f"Test failed: {e}")
            
            # Clean up in case of test failure
            try:
                if 'nexset_id' in locals():
                    logger.info(f"Cleaning up nexset with ID: {nexset_id}")
                    nexla_client.nexsets.delete(nexset_id)
            except Exception as cleanup_err:
                logger.error(f"Error during cleanup: {cleanup_err}")
                
            # Re-raise the original exception
            raise Exception(f"Nexset lifecycle test failed: {e}") from e
    
    def test_nexset_copy(self, nexla_client: NexlaClient, test_nexset):
        """Test copying a nexset"""
        try:
            # Copy the test nexset
            logger.info(f"Copying nexset with ID: {test_nexset.id}")
            
            copied_nexset = nexla_client.nexsets.copy(
                dataset_id=test_nexset.id,
                new_name=f"Copy of {test_nexset.name}",
                copy_access_controls=True
            )
            logger.info(f"Created copy with ID: {copied_nexset.id}")
            logger.debug(f"Copied nexset details: {copied_nexset}")
            
            assert isinstance(copied_nexset, Nexset)
            assert copied_nexset.id != test_nexset.id
            assert copied_nexset.name.startswith("Copy of ") or "copy" in copied_nexset.name.lower()
            
            # Clean up by deleting the copied nexset
            logger.info(f"Cleaning up copied nexset with ID: {copied_nexset.id}")
            delete_response = nexla_client.nexsets.delete(copied_nexset.id)
            logger.info(f"Nexset deletion response: {delete_response}")
            
        except Exception as e:
            logger.error(f"Copy test failed: {e}")
            
            # Clean up in case of test failure
            try:
                if 'copied_nexset' in locals() and hasattr(copied_nexset, 'id'):
                    logger.info(f"Cleaning up copied nexset with ID: {copied_nexset.id}")
                    nexla_client.nexsets.delete(copied_nexset.id)
            except Exception as cleanup_err:
                logger.error(f"Error during cleanup: {cleanup_err}")
                
            # Re-raise the original exception
            raise Exception(f"Nexset copy test failed: {e}") from e
    
    def test_nexset_activate_pause(self, nexla_client: NexlaClient, test_nexset):
        """Test activating and pausing a nexset"""
        try:
            # Activate the nexset
            logger.info(f"Activating nexset with ID: {test_nexset.id}")
            
            try:
                activated_nexset = nexla_client.nexsets.activate(test_nexset.id)
                logger.debug(f"Activated nexset details: {activated_nexset}")
                
                assert isinstance(activated_nexset, Nexset)
                assert activated_nexset.id == test_nexset.id
                if hasattr(activated_nexset, "status"):
                    assert activated_nexset.status and activated_nexset.status != "paused"
                
                # Pause the nexset
                logger.info(f"Pausing nexset with ID: {test_nexset.id}")
                paused_nexset = nexla_client.nexsets.pause(test_nexset.id)
                logger.debug(f"Paused nexset details: {paused_nexset}")
                
                assert isinstance(paused_nexset, Nexset)
                assert paused_nexset.id == test_nexset.id
                if hasattr(paused_nexset, "status"):
                    assert paused_nexset.status and (
                        paused_nexset.status == "paused" or
                        "pause" in str(paused_nexset.status).lower()
                    )
                
            except (NexlaAPIError, AttributeError) as e:
                # Activate/pause might not be supported for this nexset
                logger.warning(f"Activate/pause operations not supported: {e}")
                pytest.skip(f"Activate/pause operations not supported: {e}")
            
        except Exception as e:
            logger.error(f"Activate/pause test failed: {e}")
            # Re-raise the exception
            raise Exception(f"Nexset activate/pause test failed: {e}") from e 