"""
Example usage of the Nexla Transforms API

This example demonstrates various operations on transforms using the Nexla SDK:
1. List all transforms (with reusable filter options)
2. List public transforms
3. Get a transform by ID
4. Create a transform
5. Update a transform
6. Copy a transform
7. Delete a transform
8. List attribute transforms
9. List public attribute transforms
10. Get an attribute transform
11. Create an attribute transform
12. Update an attribute transform
13. Delete an attribute transform
"""

import json
import logging
import sys
from typing import Dict, Any, List, Optional

# Add the parent directory to the path so we can import from examples
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from client import nexla_client
from nexla_sdk.models.transforms import (
    Transform, TransformList, AttributeTransform, 
    CreateTransformRequest, UpdateTransformRequest, 
    CreateAttributeTransformRequest, CodeType, OutputType, CodeEncoding
)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def list_transforms():
    """List all transforms with different reusable filter options"""
    logger.info("Listing transforms (default)...")
    
    # Default behavior (only reusable transforms)
    transforms = nexla_client.transforms.list()
    logger.info(f"Found {len(transforms.items)} reusable transforms")
    
    # All transforms (both reusable and non-reusable)
    all_transforms = nexla_client.transforms.list(reusable="all")
    logger.info(f"Found {len(all_transforms.items)} total transforms (reusable and non-reusable)")
    
    # Only non-reusable transforms
    non_reusable_transforms = nexla_client.transforms.list(reusable="0")
    logger.info(f"Found {len(non_reusable_transforms.items)} non-reusable transforms")
    
    # Only reusable transforms (explicit)
    reusable_transforms = nexla_client.transforms.list(reusable="1")
    logger.info(f"Found {len(reusable_transforms.items)} reusable transforms")
    
    # Pagination example
    transforms_page_1 = nexla_client.transforms.list(page=1, per_page=10)
    logger.info(f"Page 1: Found {len(transforms_page_1.items)} transforms")
    
    return transforms


def list_public_transforms():
    """List all public transforms"""
    logger.info("Listing public transforms...")
    
    public_transforms = nexla_client.transforms.list_public()
    logger.info(f"Found {len(public_transforms)} public transforms")
    
    return public_transforms


def get_transform(transform_id: int):
    """Get a transform by ID"""
    logger.info(f"Getting transform with ID: {transform_id}")
    
    transform = nexla_client.transforms.get(transform_id)
    logger.info(f"Retrieved transform: {transform.name}")
    
    return transform


def create_transform():
    """Create a new transform"""
    logger.info("Creating a new transform...")
    
    # Example of a simple Jolt standard transform
    transform_data = CreateTransformRequest(
        name="Sample Transform",
        description="A sample transform created via SDK",
        output_type=OutputType.RECORD,
        reusable=True,
        code_type=CodeType.JOLT_STANDARD,
        code_encoding=CodeEncoding.NONE,
        code=[
            {
                "operation": "shift",
                "spec": {
                    "source_field1": "target_field1",
                    "source_field2": "target_field2",
                    "nested": {
                        "field": "flattened_field"
                    }
                }
            }
        ],
        tags=["sample", "sdk-created"]
    )
    
    new_transform = nexla_client.transforms.create(transform_data)
    logger.info(f"Created transform with ID: {new_transform.id}")
    
    return new_transform


def update_transform(transform_id: int):
    """Update an existing transform"""
    logger.info(f"Updating transform with ID: {transform_id}")
    
    # First get the current transform
    current_transform = nexla_client.transforms.get(transform_id)
    
    # Prepare update data
    transform_data = UpdateTransformRequest(
        name=f"{current_transform.name} (Updated)",
        description=f"{current_transform.description or ''} - Updated via SDK",
        output_type=current_transform.output_type,
        reusable=current_transform.reusable,
        code_type=current_transform.code_type,
        code_encoding=current_transform.code_encoding,
        code=current_transform.code,
        tags=current_transform.tags + ["updated"] if current_transform.tags else ["updated"]
    )
    
    updated_transform = nexla_client.transforms.update(transform_id, transform_data)
    logger.info(f"Updated transform: {updated_transform.name}")
    
    return updated_transform


def copy_transform(transform_id: int):
    """Copy a transform"""
    logger.info(f"Copying transform with ID: {transform_id}")
    
    copied_transform = nexla_client.transforms.copy(transform_id)
    logger.info(f"Created copy with ID: {copied_transform.id}")
    
    return copied_transform


def delete_transform(transform_id: int):
    """Delete a transform"""
    logger.info(f"Deleting transform with ID: {transform_id}")
    
    delete_response = nexla_client.transforms.delete(transform_id)
    logger.info(f"Delete response: {delete_response.code} - {delete_response.message}")
    
    return delete_response


def list_attribute_transforms():
    """List all attribute transforms"""
    logger.info("Listing attribute transforms...")
    
    attribute_transforms = nexla_client.transforms.list_attribute_transforms()
    logger.info(f"Found {len(attribute_transforms)} attribute transforms")
    
    # Pagination example
    attribute_transforms_page_1 = nexla_client.transforms.list_attribute_transforms(page=1, per_page=10)
    logger.info(f"Page 1: Found {len(attribute_transforms_page_1)} attribute transforms")
    
    return attribute_transforms


