"""
Example usage of the Nexla Destinations API

This example demonstrates various operations on data sinks (destinations):
1. Listing destinations
2. Getting a specific destination
3. Creating a new destination
4. Updating a destination
5. Monitoring a destination (metrics)
6. Controlling destination writing (activate/pause)
7. Validating destination configuration
8. Cleaning up (deleting a destination)
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError, NexlaNotFoundError, NexlaValidationError
from nexla_sdk.models.destinations import SinkType, FileStatus
from client import nexla_client


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def list_destinations_example(client: NexlaClient) -> None:
    """Example of listing data destinations"""
    logger.info("Listing data destinations...")
    
    # List all destinations with default pagination (page 1, 100 items per page)
    destinations = client.destinations.list()
    
    # Print count and basic info about each destination
    logger.info(f"Found {len(destinations.items)} destinations:")
    for destination in destinations.items:
        logger.info(f"  ID: {destination.id}, Name: {destination.name}, Type: {destination.sink_type}, Status: {destination.status}")
        
    # You can also filter by access role
    # from nexla_sdk.models.access import AccessRole
    # admin_destinations = client.destinations.list(access_role=AccessRole.ADMIN)
    # logger.info(f"Found {len(admin_destinations.items)} destinations where you have admin access")


def get_destination_example(client: NexlaClient, sink_id: int) -> None:
    """Example of retrieving a specific data destination"""
    logger.info(f"Getting destination with ID {sink_id}...")
    
    try:
        # Get basic destination info
        destination = client.destinations.get(sink_id)
        logger.info(f"Destination details:")
        logger.info(f"  Name: {destination.name}")
        logger.info(f"  Type: {destination.sink_type}")
        logger.info(f"  Status: {destination.status}")
        logger.info(f"  DataSet ID: {destination.data_set_id}")
        if destination.owner:
            logger.info(f"  Owner: {destination.owner.full_name}")
        if destination.org:
            logger.info(f"  Organization: {destination.org.name}")
        
        # Get expanded destination info
        expanded_destination = client.destinations.get(sink_id, expand=True)
        logger.info(f"Expanded destination details:")
        logger.info(f"  Sink config: {json.dumps(expanded_destination.sink_config, indent=2) if expanded_destination.sink_config else None}")
        
    except NexlaNotFoundError as e:
        logger.error(f"Destination not found: {e}")
    except NexlaAPIError as e:
        logger.error(f"Error retrieving destination: {e}")


def create_destination_example(client: NexlaClient, name: str, data_set_id: int, data_cred_id: int) -> Optional[int]:
    """Example of creating a new data destination"""
    logger.info(f"Creating a new destination named '{name}'...")
    
    try:
        # Create a simple S3 destination
        destination = client.destinations.create({
            "name": name,
            "description": "Created via SDK example",
            "sink_type": SinkType.S3.value,
            "data_set_id": data_set_id,
            "data_credentials_id": data_cred_id,
            "sink_config": {
                "mapping": {
                    "mode": "auto",
                    "tracker_mode": "NONE"
                },
                "data_format": "csv",
                "sink_type": "s3",
                "path": "example-bucket/nexla-output",
                "output.dir.name.pattern": "{yyyy}-{MM}-{dd}"
            }
        })
        
        logger.info(f"Destination created successfully with ID: {destination.id}")
        return destination.id
        
    except NexlaAPIError as e:
        logger.error(f"Error creating destination: {e}")
        return None


def update_destination_example(client: NexlaClient, sink_id: int) -> None:
    """Example of updating a data destination"""
    logger.info(f"Updating destination with ID {sink_id}...")
    
    try:
        # Update destination name and description
        updated_destination = client.destinations.update(
            sink_id,
            {
                "name": f"Updated destination {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "description": "Updated via SDK example"
            }
        )
        
        logger.info(f"Destination updated successfully:")
        logger.info(f"  New name: {updated_destination.name}")
        logger.info(f"  New description: {updated_destination.description}")
        
    except NexlaAPIError as e:
        logger.error(f"Error updating destination: {e}")


def control_output_example(client: NexlaClient, sink_id: int) -> None:
    """Example of controlling destination output (activate/pause)"""
    logger.info(f"Controlling output for destination with ID {sink_id}...")
    
    try:
        # Activate the destination
        logger.info("Activating destination...")
        activated_destination = client.destinations.activate(sink_id)
        logger.info(f"Destination activated. Status: {activated_destination.status}")
        
        # Pause the destination
        logger.info("Pausing destination...")
        paused_destination = client.destinations.pause(sink_id)
        logger.info(f"Destination paused. Status: {paused_destination.status}")
        
    except NexlaAPIError as e:
        logger.error(f"Error controlling output: {e}")


def validate_config_example(client: NexlaClient, sink_id: int) -> None:
    """Example of validating a destination configuration"""
    logger.info(f"Validating configuration for destination with ID {sink_id}...")
    
    try:
        # Validate the current destination configuration
        validation_result = client.destinations.validate_config(sink_id)
        
        logger.info(f"Validation status: {validation_result.status}")
        if validation_result.output:
            for field in validation_result.output:
                if field.errors:
                    logger.warning(f"Field '{field.name}' has errors: {field.errors}")
                else:
                    logger.info(f"Field '{field.name}' is valid")
        
        # Optionally, validate a custom configuration
        custom_config = {
            "mapping": {
                "mode": "manual",
                "mapping": {
                    "id": ["id"],
                    "name": ["name"]
                }
            },
            "data_format": "json",
            "sink_type": "s3",
            "path": "example-bucket/custom-path"
        }
        
        custom_validation = client.destinations.validate_config(sink_id, custom_config)
        logger.info(f"Custom config validation status: {custom_validation.status}")
    
    except NexlaAPIError as e:
        logger.error(f"Error validating configuration: {e}")


def monitor_destination_metrics_example(client: NexlaClient, sink_id: int) -> None:
    """Example of monitoring a destination using metrics"""
    logger.info(f"Getting metrics for destination with ID {sink_id}...")
    
    try:
        # Get lifetime metrics
        lifetime_metrics = client.destinations.get_metrics(sink_id)
        logger.info(f"Lifetime metrics:")
        logger.info(f"  Records: {lifetime_metrics.metrics.get('records', 0)}")
        logger.info(f"  Size: {lifetime_metrics.metrics.get('size', 0)} bytes")
        
        # Get daily metrics for the last 7 days
        from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
        to_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        
        try:
            daily_metrics = client.destinations.get_daily_metrics(
                sink_id,
                from_date=from_date,
                to_date=to_date
            )
            
            logger.info(f"Daily metrics for the last 7 days:")
            for metric in daily_metrics.metrics:
                logger.info(f"  Date: {metric.time}, Records: {metric.record}, Size: {metric.size} bytes")
        except (NexlaAPIError, NexlaValidationError) as e:
            logger.warning(f"Could not retrieve daily metrics: {e}")
            
        # Get metrics aggregated by ingestion frequency
        try:
            run_metrics = client.destinations.get_run_summary_metrics(
                sink_id,
                from_date=from_date,
                to_date=to_date
            )
            
            logger.info(f"Metrics by ingestion frequency:")
            if run_metrics.metrics:
                for run_id, metrics in run_metrics.metrics.items():
                    logger.info(f"  Run ID: {run_id}")
                    logger.info(f"    Records: {metrics.get('records', 0)}")
                    logger.info(f"    Size: {metrics.get('size', 0)} bytes")
                    logger.info(f"    Errors: {metrics.get('errors', 0)}")
            else:
                logger.info("  No metrics available for this period")
        except (NexlaAPIError, NexlaValidationError) as e:
            logger.warning(f"Could not retrieve run summary metrics: {e}")
            
    except NexlaAPIError as e:
        logger.error(f"Error getting metrics: {e}")


def monitor_files_example(client: NexlaClient, sink_id: int) -> None:
    """Example of monitoring files written by a destination"""
    logger.info(f"Getting file statistics for destination with ID {sink_id}...")
    
    try:
        # Get statistics on file write status
        try:
            files_stats = client.destinations.get_files_stats_metrics(sink_id)
            
            logger.info("File status statistics:")
            if isinstance(files_stats.metrics, dict) and 'data' in files_stats.metrics:
                data = files_stats.metrics['data']
                if isinstance(data, dict):
                    for status, count_dict in data.items():
                        if isinstance(count_dict, dict):
                            for status_name, count in count_dict.items():
                                logger.info(f"  {status_name}: {count}")
                        else:
                            logger.info(f"  {status}: {count_dict}")
                elif isinstance(data, int):
                    logger.info(f"  Total files: {data}")
            else:
                logger.info("  No file statistics available")
        except (NexlaAPIError, NexlaValidationError) as e:
            logger.warning(f"Could not retrieve file status metrics: {e}")
        
        # Get file write history
        from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
        try:
            files_metrics = client.destinations.get_files_metrics(
                sink_id,
                from_date=from_date
            )
            
            logger.info("Recent file write history:")
            if hasattr(files_metrics.metrics, 'data') and files_metrics.metrics.data:
                for file_metric in files_metrics.metrics.data:
                    logger.info(f"  File: {file_metric.name}")
                    logger.info(f"    Status: {file_metric.writeStatus}")
                    logger.info(f"    Size: {file_metric.size} bytes")
                    logger.info(f"    Records: {file_metric.recordCount}")
                    if file_metric.lastWritten:
                        logger.info(f"    Last written: {file_metric.lastWritten}")
            else:
                logger.info("  No file write history available")
        except (NexlaAPIError, NexlaValidationError) as e:
            logger.warning(f"Could not retrieve file metrics: {e}")
                
        # Get raw file write status (no aggregation)
        try:
            logger.info("Raw file write events:")
            raw_files = client.destinations.get_files_raw_metrics(
                sink_id,
                from_date=from_date,
                status=FileStatus.COMPLETE
            )
            
            if raw_files.metrics:
                for file_event in raw_files.metrics:
                    logger.info(f"  File: {file_event.name}")
                    logger.info(f"    Status: {file_event.writeStatus}")
                    logger.info(f"    Size: {file_event.size} bytes")
                    logger.info(f"    Records: {file_event.recordCount}")
                    if file_event.lastWritten:
                        logger.info(f"    Write time: {file_event.lastWritten}")
            else:
                logger.info("  No raw file write events available")
        except (NexlaAPIError, NexlaValidationError) as e:
            logger.warning(f"Could not retrieve raw file metrics: {e}")
    
    except Exception as e:
        logger.error(f"Error monitoring files: {e}")


def copy_destination_example(client: NexlaClient, sink_id: int) -> Optional[int]:
    """Example of copying a destination"""
    logger.info(f"Copying destination with ID {sink_id}...")
    
    try:
        # Copy the destination with default settings
        copied_destination = client.destinations.copy(sink_id)
        
        logger.info(f"Destination copied successfully with ID: {copied_destination.id}")
        logger.info(f"New destination name: {copied_destination.name}")
        
        # Copy with custom options
        copied_with_options = client.destinations.copy(
            sink_id,
            {
                "reuse_data_credentials": True,
                "copy_access_controls": True
            }
        )
        
        logger.info(f"Destination copied with options, new ID: {copied_with_options.id}")
        
        return copied_destination.id
    
    except NexlaAPIError as e:
        logger.error(f"Error copying destination: {e}")
        return None


def delete_destination_example(client: NexlaClient, sink_id: int) -> bool:
    """Example of deleting a destination"""
    logger.info(f"Deleting destination with ID {sink_id}...")
    
    try:
        response = client.destinations.delete(sink_id)
        logger.info(f"Destination deleted successfully")
        return True
        
    except NexlaAPIError as e:
        logger.error(f"Error deleting destination: {e}")
        return False


def run_all_examples() -> None:
    """Run all example functions in sequence"""
    # Use a shared client instance
    client = nexla_client
    
    # List available destinations
    list_destinations_example(client)
    
    # Use the first destination found for examples or create a new one
    # This is for demonstration - you would typically use known IDs in real usage
    destinations = client.destinations.list()
    
    if destinations.items:
        existing_id = destinations.items[0].id
        logger.info(f"Using existing destination with ID {existing_id} for examples")
        
        # Run examples with the existing destination
        get_destination_example(client, existing_id)
        update_destination_example(client, existing_id)
        validate_config_example(client, existing_id)
        control_output_example(client, existing_id)
        monitor_destination_metrics_example(client, existing_id)
        monitor_files_example(client, existing_id)
        
        # Copy the destination
        copied_id = copy_destination_example(client, existing_id)
        if copied_id:
            # Clean up the copied destination
            delete_destination_example(client, copied_id)
    else:
        logger.warning("No existing destinations found. To run examples, you need at least one destination.")
        logger.info("To create a destination, you need a dataset ID and credentials ID.")
        logger.info("Use the following example with appropriate IDs:")
        logger.info("  create_destination_example(client, 'Example Destination', 12345, 67890)")


if __name__ == "__main__":
    run_all_examples() 