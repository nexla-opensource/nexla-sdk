"""
Example usage of the Nexla Sources API

This example demonstrates various operations on data sources:
1. Listing sources
2. Getting a specific source
3. Creating a new source
4. Updating a source
5. Monitoring a source (metrics)
6. Controlling source ingestion (activate/pause)
7. Inspecting source data
8. Cleaning up (deleting a source)
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError
from nexla_sdk.models.sources import SourceType, FileStatus
from client import nexla_client


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def list_sources_example(client: NexlaClient) -> None:
    """Example of listing data sources"""
    logger.info("Listing data sources...")
    
    # List all sources with default pagination (page 1, 100 items per page)
    sources = client.sources.list()
    
    # Print count and basic info about each source
    logger.info(f"Found {len(sources.items)} sources:")
    for source in sources.items:
        logger.info(f"  ID: {source.id}, Name: {source.name}, Type: {source.source_type}, Status: {source.status}")


def get_source_example(client: NexlaClient, source_id: int) -> None:
    """Example of retrieving a specific data source"""
    logger.info(f"Getting source with ID {source_id}...")
    
    try:
        # Get basic source info
        source = client.sources.get(source_id)
        logger.info(f"Source details:")
        logger.info(f"  Name: {source.name}")
        logger.info(f"  Type: {source.source_type}")
        logger.info(f"  Status: {source.status}")
        logger.info(f"  Ingest method: {source.ingest_method}")
        logger.info(f"  Owner: {source.owner.full_name}")
        logger.info(f"  Organization: {source.org.name}")
        logger.info(f"  Associated datasets: {len(source.data_sets)}")
        
        # Get expanded source info
        expanded_source = client.sources.get(source_id, expand=True)
        logger.info(f"Expanded source details:")
        logger.info(f"  Source config: {json.dumps(expanded_source.source_config, indent=2)}")
        
    except NexlaAPIError as e:
        logger.error(f"Error retrieving source: {e}")


def create_source_example(client: NexlaClient, source_name: str) -> Optional[int]:
    """Example of creating a new data source"""
    logger.info(f"Creating a new source named '{source_name}'...")
    
    try:
        # Create a simple file_upload source
        source = client.sources.create(
            name=source_name,
            source_type=SourceType.FILE_UPLOAD.value,
            source_config={
                "file_type": "csv",
                "file_name_pattern": "*.csv",
                "delimiter": ",",
                "has_header": True
            },
            description="Created via SDK example"
        )
        
        logger.info(f"Source created successfully with ID: {source.id}")
        return source.id
        
    except NexlaAPIError as e:
        logger.error(f"Error creating source: {e}")
        return None


def update_source_example(client: NexlaClient, source_id: int) -> None:
    """Example of updating a data source"""
    logger.info(f"Updating source with ID {source_id}...")
    
    try:
        # Update source name and description
        updated_source = client.sources.update(
            source_id=source_id,
            name=f"Updated source {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            description="Updated via SDK example"
        )
        
        logger.info(f"Source updated successfully:")
        logger.info(f"  New name: {updated_source.name}")
        logger.info(f"  New description: {updated_source.description}")
        
    except NexlaAPIError as e:
        logger.error(f"Error updating source: {e}")


def control_ingestion_example(client: NexlaClient, source_id: int) -> None:
    """Example of controlling source ingestion (activate/pause)"""
    logger.info(f"Controlling ingestion for source with ID {source_id}...")
    
    try:
        # Activate the source
        logger.info("Activating source...")
        activated_source = client.sources.activate(source_id)
        logger.info(f"Source activated. Status: {activated_source.status}")
        
        # Pause the source
        logger.info("Pausing source...")
        paused_source = client.sources.pause(source_id)
        logger.info(f"Source paused. Status: {paused_source.status}")
        
    except NexlaAPIError as e:
        logger.error(f"Error controlling ingestion: {e}")


def validate_config_example(client: NexlaClient, source_id: int) -> None:
    """Example of validating a source configuration"""
    logger.info(f"Validating configuration for source with ID {source_id}...")
    
    try:
        # Validate the current source configuration
        validation_result = client.sources.validate_config(source_id)
        
        logger.info(f"Validation status: {validation_result.status}")
        if validation_result.output:
            for field in validation_result.output:
                if field.errors:
                    logger.warning(f"Field '{field.name}' has errors: {field.errors}")
                else:
                    logger.info(f"Field '{field.name}' is valid")
    
    except NexlaAPIError as e:
        logger.error(f"Error validating configuration: {e}")


def inspect_source_example(client: NexlaClient, source_id: int) -> None:
    """Example of inspecting source data"""
    logger.info(f"Inspecting data for source with ID {source_id}...")
    
    try:
        # For S3 sources, you can inspect the hierarchy
        # Note: This example assumes an S3 source. For other source types,
        # you would use different parameters.
        source = client.sources.get(source_id)
        
        if source.source_type == "s3":
            logger.info("Probing S3 source tree structure...")
            tree_result = client.sources.probe_tree(
                source_id=source_id,
                depth=2,
                bucket="my-bucket",
                prefix="data/",
                region="us-west-2"
            )
            
            logger.info(f"Tree probe status: {tree_result.status}")
            logger.info(f"Connection type: {tree_result.connection_type}")
            logger.info(f"Directory structure: {json.dumps(tree_result.output, indent=2)}")
            
            # For a specific file, you can get a sample
            logger.info("Probing a specific file for sample data...")
            file_sample = client.sources.probe_files(
                source_id=source_id,
                path="data/sample.csv"
            )
            
            logger.info(f"File sample status: {file_sample.status}")
            logger.info(f"File format: {file_sample.output.format}")
            logger.info(f"Sample records: {json.dumps(file_sample.output.messages[:3], indent=2)}")
        
    except NexlaAPIError as e:
        logger.error(f"Error inspecting source: {e}")


def monitor_source_example(client: NexlaClient, source_id: int) -> None:
    """Example of monitoring a source using metrics"""
    logger.info(f"Getting metrics for source with ID {source_id}...")
    
    try:
        # Get lifetime metrics
        lifetime_metrics = client.sources.get_metrics(source_id)
        logger.info(f"Lifetime metrics:")
        logger.info(f"  Records: {lifetime_metrics.metrics.get('records', 0)}")
        logger.info(f"  Size: {lifetime_metrics.metrics.get('size', 0)} bytes")
        
        # Get daily metrics for the past 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        logger.info(f"Daily metrics from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}:")
        daily_metrics = client.sources.get_daily_metrics(
            source_id=source_id,
            from_date=start_date,
            to_date=end_date
        )
        
        for metric in daily_metrics.metrics:
            logger.info(f"  Date: {metric.time}, Records: {metric.record}, Size: {metric.size}")
        
        # Get file stats
        file_stats = client.sources.get_files_stats(source_id)
        logger.info("File status statistics:")
        for status, count in file_stats.metrics.get("data", {}).items():
            logger.info(f"  {status}: {count}")
        
        # Get per-file metrics
        file_metrics = client.sources.get_files_metrics(source_id)
        logger.info("File metrics:")
        for file_metric in file_metrics.metrics.data[:5]:  # Show first 5 files
            logger.info(f"  File: {file_metric.name}")
            logger.info(f"    Status: {file_metric.ingestionStatus}")
            logger.info(f"    Records: {file_metric.recordCount}")
            logger.info(f"    Size: {file_metric.size} bytes")
            logger.info(f"    Last ingested: {file_metric.lastIngested}")
        
    except NexlaAPIError as e:
        logger.error(f"Error getting metrics: {e}")


def copy_source_example(client: NexlaClient, source_id: int) -> Optional[int]:
    """Example of copying a data source"""
    logger.info(f"Copying source with ID {source_id}...")
    
    try:
        # Copy the source, reusing credentials
        copied_source = client.sources.copy(
            source_id=source_id,
            reuse_data_credentials=True,
            copy_access_controls=True
        )
        
        logger.info(f"Source copied successfully with ID: {copied_source.id}")
        logger.info(f"  Name: {copied_source.name}")
        logger.info(f"  Type: {copied_source.source_type}")
        
        return copied_source.id
        
    except NexlaAPIError as e:
        logger.error(f"Error copying source: {e}")
        return None


def delete_source_example(client: NexlaClient, source_id: int) -> bool:
    """Example of deleting a data source"""
    logger.info(f"Deleting source with ID {source_id}...")
    
    try:
        # Delete the source
        delete_response = client.sources.delete(source_id)
        logger.info(f"Delete response: {delete_response.code} - {delete_response.message}")
        return True
        
    except NexlaAPIError as e:
        logger.error(f"Error deleting source: {e}")
        return False


def run_all_examples() -> None:
    """Run all sources API examples"""
    client = nexla_client
    
    # List all sources
    list_sources_example(client)
    
    # Find an example source ID from the list response or create a new one
    source_id = None
    
    # Create a new source for our examples
    source_id = create_source_example(client, f"SDK Example Source {datetime.now().strftime('%Y%m%d%H%M%S')}")
    if not source_id:
        logger.error("Failed to create a source. Examples cannot continue.")
        return
    
    # Get source details
    get_source_example(client, source_id)
    
    # Update the source
    update_source_example(client, source_id)
    
    # Control ingestion
    control_ingestion_example(client, source_id)
    
    # Validate source configuration
    validate_config_example(client, source_id)
    
    # Monitor the source with metrics
    monitor_source_example(client, source_id)
    
    # Copy the source
    copied_source_id = copy_source_example(client, source_id)
    
    # Clean up by deleting the sources
    if copied_source_id:
        delete_source_example(client, copied_source_id)
    delete_source_example(client, source_id)


if __name__ == "__main__":
    run_all_examples() 