def list_public_attribute_transforms():
    """List all public attribute transforms"""
    logger.info("Listing public attribute transforms...")
    
    public_attribute_transforms = nexla_client.transforms.list_public_attribute_transforms()
    logger.info(f"Found {len(public_attribute_transforms)} public attribute transforms")
    
    return public_attribute_transforms


def get_attribute_transform(transform_id: int):
    """Get an attribute transform by ID"""
    logger.info(f"Getting attribute transform with ID: {transform_id}")
    
    attribute_transform = nexla_client.transforms.get_attribute_transform(transform_id)
    logger.info(f"Retrieved attribute transform: {attribute_transform.name}")
    
    return attribute_transform


def create_attribute_transform():
    """Create a new attribute transform"""
    logger.info("Creating a new attribute transform...")
    
    # Example Python code for an attribute transform (Base64 encoded)
    # This is a simple function that returns the input capitalized
    python_code = """
def transform(input_value):
    if isinstance(input_value, str):
        return input_value.upper()
    return input_value
"""
    import base64
    encoded_code = base64.b64encode(python_code.encode()).decode()
    
    # Create the attribute transform
    transform_data = CreateAttributeTransformRequest(
        name="Capitalize String Transform",
        description="Converts input string to uppercase",
        code_type=CodeType.PYTHON,
        code=encoded_code,
        tags=["string", "uppercase", "sample"]
    )
    
    new_attribute_transform = nexla_client.transforms.create_attribute_transform(transform_data)
    logger.info(f"Created attribute transform with ID: {new_attribute_transform.id}")
    
    return new_attribute_transform


def update_attribute_transform(transform_id: int):
    """Update an existing attribute transform"""
    logger.info(f"Updating attribute transform with ID: {transform_id}")
    
    # First get the current attribute transform
    current_transform = nexla_client.transforms.get_attribute_transform(transform_id)
    
    # Python code for updated attribute transform (Base64 encoded)
    # This is a modified function that handles None values
    python_code = """
def transform(input_value):
    if input_value is None:
        return None
    if isinstance(input_value, str):
        return input_value.upper()
    return str(input_value).upper()
"""
    import base64
    encoded_code = base64.b64encode(python_code.encode()).decode()
    
    # Prepare update data
    transform_data = CreateAttributeTransformRequest(
        name=f"{current_transform.name} (Updated)",
        description=f"{current_transform.description or ''} - Updated via SDK",
        code_type=CodeType.PYTHON,
        code=encoded_code,
        tags=current_transform.tags + ["updated"] if current_transform.tags else ["updated"]
    )
    
    updated_transform = nexla_client.transforms.update_attribute_transform(transform_id, transform_data)
    logger.info(f"Updated attribute transform: {updated_transform.name}")
    
    return updated_transform


def delete_attribute_transform(transform_id: int):
    """Delete an attribute transform"""
    logger.info(f"Deleting attribute transform with ID: {transform_id}")
    
    delete_response = nexla_client.transforms.delete_attribute_transform(transform_id)
    logger.info(f"Delete response: {delete_response.code} - {delete_response.message}")
    
    return delete_response


if __name__ == "__main__":
    try:
        print("Starting Transforms API Examples...")
        
        # List transforms
        print("1. Listing transforms...")
        transforms = list_transforms()
        
        # If transforms are available, use one for examples
        transform_id = None
        attribute_transform_id = None
        
        if transforms and transforms.items:
            transform_id = transforms.items[0].id
            print(f"Using transform ID {transform_id} for examples")
            
            # Get transform details
            print("2. Getting transform details...")
            transform = get_transform(transform_id)
            
            # Copy a transform
            print("3. Copying transform...")
            copied_transform = copy_transform(transform_id)
            
            # Update the copied transform
            print("4. Updating copied transform...")
            updated_transform = update_transform(copied_transform.id)
            
            # Delete the copied transform
            print("5. Deleting copied transform...")
            delete_transform(copied_transform.id)
        
        # Create a new transform
        print("6. Creating a new transform...")
        new_transform = create_transform()
        
        # Delete the new transform
        print("7. Deleting the new transform...")
        delete_transform(new_transform.id)
        
        # List attribute transforms
        print("8. Listing attribute transforms...")
        attribute_transforms = list_attribute_transforms()
        
        # List public attribute transforms
        print("9. Listing public attribute transforms...")
        public_attribute_transforms = list_public_attribute_transforms()
        
        if attribute_transforms and len(attribute_transforms) > 0:
            attribute_transform_id = attribute_transforms[0].id
            print(f"Using attribute transform ID {attribute_transform_id} for examples")
            
            # Get attribute transform details
            print("10. Getting attribute transform details...")
            attribute_transform = get_attribute_transform(attribute_transform_id)
        
        # Create a new attribute transform
        print("11. Creating a new attribute transform...")
        new_attribute_transform = create_attribute_transform()
        
        # Update the new attribute transform
        print("12. Updating the new attribute transform...")
        updated_attribute_transform = update_attribute_transform(new_attribute_transform.id)
        
        # Delete the new attribute transform
        print("13. Deleting the new attribute transform...")
        delete_attribute_transform(new_attribute_transform.id)
        
        print("Transforms API Examples completed.")
        
    except Exception as e:
        logger.error(f"Error during example: {e}")
        raise 