"""
Example usage of the Nexla Nexsets API (Data Sets)

This example demonstrates various operations on nexsets (data sets) using the Nexla SDK:
1. List nexsets
2. List nexsets for a source
3. Get a specific nexset
4. Create a new nexset
5. Update a nexset
6. Update with custom transform
7. Get nexset schema
8. Update nexset schema
9. Get sample data
10. Get sample data with metadata
11. Activate/pause nexsets
12. Copy a nexset
13. Delete a nexset
"""
import logging
import os
import sys
import uuid
from typing import Dict, Any, List

from nexla_sdk.models.access import AccessRole
from client import nexla_client

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def list_nexsets():
    """List all nexsets with pagination"""
    logger.info("Listing nexsets...")
    
    # Basic listing
    nexsets = nexla_client.nexsets.list()
    logger.info(f"Found {len(nexsets.items)} nexsets")
    
    # With pagination
    nexsets_page_1 = nexla_client.nexsets.list(page=1, per_page=10)
    logger.info(f"Page 1: Found {len(nexsets_page_1.items)} nexsets")
    
    # Filter by access role
    admin_nexsets = nexla_client.nexsets.list(access_role=AccessRole.ADMIN)
    logger.info(f"Admin nexsets: Found {len(admin_nexsets.items)} nexsets")
    
    return nexsets


def list_nexsets_for_source(data_source_id: str):
    """List nexsets for a specific data source"""
    logger.info(f"Listing nexsets for data source with ID: {data_source_id}")
    
    # This feature is not directly supported in the SDK,
    # but we can filter the results manually
    all_nexsets = nexla_client.nexsets.list(per_page=100)
    source_nexsets = [
        ns for ns in all_nexsets.items 
        if hasattr(ns, 'data_source_id') and str(ns.data_source_id) == str(data_source_id)
    ]
    
    logger.info(f"Found {len(source_nexsets)} nexsets for source {data_source_id}")
    return source_nexsets


def get_nexset(nexset_id: str):
    """Get a specific nexset by ID"""
    logger.info(f"Getting nexset with ID: {nexset_id}")
    
    # Get without expand
    nexset = nexla_client.nexsets.get(nexset_id)
    logger.info(f"Nexset name: {nexset.name if hasattr(nexset, 'name') else 'unnamed'}")
    
    # Get with expand=True to fetch more details
    nexset_expanded = nexla_client.nexsets.get(nexset_id, expand=True)
    logger.info(f"Expanded nexset: Has schema: {hasattr(nexset_expanded, 'schema_')}")
    
    return nexset


