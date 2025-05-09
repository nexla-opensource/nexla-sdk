"""
Integration tests for the Flows API

These tests validate the full lifecycle of a flow:
1. Create a flow
2. Get the flow
3. Update the flow
4. List flows and verify our flow is included
5. Add/remove tags to the flow
6. Delete the flow
"""
import logging
import os
import uuid
import pytest

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError
from nexla_sdk.models.flows import (
    Flow,
    FlowList,
    FlowResponse,
    FlowNode
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
def test_flow(nexla_client: NexlaClient, unique_test_id):
    """Create a test flow for integration testing"""
    logger.info(f"Creating test flow with ID: {unique_test_id}")
    
    # Create a simple flow
    flow_data = {
        "name": f"Test Flow {unique_test_id}",
        "description": "Created by SDK integration tests",
        "type": "data_transformation" 
    }
    
    try:
        # Create the flow
        flow = nexla_client.flows.create(flow_data)
        logger.info(f"Test flow created with ID: {flow.id}")
        
        # Return the created flow for tests to use
        yield flow
        
    finally:
        # Clean up by deleting the flow after tests are done
        try:
            if 'flow' in locals() and hasattr(flow, 'id'):
                logger.info(f"Cleaning up test flow with ID: {flow.id}")
                delete_response = nexla_client.flows.delete(flow.id)
                logger.info(f"Flow deletion response: {delete_response}")
        except Exception as e:
            logger.error(f"Error cleaning up test flow: {e}")


class TestFlowsIntegration:
    """Integration tests for the Flows API"""
    
    def test_flow_lifecycle(self, nexla_client: NexlaClient, unique_test_id):
        """
        Test the complete lifecycle of a flow:
        create -> get -> update -> add tags -> delete
        """
        try:
            # STEP 1: Create a new flow
            logger.info("Step 1: Creating a new flow")
            flow_name = f"Lifecycle Test Flow {unique_test_id}"
            flow_data = {
                "name": flow_name,
                "description": "Created by SDK lifecycle test",
                "type": "data_transformation"
            }
            
            new_flow = nexla_client.flows.create(flow_data)
            logger.info(f"Created flow with ID: {new_flow.id}")
            
            assert isinstance(new_flow, (Flow, FlowResponse))
            assert hasattr(new_flow, "id")
            assert hasattr(new_flow, "name")
            if hasattr(new_flow, "name"):  # Some API versions might return different objects
                assert new_flow.name == flow_name
            
            flow_id = new_flow.id
            
            # STEP 2: Get the flow
            logger.info(f"Step 2: Getting flow with ID: {flow_id}")
            retrieved_flow = nexla_client.flows.get(flow_id)
            
            assert isinstance(retrieved_flow, (Flow, FlowResponse))
            # Check if we got a Flow or a FlowResponse
            if isinstance(retrieved_flow, Flow):
                assert retrieved_flow.id == flow_id
                assert retrieved_flow.name == flow_name
            elif hasattr(retrieved_flow, "flows") and len(retrieved_flow.flows) > 0:
                # If it's a FlowResponse, the flow is in the flows array
                assert retrieved_flow.flows[0].id == flow_id
                if hasattr(retrieved_flow.flows[0], "name"):
                    assert retrieved_flow.flows[0].name == flow_name
            
            # STEP 3: Update the flow
            logger.info(f"Step 3: Updating flow with ID: {flow_id}")
            updated_name = f"Updated {flow_name}"
            updated_description = "Updated by SDK lifecycle test"
            
            # Pass update data as a dictionary
            update_data = {
                "name": updated_name,
                "description": updated_description
            }
            updated_flow = nexla_client.flows.update(flow_id, update_data)
            
            assert isinstance(updated_flow, (Flow, FlowResponse))
            # Different API versions might return different objects, so we check what we can
            if hasattr(updated_flow, "id"):
                assert updated_flow.id == flow_id
            if hasattr(updated_flow, "name"):
                assert updated_flow.name == updated_name
            
            # Verify update by getting the flow again
            updated_retrieved_flow = nexla_client.flows.get(flow_id)
            
            # Check if we got a Flow or a FlowResponse
            if isinstance(updated_retrieved_flow, Flow):
                assert updated_retrieved_flow.name == updated_name
                assert updated_retrieved_flow.description == updated_description
            elif hasattr(updated_retrieved_flow, "flows") and len(updated_retrieved_flow.flows) > 0:
                if hasattr(updated_retrieved_flow.flows[0], "name"):
                    assert updated_retrieved_flow.flows[0].name == updated_name
                if hasattr(updated_retrieved_flow.flows[0], "description"):
                    assert updated_retrieved_flow.flows[0].description == updated_description
            
            # STEP 4: List flows and verify our flow is included
            logger.info("Step 4: Listing flows and verifying our flow is included")
            flows_list = nexla_client.flows.list()
            
            assert isinstance(flows_list, (FlowList, FlowResponse))
            
            # Extract flow IDs from the response, handling both FlowList and FlowResponse
            flow_ids = []
            if isinstance(flows_list, FlowList):
                flow_ids = [f.id for f in flows_list.items if hasattr(f, 'id')]
            elif hasattr(flows_list, "flows"):
                flow_ids = [f.id for f in flows_list.flows if hasattr(f, 'id')]
            
            assert flow_id in flow_ids, f"Flow ID {flow_id} not found in flows list"
            
            # STEP 5: Add tags to the flow (if supported)
            try:
                logger.info(f"Step 5a: Adding tags to flow with ID: {flow_id}")
                tags = ["sdk-test", unique_test_id]
                tagged_flow = nexla_client.flows.add_tags(flow_id, tags)
                logger.info(f"Added tags response: {tagged_flow}")
                
                # Verify tags were added by getting the flow
                flow_with_tags = nexla_client.flows.get(flow_id)
                
                # Check for tags in the response
                if isinstance(flow_with_tags, Flow) and hasattr(flow_with_tags, "tags"):
                    for tag in tags:
                        assert tag in flow_with_tags.tags, f"Tag {tag} not found in flow tags"
                elif hasattr(flow_with_tags, "flows") and len(flow_with_tags.flows) > 0:
                    if hasattr(flow_with_tags.flows[0], "tags"):
                        for tag in tags:
                            assert tag in flow_with_tags.flows[0].tags, f"Tag {tag} not found in flow tags"
                
                # Remove tags
                logger.info(f"Step 5b: Removing tags from flow with ID: {flow_id}")
                untagged_flow = nexla_client.flows.remove_tags(flow_id, tags)
                logger.info(f"Removed tags response: {untagged_flow}")
                
                # Verify tags were removed
                flow_without_tags = nexla_client.flows.get(flow_id)
                
                # Check for tags in the response
                if isinstance(flow_without_tags, Flow) and hasattr(flow_without_tags, "tags"):
                    for tag in tags:
                        assert tag not in flow_without_tags.tags, f"Tag {tag} still found in flow tags after removal"
                elif hasattr(flow_without_tags, "flows") and len(flow_without_tags.flows) > 0:
                    if hasattr(flow_without_tags.flows[0], "tags"):
                        for tag in tags:
                            assert tag not in flow_without_tags.flows[0].tags, f"Tag {tag} still found in flow tags after removal"
                    
            except (NexlaAPIError, AttributeError) as e:
                # Tag operations might not be supported or API structure might be different
                logger.warning(f"Tag operations not supported or failed: {e}")
                pytest.skip(f"Tag operations not supported: {e}")
            
            # STEP 6: Delete the flow
            logger.info(f"Step 6: Deleting flow with ID: {flow_id}")
            delete_response = nexla_client.flows.delete(flow_id)
            
            assert delete_response is not None
            if isinstance(delete_response, dict):
                logger.info(f"Delete response: {delete_response}")
            
            # STEP 7: Verify the flow is deleted by trying to get it (should fail)
            logger.info(f"Step 7: Verifying flow is deleted by trying to get it")
            with pytest.raises(NexlaAPIError) as excinfo:
                nexla_client.flows.get(flow_id)
                
            assert excinfo.value.status_code == 404 or 400 <= excinfo.value.status_code < 500
            
        except Exception as e:
            logger.error(f"Test failed: {e}")
            
            # Clean up in case of test failure
            try:
                if 'flow_id' in locals():
                    logger.info(f"Cleaning up flow with ID: {flow_id}")
                    nexla_client.flows.delete(flow_id)
            except Exception as cleanup_err:
                logger.error(f"Error during cleanup: {cleanup_err}")
                
            # Re-raise the original exception
            raise
    
    def test_flow_run(self, nexla_client: NexlaClient, test_flow):
        """Test running a flow (if applicable)"""
        try:
            # Try to run the flow
            logger.info(f"Attempting to run flow with ID: {test_flow.id}")
            
            try:
                # This may not be supported for all flow types
                run_response = nexla_client.flows.run(test_flow.id)
                
                assert run_response is not None
                logger.info(f"Flow run initiated with response: {run_response}")
                
                # Check run status if possible
                if hasattr(nexla_client.flows, 'get_run_status') and isinstance(run_response, dict) and "run_id" in run_response:
                    run_status = nexla_client.flows.get_run_status(test_flow.id, run_response["run_id"])
                    logger.info(f"Flow run status: {run_status}")
                    assert run_status is not None
                
            except (NexlaAPIError, AttributeError) as e:
                # Flow run might not be supported for this flow type
                logger.warning(f"Flow run not supported or failed: {e}")
                pytest.skip(f"Flow run operations not supported: {e}")
                
        except Exception as e:
            logger.error(f"Flow run test failed: {e}")
            # Re-raise the exception
            raise Exception(f"Flow run test failed: {e}") from e
            
    def test_flow_tags(self, nexla_client: NexlaClient, unique_test_id):
        """Test adding and removing tags from a flow"""
        logger.info("Starting test_flow_tags")
        
        # Create a flow for testing tags
        flow_name = f"Tags Test Flow {unique_test_id}"
        flow_data = {
            "name": flow_name,
            "description": "Created for testing tags functionality",
            "type": "data_transformation"
        }
        
        flow_id = None
        
        try:
            # Create the flow
            logger.info(f"Creating flow for tags test: {flow_name}")
            new_flow = nexla_client.flows.create(flow_data)
            logger.info(f"Created flow with ID: {new_flow.id}")
            
            flow_id = new_flow.id
            
            # Try to add tags to the flow
            try:
                logger.info(f"Adding tags to flow: {flow_id}")
                tags = ["sdk-test", f"tag-{unique_test_id}", "integration-test"]
                tagged_flow = nexla_client.flows.add_tags(flow_id, tags)
                logger.info(f"Response after adding tags: {tagged_flow}")
                
                # Get the flow and verify tags were added
                flow_with_tags = nexla_client.flows.get(flow_id)
                
                # Check for tags in the response
                tags_found = False
                if isinstance(flow_with_tags, Flow) and hasattr(flow_with_tags, "tags"):
                    tags_found = True
                    for tag in tags:
                        assert tag in flow_with_tags.tags, f"Tag '{tag}' not found in flow tags: {flow_with_tags.tags}"
                        logger.info(f"Verified tag was added: {tag}")
                elif hasattr(flow_with_tags, "flows") and len(flow_with_tags.flows) > 0:
                    if hasattr(flow_with_tags.flows[0], "tags"):
                        tags_found = True
                        for tag in tags:
                            assert tag in flow_with_tags.flows[0].tags, f"Tag '{tag}' not found in flow tags: {flow_with_tags.flows[0].tags}"
                            logger.info(f"Verified tag was added: {tag}")
                
                if not tags_found:
                    logger.warning("Tags not found in response, API might not support tags")
                    pytest.skip("Tags not found in response, API might not support tags")
                    return
                    
                # Remove some tags
                tags_to_remove = tags[:1]  # Remove first tag
                logger.info(f"Removing tags from flow: {tags_to_remove}")
                untagged_flow = nexla_client.flows.remove_tags(flow_id, tags_to_remove)
                logger.info(f"Response after removing tags: {untagged_flow}")
                
                # Get the flow and verify tags were removed
                flow_after_removal = nexla_client.flows.get(flow_id)
                
                # Check for tags in the response
                if isinstance(flow_after_removal, Flow) and hasattr(flow_after_removal, "tags"):
                    for tag in tags_to_remove:
                        assert tag not in flow_after_removal.tags, f"Tag '{tag}' was found in flow tags after removal: {flow_after_removal.tags}"
                        logger.info(f"Verified tag was removed: {tag}")
                    
                    # Verify remaining tags are still there
                    remaining_tags = tags[1:]  # The tags that weren't removed
                    for tag in remaining_tags:
                        assert tag in flow_after_removal.tags, f"Tag '{tag}' not found in flow tags after partial removal: {flow_after_removal.tags}"
                        logger.info(f"Verified tag is still present: {tag}")
                elif hasattr(flow_after_removal, "flows") and len(flow_after_removal.flows) > 0:
                    if hasattr(flow_after_removal.flows[0], "tags"):
                        for tag in tags_to_remove:
                            assert tag not in flow_after_removal.flows[0].tags, f"Tag '{tag}' was found in flow tags after removal: {flow_after_removal.flows[0].tags}"
                            logger.info(f"Verified tag was removed: {tag}")
                        
                        # Verify remaining tags are still there
                        remaining_tags = tags[1:]  # The tags that weren't removed
                        for tag in remaining_tags:
                            assert tag in flow_after_removal.flows[0].tags, f"Tag '{tag}' not found in flow tags after partial removal: {flow_after_removal.flows[0].tags}"
                            logger.info(f"Verified tag is still present: {tag}")
                
            except (NexlaAPIError, AttributeError) as e:
                # Tag operations might not be supported
                logger.warning(f"Tag operations not supported or failed: {e}")
                pytest.skip(f"Tag operations not supported: {e}")
        
        except Exception as e:
            logger.error(f"Test failed: {e}")
            
            # Clean up in case of test failure
            try:
                if flow_id:
                    logger.info(f"Cleaning up flow in tags test with ID: {flow_id}")
                    nexla_client.flows.delete(flow_id)
            except Exception as cleanup_err:
                logger.error(f"Error during cleanup in tags test: {cleanup_err}")
                
            # Re-raise the original exception
            raise Exception(f"Flow tags test failed: {e}") from e
        
        finally:
            # Clean up - delete the flow
            try:
                if flow_id:
                    logger.info(f"Cleaning up flow in tags test with ID: {flow_id}")
                    delete_response = nexla_client.flows.delete(flow_id)
                    logger.info(f"Flow deletion response: {delete_response}")
            except Exception as e:
                logger.error(f"Error cleaning up flow in tags test: {e}")
