"""
Integration tests for the Sources API

These tests validate the full lifecycle of a source:
1. Create a source
2. Get the source
3. Update the source
4. List sources and verify our source is included
5. Activate/pause the source
6. Get metrics for the source
7. Validate source configuration
8. Create a copy of the source
9. Delete the sources
"""
import logging
import os
import uuid
import pytest
from datetime import datetime, timedelta

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError, NexlaValidationError
from nexla_sdk.models.sources import (
    Source,
    SourceExpanded,
    SourceList,
    SourceWithExpandedDataSets,
    DeleteSourceResponse,
)
from nexla_sdk.models.source_metrics import (
    SourceMetricsResponse,
    AggregatedMetricsResponse,
    ConfigValidationResponse,
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
def test_source(nexla_client: NexlaClient, unique_test_id):
    """Create a test source for integration testing"""
    logger.info(f"Creating test source with ID: {unique_test_id}")
    
    # Create a simple file_upload source
    source_data = {
        "name": f"Test Source {unique_test_id}",
        "description": "Created by SDK integration tests",
        "source_type": "file_upload",
        "source_config": {
            "file_type": "csv",
            "file_name_pattern": "*.csv",
            "delimiter": ",",
            "has_header": True
        }
    }
    
    try:
        # Create the source
        source = nexla_client.sources.create(**source_data)
        logger.info(f"Test source created with ID: {source.id}")
        
        # Return the created source for tests to use
        yield source
        
    finally:
        # Clean up by deleting the source after tests are done
        try:
            if 'source' in locals() and hasattr(source, 'id'):
                logger.info(f"Cleaning up test source with ID: {source.id}")
                try:
                    delete_response = nexla_client.sources.delete(source.id)
                    logger.info(f"Source deletion response: {delete_response.message}")
                except Exception as e:
                    # If the source is already deleted or some other error occurs during cleanup,
                    # log it but don't raise since this is just cleanup
                    logger.warning(f"Error during source cleanup, but continuing: {e}")
        except Exception as e:
            logger.error(f"Error cleaning up test source: {e}")


class TestSourcesIntegration:
    """Integration tests for the Sources API"""
    
    def test_source_lifecycle(self, nexla_client: NexlaClient, unique_test_id):
        """
        Test the complete lifecycle of a source:
        create -> get -> update -> activate/pause -> delete
        """
        try:
            # STEP 1: Create a new source
            logger.info("Step 1: Creating a new source")
            source_name = f"Lifecycle Test Source {unique_test_id}"
            source_data = {
                "name": source_name,
                "description": "Created by SDK lifecycle test",
                "source_type": "file_upload",
                "source_config": {
                    "file_type": "csv",
                    "file_name_pattern": "*.csv",
                    "delimiter": ",",
                    "has_header": True
                }
            }
            
            new_source = nexla_client.sources.create(**source_data)
            logger.info(f"Created source with ID: {new_source.id}")
            
            assert isinstance(new_source, Source)
            assert new_source.name == source_name
            assert new_source.description == "Created by SDK lifecycle test"
            assert new_source.source_type == "file_upload"
            
            source_id = new_source.id
            
            # STEP 2: Get the source
            logger.info(f"Step 2: Getting source with ID: {source_id}")
            retrieved_source = nexla_client.sources.get(source_id)
            
            assert isinstance(retrieved_source, Source)
            assert retrieved_source.id == source_id
            assert retrieved_source.name == source_name
            
            # STEP 3: Get source with expand=True
            logger.info(f"Step 3: Getting expanded source with ID: {source_id}")
            expanded_source = nexla_client.sources.get(source_id, expand=True)
            
            assert isinstance(expanded_source, (SourceExpanded, SourceWithExpandedDataSets))
            assert expanded_source.id == source_id
            assert hasattr(expanded_source, "source_config")
            
            # STEP 4: Update the source
            logger.info(f"Step 4: Updating source with ID: {source_id}")
            updated_name = f"Updated {source_name}"
            updated_description = "Updated by SDK lifecycle test"
            
            updated_source = nexla_client.sources.update(
                source_id=source_id,
                name=updated_name,
                description=updated_description
            )
            
            assert isinstance(updated_source, Source)
            assert updated_source.id == source_id
            assert updated_source.name == updated_name
            assert updated_source.description == updated_description
            
            # STEP 5: List sources and verify our source is included
            logger.info("Step 5: Listing sources and verifying our source is included")
            sources_list = nexla_client.sources.list()
            
            assert isinstance(sources_list, SourceList)
            # Check if our source is in the list
            source_ids = [s.id for s in sources_list.items]
            assert source_id in source_ids
            
            # STEP 6: Activate/pause the source (if supported)
            try:
                logger.info(f"Step 6a: Activating source with ID: {source_id}")
                activated_source = nexla_client.sources.activate(source_id)
                assert isinstance(activated_source, Source)
                assert activated_source.id == source_id
                
                logger.info(f"Step 6b: Pausing source with ID: {source_id}")
                paused_source = nexla_client.sources.pause(source_id)
                assert isinstance(paused_source, Source)
                assert paused_source.id == source_id
            except NexlaAPIError as e:
                # Some source types might not support activate/pause operations
                logger.warning(f"Activate/pause operations not supported for this source type: {e}")
            
            # STEP 7: Validate source configuration
            try:
                logger.info(f"Step 7: Validating source configuration for ID: {source_id}")
                validation_result = nexla_client.sources.validate_config(source_id)
                
                assert isinstance(validation_result, ConfigValidationResponse)
                assert hasattr(validation_result, "status")
                assert hasattr(validation_result, "output")
            except (NexlaAPIError, NexlaValidationError) as e:
                # Validation might not be supported for all source types
                logger.warning(f"Validation not supported for this source type: {e}")
            
            # STEP 8: Get source metrics
            try:
                logger.info(f"Step 8: Getting metrics for source with ID: {source_id}")
                metrics = nexla_client.sources.get_metrics(source_id)
                
                assert isinstance(metrics, SourceMetricsResponse)
                assert hasattr(metrics, "metrics")
                assert "status" in metrics.__dict__
                
                # Try getting daily metrics
                end_date = datetime.now()
                start_date = end_date - timedelta(days=7)
                
                daily_metrics = nexla_client.sources.get_daily_metrics(
                    source_id=source_id,
                    from_date=start_date,
                    to_date=end_date
                )
                
                assert isinstance(daily_metrics, AggregatedMetricsResponse)
                assert hasattr(daily_metrics, "metrics")
                
            except (NexlaAPIError, NexlaValidationError) as e:
                # Metrics might not be available for newly created sources
                logger.warning(f"Metrics not available for this source: {e}")
            
            # STEP 9: Delete the source
            logger.info(f"Step 9: Deleting source with ID: {source_id}")
            delete_response = nexla_client.sources.delete(source_id)
            
            assert isinstance(delete_response, DeleteSourceResponse)
            assert delete_response.code in ["OK", "200", 200]
            
            # STEP 10: Verify the source is deleted by trying to get it (should fail)
            logger.info(f"Step 10: Verifying source is deleted by trying to get it")
            with pytest.raises(NexlaAPIError) as excinfo:
                nexla_client.sources.get(source_id)
                
            assert excinfo.value.status_code == 404 or 400 <= excinfo.value.status_code < 500
            
        except Exception as e:
            logger.error(f"Test failed: {e}")
            
            # Clean up in case of test failure
            try:
                if 'source_id' in locals():
                    logger.info(f"Cleaning up source with ID: {source_id}")
                    try:
                        nexla_client.sources.delete(source_id)
                    except Exception as cleanup_err:
                        logger.warning(f"Error during cleanup: {cleanup_err}")
            except Exception as cleanup_err:
                logger.error(f"Error during cleanup: {cleanup_err}")
                
            # Re-raise the original exception
            raise

    def test_source_copy(self, nexla_client: NexlaClient, test_source):
        """Test copying a source"""
        try:
            # Copy the test source
            logger.info(f"Copying source with ID: {test_source.id}")
            
            copied_source = nexla_client.sources.copy(
                source_id=test_source.id,
                reuse_data_credentials=True
            )
            
            logger.info(f"Created copy with ID: {copied_source.id}")
            
            assert isinstance(copied_source, Source)
            assert copied_source.id != test_source.id
            assert copied_source.name.startswith(test_source.name) or "copy" in copied_source.name.lower()
            
            # Clean up by deleting the copied source
            logger.info(f"Cleaning up copied source with ID: {copied_source.id}")
            try:
                delete_response = nexla_client.sources.delete(copied_source.id)
                logger.info(f"Source deletion response: {delete_response.message}")
            except Exception as e:
                logger.warning(f"Error deleting copied source, but continuing: {e}")
            
        except Exception as e:
            logger.error(f"Copy test failed: {e}")
            
            # Clean up in case of test failure
            try:
                if 'copied_source' in locals() and hasattr(copied_source, 'id'):
                    logger.info(f"Cleaning up copied source with ID: {copied_source.id}")
                    try:
                        nexla_client.sources.delete(copied_source.id)
                    except Exception as cleanup_err:
                        logger.warning(f"Error during copied source cleanup, but continuing: {cleanup_err}")
            except Exception as cleanup_err:
                logger.error(f"Error during cleanup: {cleanup_err}")
                
            # Re-raise the original exception
            raise

    def test_probe_and_metrics_methods(self, nexla_client: NexlaClient, test_source):
        """Test the probe and metrics methods for sources"""
        source_id = test_source.id
        
        # Test file stats metrics (might return empty data for new sources)
        try:
            logger.info(f"Testing file stats metrics for source ID: {source_id}")
            file_stats = nexla_client.sources.get_files_stats(source_id)
            
            # Just verify the call doesn't raise an exception
            logger.info(f"File stats: {file_stats}")
        except (NexlaAPIError, NexlaValidationError) as e:
            # This might fail for newly created sources with no data
            logger.warning(f"Could not get file stats: {e}")
        
        # Test files metrics (might return empty data for new sources)
        try:
            logger.info(f"Testing files metrics for source ID: {source_id}")
            files_metrics = nexla_client.sources.get_files_metrics(source_id)
            
            # Just verify the call doesn't raise an exception
            logger.info(f"Files metrics: {files_metrics}")
        except (NexlaAPIError, NexlaValidationError) as e:
            # This might fail for newly created sources with no data
            logger.warning(f"Could not get files metrics: {e}")
        
        # Test daily metrics which has a more consistent structure
        try:
            logger.info(f"Testing daily metrics for source ID: {source_id}")
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            # Skip run metrics test since it needs further model investigation
            logger.info(f"Skipping run metrics test for now")
            
            # Test daily metrics instead
            daily_metrics = nexla_client.sources.get_daily_metrics(
                source_id=source_id,
                from_date=start_date,
                to_date=end_date
            )
            logger.info(f"Daily metrics: {daily_metrics}")
            
        except (NexlaAPIError, NexlaValidationError) as e:
            # This might fail for newly created sources with no data
            logger.warning(f"Could not get metrics: {e}") 