def create_nexset():
    """Create a new nexset"""
    logger.info("Creating a new nexset...")
    
    # First, find a parent nexset to use as a base
    try:
        # Get the first available nexset to use as a parent
        all_nexsets = nexla_client.nexsets.list(per_page=1)
        if not all_nexsets or not all_nexsets.items:
            logger.error("No nexsets found to use as parent")
            return None
        
        parent_id = all_nexsets.items[0].id
        logger.info(f"Using nexset {parent_id} as parent")
        
        # Create a unique name
        unique_id = uuid.uuid4().hex[:8]
        
        # Define nexset data
        nexset_data = {
            "name": f"Example Nexset {unique_id}",
            "description": "Created by the Nexla SDK example",
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
        new_nexset = nexla_client.nexsets.create(nexset_data)
        logger.info(f"Created nexset with ID: {new_nexset.id}")
        return new_nexset
    except Exception as e:
        logger.error(f"Failed to create nexset: {e}")
        return None


def update_nexset(nexset_id: str):
    """Update an existing nexset"""
    logger.info(f"Updating nexset with ID: {nexset_id}")
    
    # Update basic properties
    nexset_data = {
        "name": "Updated Nexset Name",
        "description": "Updated by the Nexla SDK example"
    }
    
    updated_nexset = nexla_client.nexsets.update(nexset_id, nexset_data)
    logger.info(f"Updated nexset: {updated_nexset.name if hasattr(updated_nexset, 'name') else 'unnamed'}")
    
    # Add tags
    tags_update = {
        "tags": ["example", "sdk", "test"]
    }
    tagged_nexset = nexla_client.nexsets.update(nexset_id, tags_update)
    logger.info(f"Added tags to nexset")
    
    # Remove tags
    remove_tags = {
        "tags": []
    }
    untagged_nexset = nexla_client.nexsets.update(nexset_id, remove_tags)
    logger.info(f"Removed tags from nexset")
    
    return updated_nexset


def update_with_custom_transform(nexset_id: str):
    """Update a nexset with a custom transform"""
    logger.info(f"Updating nexset with ID: {nexset_id} with custom transform")
    
    # Define a custom transform
    custom_transform = {
        "version": 1,
        "data_maps": [],
        "transforms": [
            {
                "operation": "shift",
                "spec": {
                    "id": "user_id",
                    "name": "user_name",
                    "value": "amount"
                }
            }
        ]
    }
    
    # Update the nexset with the custom transform
    nexset_data = {
        "has_custom_transform": True,
        "transform": custom_transform
    }
    
    try:
        updated_nexset = nexla_client.nexsets.update(nexset_id, nexset_data)
        logger.info(f"Updated nexset with custom transform")
        return updated_nexset
    except Exception as e:
        logger.error(f"Failed to update nexset with custom transform: {e}")
        return None


def get_schema(nexset_id: str):
    """Get the schema for a nexset"""
    logger.info(f"Getting schema for nexset with ID: {nexset_id}")
    
    schema = nexla_client.nexsets.get_schema(nexset_id)
    logger.info(f"Schema has {len(schema.attributes)} attributes")
    
    # Print attribute names
    attribute_names = [attr.name for attr in schema.attributes]
    logger.info(f"Attributes: {', '.join(attribute_names)}")
    
    return schema


def update_schema(nexset_id: str):
    """Update the schema for a nexset"""
    logger.info(f"Updating schema for nexset with ID: {nexset_id}")
    
    # First, get the current schema
    current_schema = nexla_client.nexsets.get_schema(nexset_id)
    
    # Convert to dict for modification
    schema_dict = current_schema.model_dump()
    
    # Add a new attribute
    schema_dict["attributes"].append({
        "name": "timestamp",
        "type": "timestamp",
        "nullable": True,
        "description": "Event timestamp"
    })
    
    # Update the schema
    try:
        updated_schema = nexla_client.nexsets.update_schema(nexset_id, schema_dict)
        logger.info(f"Updated schema has {len(updated_schema.attributes)} attributes")
        return updated_schema
    except Exception as e:
        logger.error(f"Failed to update schema: {e}")
        return None


def get_sample_data(nexset_id: str):
    """Get sample data for a nexset"""
    logger.info(f"Getting sample data for nexset with ID: {nexset_id}")
    
    # Get basic sample data
    samples = nexla_client.nexsets.get_sample_data(nexset_id, limit=5)
    
    if hasattr(samples, "records"):
        logger.info(f"Got {len(samples.records)} sample records")
        if samples.records:
            logger.info(f"First sample record: {samples.records[0]}")
    elif isinstance(samples, list):
        logger.info(f"Got {len(samples)} sample records")
        if samples:
            logger.info(f"First sample record: {samples[0]}")
    
    return samples


def get_sample_data_with_metadata(nexset_id: str):
    """Get sample data with Nexla metadata for a nexset"""
    logger.info(f"Getting sample data with metadata for nexset with ID: {nexset_id}")
    
    # Get sample data with metadata
    samples = nexla_client.nexsets.get_sample_data(
        nexset_id, 
        limit=5, 
        include_metadata=True
    )
    
    if isinstance(samples, list) and samples:
        logger.info(f"Got {len(samples)} sample records with metadata")
        if samples:
            sample = samples[0]
            if hasattr(sample, "rawMessage") and hasattr(sample, "nexlaMetaData"):
                logger.info(f"Sample raw message: {sample.rawMessage}")
                logger.info(f"Sample metadata resource type: {sample.nexlaMetaData.resourceType}")
    
    return samples


def get_characteristics(nexset_id: str):
    """Get characteristics for a nexset"""
    logger.info(f"Getting characteristics for nexset with ID: {nexset_id}")
    
    try:
        characteristics = nexla_client.nexsets.get_characteristics(nexset_id)
        logger.info(f"Nexset record count: {characteristics.record_count}")
        logger.info(f"Nexset file size: {characteristics.file_size} bytes")
        
        if characteristics.attributes:
            logger.info(f"Nexset has {len(characteristics.attributes)} attribute statistics")
        
        return characteristics
    except Exception as e:
        logger.error(f"Failed to get characteristics: {e}")
        return None


def activate_nexset(nexset_id: str):
    """Activate a nexset"""
    logger.info(f"Activating nexset with ID: {nexset_id}")
    
    try:
        activated_nexset = nexla_client.nexsets.activate(nexset_id)
        logger.info(f"Activated nexset: {activated_nexset.name if hasattr(activated_nexset, 'name') else 'unnamed'}")
        return activated_nexset
    except Exception as e:
        logger.error(f"Failed to activate nexset: {e}")
        return None


def pause_nexset(nexset_id: str):
    """Pause a nexset"""
    logger.info(f"Pausing nexset with ID: {nexset_id}")
    
    try:
        paused_nexset = nexla_client.nexsets.pause(nexset_id)
        logger.info(f"Paused nexset: {paused_nexset.name if hasattr(paused_nexset, 'name') else 'unnamed'}")
        return paused_nexset
    except Exception as e:
        logger.error(f"Failed to pause nexset: {e}")
        return None


def copy_nexset(nexset_id: str):
    """Create a copy of a nexset"""
    logger.info(f"Copying nexset with ID: {nexset_id}")
    
    try:
        copied_nexset = nexla_client.nexsets.copy(
            nexset_id,
            new_name=f"Copy of Nexset {nexset_id}",
            copy_access_controls=True
        )
        logger.info(f"Created copy with ID: {copied_nexset.id}")
        return copied_nexset
    except Exception as e:
        logger.error(f"Failed to copy nexset: {e}")
        return None


def delete_nexset(nexset_id: str):
    """Delete a nexset"""
    logger.info(f"Deleting nexset with ID: {nexset_id}")
    
    try:
        delete_response = nexla_client.nexsets.delete(nexset_id)
        logger.info(f"Delete response: {delete_response}")
        return delete_response
    except Exception as e:
        logger.error(f"Failed to delete nexset: {e}")
        return None


def run_examples():
    """Run all the examples"""
    print("Starting Nexsets API Examples...")
    
    # List nexsets
    print("1. Listing nexsets...")
    nexsets = list_nexsets()
    
    if nexsets and nexsets.items:
        nexset_id = nexsets.items[0].id
        print(f"Using nexset ID {nexset_id} for examples")
        
        # Get a specific nexset
        print("2. Getting nexset details...")
        nexset = get_nexset(nexset_id)
        
        # Try to get schema
        print("3. Getting schema (may not be available for all nexsets)...")
        try:
            schema = get_schema(nexset_id)
        except Exception as e:
            print(f"Schema not available: {e}")
        
        # Try to get sample data
        print("4. Getting sample data (may not be available for all nexsets)...")
        try:
            samples = get_sample_data(nexset_id)
        except Exception as e:
            print(f"Sample data not available: {e}")
        
        # Try to get characteristics
        print("5. Getting characteristics (may not be available for all nexsets)...")
        try:
            characteristics = get_characteristics(nexset_id)
        except Exception as e:
            print(f"Characteristics not available: {e}")
        
        # Create a new nexset
        print("6. Creating a new nexset...")
        new_nexset = create_nexset()
        
        if new_nexset:
            new_nexset_id = new_nexset.id
            print(f"Created new nexset with ID: {new_nexset_id}")
            
            # Update nexset
            print("7. Updating nexset...")
            update_nexset(new_nexset_id)
            
            # Update with custom transform
            print("8. Updating with custom transform...")
            try:
                update_with_custom_transform(new_nexset_id)
            except Exception as e:
                print(f"Custom transform not supported: {e}")
            
            # Try to update schema
            print("9. Updating schema (may not be supported)...")
            try:
                update_schema(new_nexset_id)
            except Exception as e:
                print(f"Schema update not supported: {e}")
            
            # Try to activate nexset
            print("10. Activating nexset (may not be supported)...")
            try:
                activate_nexset(new_nexset_id)
            except Exception as e:
                print(f"Activate not supported: {e}")
            
            # Try to pause nexset
            print("11. Pausing nexset (may not be supported)...")
            try:
                pause_nexset(new_nexset_id)
            except Exception as e:
                print(f"Pause not supported: {e}")
            
            # Try to copy nexset
            print("12. Copying nexset...")
            try:
                copied_nexset = copy_nexset(new_nexset_id)
                
                # Clean up - delete copied nexset
                if copied_nexset:
                    print(f"13. Deleting copied nexset with ID: {copied_nexset.id}...")
                    delete_nexset(copied_nexset.id)
            except Exception as e:
                print(f"Copy not supported: {e}")
            
            # Clean up - delete new nexset
            print(f"14. Deleting new nexset with ID: {new_nexset_id}...")
            delete_nexset(new_nexset_id)
    else:
        print("No nexsets found. Cannot run examples.")
    
    print("Nexsets API Examples completed.")


if __name__ == "__main__":
    run_examples() 