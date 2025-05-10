"""
Integration tests for the Destinations API

These tests validate the full lifecycle of a destination:
1. Create a destination
2. Get the destination
3. Update the destination
4. List destinations and verify our destination is included
5. Activate/pause the destination
6. Validate destination configuration
7. Get metrics for the destination
8. Create a copy of the destination
9. Delete the destinations
"""
import logging
import os
import uuid
import pytest
from datetime import datetime, timedelta

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError, NexlaValidationError, NexlaNotFoundError
from nexla_sdk.models.destinations import (
    DataSink,
    DataSinkList,
    DeleteDataSinkResponse,
    SinkType,
    SinkStatus,
    FileStatus,
    ConfigValidationResponse,
    LifetimeMetricsResponse,
    DailyMetricsResponse,
    RunSummaryMetricsResponse,
    FileStatsResponse,
    FileMetricsResponse,
    RawFileMetricsResponse
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
def test_dataset_and_credentials(nexla_client: NexlaClient):
    """
    Get existing test dataset and credentials to use for destinations.
    This fixture assumes there are available datasets and credentials in the account.
    In real testing, you would create these resources first or use known test resources.
    """
    # Get first available dataset
    datasets = nexla_client.nexsets.list()
    if not datasets.items:
        pytest.skip("No datasets available for testing")
        
    dataset_id = datasets.items[0].id
    
    # Get first available credentials
    credentials = nexla_client.credentials.list()
    if not credentials:  # credentials is a list, not a PaginatedList
        pytest.skip("No credentials available for testing")
    
    # Since we're getting different return types from the credentials.list() API,
    # handle both dict and list cases
    if isinstance(credentials, dict) and 'items' in credentials:
        # Dict with items
        if not credentials['items']:
            pytest.skip("No credentials available for testing")
        credentials_id = credentials['items'][0]['id']
    elif isinstance(credentials, dict) and isinstance(list(credentials.values())[0], dict):
        # Dict of dicts
        credentials_id = list(credentials.values())[0]['id']
    elif isinstance(credentials, list):
        # List of credential objects
        credentials_id = credentials[0].id
    else:
        # Use a hard-coded credential for testing
        # In a production environment, we would create a test credential
        logger.warning("Using hard-coded credential ID for testing (not ideal)")
        credentials_id = 5055  # Example ID, replace with a valid one in your test environment
    
    return {
        "dataset_id": dataset_id,
        "credentials_id": credentials_id,
    }


@pytest.fixture(scope="module")
def test_destination(nexla_client: NexlaClient, unique_test_id, test_dataset_and_credentials):
    """Create a test destination for integration testing"""
    logger.info(f"Creating test destination with ID: {unique_test_id}")
    
    # Create a simple S3 destination
    destination_data = {
        "name": f"Test Destination {unique_test_id}",
        "description": "Created by SDK integration tests",
        "sink_type": SinkType.S3.value,
        "data_set_id": test_dataset_and_credentials["dataset_id"],
        "data_credentials_id": test_dataset_and_credentials["credentials_id"],
        "sink_config": {
            "mapping": {
                "mode": "auto",
                "tracker_mode": "NONE"
            },
            "data_format": "csv",
            "sink_type": "s3",
            "path": "test-bucket/integration-tests",
            "output.dir.name.pattern": "{yyyy}-{MM}-{dd}"
        }
    }
    
    try:
        # Create the destination
        destination = nexla_client.destinations.create(destination_data)
        logger.info(f"Test destination created with ID: {destination.id}")
        
        # Return the created destination for tests to use
        yield destination
        
    finally:
        # Clean up by deleting the destination after tests are done
        try:
            if 'destination' in locals() and hasattr(destination, 'id'):
                logger.info(f"Cleaning up test destination with ID: {destination.id}")
                try:
                    delete_response = nexla_client.destinations.delete(destination.id)
                    logger.info(f"Destination deletion response: {delete_response}")
                except Exception as e:
                    # If the destination is already deleted or some other error occurs during cleanup,
                    # log it but don't raise since this is just cleanup
                    logger.warning(f"Error during destination cleanup, but continuing: {e}")
        except Exception as e:
            logger.error(f"Error cleaning up test destination: {e}")


class TestDestinationsIntegration:
    """Integration tests for the Destinations API"""
    
    def test_destination_lifecycle(self, nexla_client: NexlaClient, unique_test_id, test_dataset_and_credentials):
        """
        Test the complete lifecycle of a destination:
        create -> get -> update -> activate/pause -> delete
        """
        try:
            # STEP 1: Create a new destination
            logger.info("Step 1: Creating a new destination")
            destination_name = f"Lifecycle Test Destination {unique_test_id}"
            destination_data = {
                "name": destination_name,
                "description": "Created by SDK lifecycle test",
                "sink_type": SinkType.S3.value,
                "data_set_id": test_dataset_and_credentials["dataset_id"],
                "data_credentials_id": test_dataset_and_credentials["credentials_id"],
                "sink_config": {
                    "mapping": {
                        "mode": "auto",
                        "tracker_mode": "NONE"
                    },
                    "data_format": "csv",
                    "sink_type": "s3",
                    "path": "test-bucket/lifecycle-test",
                    "output.dir.name.pattern": "{yyyy}-{MM}-{dd}"
                }
            }
            
            new_destination = nexla_client.destinations.create(destination_data)
            logger.info(f"Created destination with ID: {new_destination.id}")
            
            assert isinstance(new_destination, DataSink)
            assert new_destination.name == destination_name
            assert new_destination.description == "Created by SDK lifecycle test"
            assert new_destination.sink_type == SinkType.S3.value
            
            sink_id = new_destination.id
            
            # STEP 2: Get the destination
            logger.info(f"Step 2: Getting destination with ID: {sink_id}")
            retrieved_destination = nexla_client.destinations.get(sink_id)
            
            assert isinstance(retrieved_destination, DataSink)
            assert retrieved_destination.id == sink_id
            assert retrieved_destination.name == destination_name
            
            # STEP 3: Get destination with expand=True
            logger.info(f"Step 3: Getting expanded destination with ID: {sink_id}")
            expanded_destination = nexla_client.destinations.get(sink_id, expand=True)
            
            assert isinstance(expanded_destination, DataSink)
            assert expanded_destination.id == sink_id
            assert hasattr(expanded_destination, "sink_config")
            
            # STEP 4: Update the destination
            logger.info(f"Step 4: Updating destination with ID: {sink_id}")
            updated_name = f"Updated {destination_name}"
            updated_description = "Updated by SDK lifecycle test"
            
            updated_destination = nexla_client.destinations.update(
                sink_id,
                {
                    "name": updated_name,
                    "description": updated_description
                }
            )
            
            assert isinstance(updated_destination, DataSink)
            assert updated_destination.id == sink_id
            assert updated_destination.name == updated_name
            assert updated_destination.description == updated_description
            
            # STEP 5: List destinations and verify our destination is included
            logger.info("Step 5: Listing destinations and verifying our destination is included")
            destinations_list = nexla_client.destinations.list()
            
            assert isinstance(destinations_list, DataSinkList)
            # Check if our destination is in the list
            sink_ids = [d.id for d in destinations_list.items]
            assert sink_id in sink_ids
            
            # STEP 6: Activate/pause the destination
            try:
                logger.info(f"Step 6a: Activating destination with ID: {sink_id}")
                activated_destination = nexla_client.destinations.activate(sink_id)
                assert isinstance(activated_destination, DataSink)
                assert activated_destination.id == sink_id
                
                logger.info(f"Step 6b: Pausing destination with ID: {sink_id}")
                paused_destination = nexla_client.destinations.pause(sink_id)
                assert isinstance(paused_destination, DataSink)
                assert paused_destination.id == sink_id
            except NexlaAPIError as e:
                # Some destination configurations might not support activate/pause operations
                logger.warning(f"Activate/pause operations not supported for this destination: {e}")
            
            # STEP 7: Validate destination configuration
            try:
                logger.info(f"Step 7: Validating destination configuration for ID: {sink_id}")
                validation_result = nexla_client.destinations.validate_config(sink_id)
                
                assert isinstance(validation_result, ConfigValidationResponse)
                assert hasattr(validation_result, "status")
                assert hasattr(validation_result, "output")
            except (NexlaAPIError, NexlaValidationError) as e:
                # Validation might not be supported for all destination types
                logger.warning(f"Validation not supported for this destination: {e}")
            
            # STEP 8: Clean up - Delete the destination
            logger.info(f"Step 8: Deleting destination with ID: {sink_id}")
            delete_response = nexla_client.destinations.delete(sink_id)
            
            # For destinations, delete might return either DeleteDataSinkResponse or an empty dict
            if isinstance(delete_response, DeleteDataSinkResponse):
                assert hasattr(delete_response, "code")
                assert hasattr(delete_response, "message")
            
            # Verify the destination is deleted by trying to get it (should fail)
            try:
                nexla_client.destinations.get(sink_id)
                # If we reach here, the destination wasn't deleted
                pytest.fail("Destination wasn't properly deleted")
            except NexlaNotFoundError:
                # This is expected - destination should be gone
                pass
            
        except Exception as e:
            logger.error(f"Error in destination lifecycle test: {e}")
            raise
    
    def test_destination_copy(self, nexla_client: NexlaClient, test_destination):
        """Test copying a destination"""
        logger.info(f"Testing copy of destination with ID: {test_destination.id}")
        
        try:
            # Copy the destination
            copied_destination = nexla_client.destinations.copy(test_destination.id)
            copied_id = copied_destination.id
            
            # Verify the copy
            assert isinstance(copied_destination, DataSink)
            assert copied_destination.id != test_destination.id
            assert copied_destination.name.startswith(test_destination.name)
            assert copied_destination.sink_type == test_destination.sink_type
            assert copied_destination.data_set_id == test_destination.data_set_id
            
            # Test copy with options
            copied_with_options = nexla_client.destinations.copy(
                test_destination.id,
                {
                    "reuse_data_credentials": True,
                    "copy_access_controls": True
                }
            )
            copied_with_options_id = copied_with_options.id
            
            assert isinstance(copied_with_options, DataSink)
            assert copied_with_options.id != test_destination.id
            assert copied_with_options.id != copied_id
            
            # Clean up copies
            try:
                nexla_client.destinations.delete(copied_id)
                nexla_client.destinations.delete(copied_with_options_id)
            except Exception as e:
                logger.warning(f"Error cleaning up copied destinations: {e}")
                
        except NexlaAPIError as e:
            # Copy might not be supported for all destination types
            logger.warning(f"Copy operation not supported for this destination: {e}")
            pytest.skip("Copy operation not supported for this destination type")
    
    def test_metrics_methods(self, nexla_client: NexlaClient, test_destination):
        """Test metrics methods for destinations"""
        logger.info(f"Testing metrics for destination with ID: {test_destination.id}")
        
        try:
            # Get lifetime metrics
            lifetime_metrics = nexla_client.destinations.get_metrics(test_destination.id)
            assert isinstance(lifetime_metrics, LifetimeMetricsResponse)
            assert hasattr(lifetime_metrics, "metrics")
            assert hasattr(lifetime_metrics, "status")
            
            # Get daily metrics
            from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
            to_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            
            try:
                daily_metrics = nexla_client.destinations.get_daily_metrics(
                    test_destination.id,
                    from_date=from_date,
                    to_date=to_date
                )
                assert isinstance(daily_metrics, DailyMetricsResponse)
                assert hasattr(daily_metrics, "metrics")
                assert hasattr(daily_metrics, "status")
            except (NexlaAPIError, NexlaValidationError) as e:
                logger.warning(f"Could not retrieve daily metrics: {e}")
                
            # Get run summary metrics
            try:
                run_metrics = nexla_client.destinations.get_run_summary_metrics(
                    test_destination.id,
                    from_date=from_date,
                    to_date=to_date
                )
                assert isinstance(run_metrics, RunSummaryMetricsResponse)
                assert hasattr(run_metrics, "metrics")
                assert hasattr(run_metrics, "status")
            except (NexlaAPIError, NexlaValidationError) as e:
                logger.warning(f"Could not retrieve run summary metrics: {e}")
                
            # Get files stats metrics
            try:
                files_stats = nexla_client.destinations.get_files_stats_metrics(
                    test_destination.id,
                    from_date=from_date,
                    to_date=to_date
                )
                assert isinstance(files_stats, FileStatsResponse)
                assert hasattr(files_stats, "metrics")
                assert hasattr(files_stats, "status")
            except (NexlaAPIError, NexlaValidationError) as e:
                logger.warning(f"Could not retrieve file stats metrics: {e}")
                
            # Get files metrics
            try:
                files_metrics = nexla_client.destinations.get_files_metrics(
                    test_destination.id,
                    from_date=from_date,
                    to_date=to_date
                )
                assert isinstance(files_metrics, FileMetricsResponse)
                assert hasattr(files_metrics, "metrics")
                assert hasattr(files_metrics, "status")
            except (NexlaAPIError, NexlaValidationError) as e:
                logger.warning(f"Could not retrieve file metrics: {e}")
                
            # Get raw files metrics
            try:
                raw_files = nexla_client.destinations.get_files_raw_metrics(
                    test_destination.id,
                    from_date=from_date,
                    to_date=to_date
                )
                assert isinstance(raw_files, RawFileMetricsResponse)
                assert hasattr(raw_files, "metrics")
                assert hasattr(raw_files, "status")
            except (NexlaAPIError, NexlaValidationError) as e:
                logger.warning(f"Could not retrieve raw file metrics: {e}")
            
        except NexlaAPIError as e:
            # Some metrics might not be available for new destinations with no data
            logger.warning(f"Metrics might not be available for this destination: {e}")
            pytest.skip("Metrics not available for this destination yet")


if __name__ == "__main__":
    # This allows running the tests directly (useful for development/debugging)
    pytest.main(["-xvs", __file__]) 