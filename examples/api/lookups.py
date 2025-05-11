"""
Example usage of the Nexla Lookups API (Data Maps)

This example demonstrates various operations on data maps:
1. Listing data maps
2. Getting a specific data map
3. Creating a new static data map
4. Updating a data map
5. Managing data map entries
6. Getting sample entries 
7. Downloading data map entries
8. Creating a copy of a data map
9. Cleaning up (deleting a data map)
"""
import os
import json
import logging
from typing import Dict, Any, Optional, List

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError, NexlaNotFoundError
from nexla_sdk.models.lookups import Lookup, DataType, SampleEntriesResponse
from client import nexla_client


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def list_lookups_example(client: NexlaClient) -> None:
    """Example of listing data maps"""
    logger.info("Listing data maps...")
    
    # List all data maps with default pagination (page 1, 100 items per page)
    lookups = client.lookups.list()
    
    # Print count and basic info about each data map
    logger.info(f"Found {len(lookups.items)} data maps:")
    for lookup in lookups.items:
        logger.info(f"  ID: {lookup.id}, Name: {lookup.name}, Type: {lookup.data_type or 'N/A'}")
    
    # List data maps with validation to get entry counts
    logger.info("Listing data maps with validation...")
    lookups_validated = client.lookups.list(validate=True)
    for lookup in lookups_validated.items:
        entry_count = lookup.map_entry_count or 0
        logger.info(f"  ID: {lookup.id}, Name: {lookup.name}, Entries: {entry_count}")


def get_lookup_example(client: NexlaClient, lookup_id: str) -> None:
    """Example of retrieving a specific data map"""
    logger.info(f"Getting data map with ID {lookup_id}...")
    
    try:
        # Get basic data map info
        lookup = client.lookups.get(lookup_id)
        logger.info(f"Data map details:")
        logger.info(f"  Name: {lookup.name}")
        logger.info(f"  Type: {lookup.data_type}")
        logger.info(f"  Primary key: {lookup.map_primary_key}")
        if lookup.owner:
            logger.info(f"  Owner: {lookup.owner.full_name}")
        if lookup.org:
            logger.info(f"  Organization: {lookup.org.name}")
        
        # Get data map with validation
        logger.info(f"Getting data map with validation...")
        lookup_validated = client.lookups.get(lookup_id, validate=True)
        if hasattr(lookup_validated, 'map_entry_info') and lookup_validated.map_entry_info:
            logger.info(f"  Entry info: {json.dumps(lookup_validated.map_entry_info, indent=2)}")
        
        # Get data map with expanded details
        logger.info(f"Getting data map with expanded details...")
        lookup_expanded = client.lookups.get(lookup_id, expand=True)
        logger.info(f"  Expanded data map retrieved successfully")
        
    except NexlaAPIError as e:
        logger.error(f"Error retrieving data map: {e}")


def create_lookup_example(client: NexlaClient, lookup_name: str) -> Optional[str]:
    """Example of creating a new static data map"""
    logger.info(f"Creating a new data map named '{lookup_name}'...")
    
    try:
        # Create a simple key-value data map
        lookup = client.lookups.create({
            "name": lookup_name,
            "data_type": DataType.STRING.value,
            "emit_data_default": True,
            "map_primary_key": "eventId",
            "description": "Created via SDK example",
            "data_defaults": {
                "eventId": "Unknown",
                "description": "Unknown",
                "category": "Unknown"
            },
            "data_map": [
                {
                    "eventId": "0",
                    "description": "Search",
                    "category": "Web"
                },
                {
                    "eventId": "1",
                    "description": "Checkout",
                    "category": "App"
                },
                {
                    "eventId": "2",
                    "description": "Return",
                    "category": "App"
                }
            ]
        })
        
        logger.info(f"Data map created successfully with ID: {lookup.id}")
        return lookup.id
        
    except NexlaAPIError as e:
        logger.error(f"Error creating data map: {e}")
        return None


def update_lookup_example(client: NexlaClient, lookup_id: str) -> None:
    """Example of updating a data map"""
    logger.info(f"Updating data map with ID {lookup_id}...")
    
    try:
        # Update data map name and description
        updated_lookup = client.lookups.update(
            lookup_id=lookup_id,
            lookup_data={
                "name": f"Updated data map",
                "description": "Updated via SDK example"
            }
        )
        
        logger.info(f"Data map updated successfully:")
        logger.info(f"  New name: {updated_lookup.name}")
        logger.info(f"  New description: {updated_lookup.description}")
        
    except NexlaAPIError as e:
        logger.error(f"Error updating data map: {e}")


def manage_entries_example(client: NexlaClient, lookup_id: str) -> None:
    """Example of managing entries in a data map"""
    logger.info(f"Managing entries for data map with ID {lookup_id}...")
    
    try:
        # Add/update specific entries
        logger.info("Adding/updating entries...")
        new_entries = [
            {
                "eventId": "3",
                "description": "Login",
                "category": "Auth"
            },
            {
                "eventId": "4",
                "description": "Logout",
                "category": "Auth"
            }
        ]
        
        result = client.lookups.upsert_entries(lookup_id, new_entries)
        logger.info(f"Updated entries: {json.dumps(result, indent=2)}")
        
        # Check entries by key
        logger.info("Checking specific entries...")
        entries = client.lookups.check_entries(lookup_id, ["1", "2"])
        logger.info(f"Found entries: {json.dumps(entries, indent=2)}")
        
        # Check entries with wildcard
        logger.info("Checking entries with wildcard...")
        entries_wildcard = client.lookups.check_entries(lookup_id, "*")
        logger.info(f"Found {len(entries_wildcard)} entries with wildcard")
        
        # Delete specific entries
        logger.info("Deleting entries...")
        delete_result = client.lookups.delete_entries(lookup_id, ["4"])
        logger.info(f"Delete result: {json.dumps(delete_result, indent=2)}")
        
    except NexlaAPIError as e:
        logger.error(f"Error managing entries: {e}")


def get_sample_entries_example(client: NexlaClient, lookup_id: str) -> None:
    """Example of getting sample entries from a data map"""
    logger.info(f"Getting sample entries from data map with ID {lookup_id}...")
    
    try:
        # Get sample entries with default field name (all fields)
        logger.info("Getting sample entries (all fields)...")
        samples = client.lookups.get_sample_entries(lookup_id)
        
        # Display sample entries
        if samples.output:
            if isinstance(samples.output, list):
                logger.info(f"Found {len(samples.output)} sample entries")
                if len(samples.output) > 0:
                    logger.info(f"First sample: {json.dumps(samples.output[0], indent=2)}")
            else:
                logger.info(f"Sample output: {json.dumps(samples.output, indent=2)}")
        
        # Get sample entries for a specific field
        logger.info("Getting sample entries for a specific field...")
        field_samples = client.lookups.get_sample_entries(lookup_id, field_name="eventId")
        
        if field_samples.output:
            # Use model_dump for Pydantic v2 compatibility
            try:
                sample_data = field_samples.model_dump(exclude_none=True)
            except AttributeError:
                # Fallback for older Pydantic versions
                sample_data = field_samples.dict(exclude_none=True)
            logger.info(f"Field samples response: {json.dumps(sample_data, indent=2)}")
        
    except NexlaAPIError as e:
        logger.warning(f"Sample entries not available: {e}")


def download_entries_example(client: NexlaClient, lookup_id: str) -> None:
    """Example of downloading all entries from a data map"""
    logger.info(f"Downloading entries from data map with ID {lookup_id}...")
    
    try:
        # Download all entries as CSV
        csv_data = client.lookups.download_entries(lookup_id)
        
        # Display first few lines
        lines = csv_data.strip().split('\n')
        preview = '\n'.join(lines[:min(5, len(lines))])
        logger.info(f"CSV preview:\n{preview}")
        
        # You could also save the CSV to a file
        # with open(f"data_map_{lookup_id}.csv", "w") as f:
        #     f.write(csv_data)
        
    except NexlaAPIError as e:
        logger.error(f"Error downloading entries: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error downloading entries: {e}")


def copy_lookup_example(client: NexlaClient, lookup_id: str) -> Optional[str]:
    """Example of copying a data map"""
    logger.info(f"Creating a copy of data map with ID {lookup_id}...")
    
    try:
        # Copy the data map with a new name
        copied_lookup = client.lookups.copy(lookup_id, new_name="Copied data map")
        
        logger.info(f"Data map copied successfully:")
        logger.info(f"  New ID: {copied_lookup.id}")
        logger.info(f"  New name: {copied_lookup.name}")
        
        return copied_lookup.id
        
    except NexlaAPIError as e:
        logger.error(f"Error copying data map: {e}")
        return None


def delete_lookup_example(client: NexlaClient, lookup_id: str) -> bool:
    """Example of deleting a data map"""
    logger.info(f"Deleting data map with ID {lookup_id}...")
    
    try:
        # Delete the data map
        result = client.lookups.delete(lookup_id)
        
        if result is not None:
            logger.info(f"Data map deletion response: {result.message}")
        else:
            logger.info(f"Data map deleted successfully")
        return True
        
    except NexlaNotFoundError:
        logger.warning(f"Data map with ID {lookup_id} not found")
        return True
    except NexlaAPIError as e:
        logger.error(f"Error deleting data map: {e}")
        return False


def run_all_examples() -> None:
    """Run all lookup examples in sequence"""
    client = nexla_client()
    
    # List existing data maps
    list_lookups_example(client)
    
    # Create a new data map
    lookup_id = create_lookup_example(client, f"Example Data Map")
    if not lookup_id:
        logger.error("Failed to create data map, stopping examples")
        return
    
    # Get and display the data map
    get_lookup_example(client, lookup_id)
    
    # Update the data map
    update_lookup_example(client, lookup_id)
    
    # Manage entries in the data map
    manage_entries_example(client, lookup_id)
    
    # Get sample entries
    get_sample_entries_example(client, lookup_id)
    
    # Download entries
    download_entries_example(client, lookup_id)
    
    # Create a copy of the data map
    copied_id = copy_lookup_example(client, lookup_id)
    
    # Clean up: delete the data maps
    if lookup_id:
        delete_lookup_example(client, lookup_id)
    if copied_id:
        delete_lookup_example(client, copied_id)


if __name__ == "__main__":
    run_all_examples() 