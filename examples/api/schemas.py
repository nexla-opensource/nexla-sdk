"""
Nexla Schema Templates API Examples

This module demonstrates how to use the Nexla SDK to interact with Schema Templates.
"""
import logging
import os
import json
from typing import Dict, Any, List, Optional

from client import nexla_client
from nexla_sdk.models.schemas import DataSchema, SchemaProperty

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_all_schemas():
    """List all schemas owned by the authenticated user"""
    logger.info("Listing all schemas")
    
    schemas = nexla_client.schemas.list()
    logger.info(f"Found {len(schemas)} schemas")
    
    # Print basic info for each schema
    for schema in schemas:
        template_status = "Template" if schema.template else "Regular"
        logger.info(f"- Schema {schema.id}: {schema.name} ({template_status})")
        
    return schemas


def list_template_schemas():
    """List only schemas that are templates"""
    logger.info("Listing template schemas")
    
    schemas = nexla_client.schemas.list(template=True)
    logger.info(f"Found {len(schemas)} template schemas")
    
    # Print basic info for each schema
    for schema in schemas:
        logger.info(f"- Template Schema {schema.id}: {schema.name}")
        
    return schemas


def list_non_template_schemas():
    """List only schemas that are not templates"""
    logger.info("Listing non-template schemas")
    
    schemas = nexla_client.schemas.list(template=False)
    logger.info(f"Found {len(schemas)} non-template schemas")
    
    # Print basic info for each schema
    for schema in schemas:
        logger.info(f"- Non-Template Schema {schema.id}: {schema.name}")
        
    return schemas


def get_schema_by_id(schema_id: str):
    """Get details for a specific schema"""
    logger.info(f"Getting schema with ID: {schema_id}")
    
    schema = nexla_client.schemas.get(schema_id)
    logger.info(f"Retrieved schema: {schema.name}")
    
    # Print schema details
    if schema.schema and schema.schema.properties:
        logger.info("Schema properties:")
        for prop_name, prop_details in schema.schema.properties.items():
            logger.info(f"  - {prop_name}: {prop_details.type}")
    
    return schema


def get_schema_with_datasets(schema_id: str):
    """Get schema details including associated datasets"""
    logger.info(f"Getting schema with ID {schema_id} and associated datasets")
    
    schema = nexla_client.schemas.get(schema_id, expand=True)
    logger.info(f"Retrieved schema: {schema.name}")
    
    # Check for associated datasets
    if schema.data_sets:
        logger.info(f"Schema is associated with {len(schema.data_sets)} datasets:")
        for dataset_id in schema.data_sets:
            logger.info(f"  - Dataset ID: {dataset_id}")
    else:
        logger.info("Schema is not associated with any datasets")
    
    return schema


def create_schema_from_specification():
    """Create a new schema by providing a specification"""
    logger.info("Creating a new schema from specification")
    
    # Define schema specification
    schema_data = {
        "name": "Sample Schema from SDK",
        "schema": {
            "properties": {
                "id": {
                    "type": "number"
                },
                "name": {
                    "type": "string"
                },
                "email": {
                    "type": "string"
                },
                "active": {
                    "type": "boolean"
                },
                "created_at": {
                    "type": "string"
                }
            },
            "type": "object",
            "$schema": "http://json-schema.org/draft-04/schema#"
        },
        "annotations": {
            "properties": {
                "id": {
                    "description": "Unique identifier"
                },
                "name": {
                    "description": "User's full name"
                },
                "email": {
                    "description": "User's email address"
                },
                "active": {
                    "description": "Whether the user is active"
                },
                "created_at": {
                    "description": "Creation timestamp"
                }
            },
            "type": "object"
        },
        "template": True  # Create as a template
    }
    
    schema = nexla_client.schemas.create(schema_data)
    logger.info(f"Created schema with ID: {schema.id}")
    
    return schema


def create_schema_from_existing(source_schema_id: str):
    """Create a new schema by copying an existing schema"""
    logger.info(f"Creating a new schema by copying schema ID: {source_schema_id}")
    
    schema = nexla_client.schemas.create_from_schema(source_schema_id)
    logger.info(f"Created schema with ID: {schema.id}")
    
    return schema


def create_schema_from_dataset(dataset_id: str):
    """Create a new schema from a dataset's schema"""
    logger.info(f"Creating a new schema from dataset ID: {dataset_id}")
    
    schema = nexla_client.schemas.create_from_dataset(dataset_id)
    logger.info(f"Created schema with ID: {schema.id}")
    
    return schema


def update_schema(schema_id: str):
    """Update an existing schema"""
    logger.info(f"Updating schema with ID: {schema_id}")
    
    # First, get the current schema
    schema = nexla_client.schemas.get(schema_id)
    
    # Make changes to the schema
    schema_data = schema.model_dump(by_alias=True)
    
    # Add or update schema name if it exists
    if "name" in schema_data:
        schema_data["name"] = f"{schema_data.get('name', 'Schema')} (Updated)"
    
    # Add a new property to the schema
    if schema_data.get("schema", {}).get("properties"):
        schema_data["schema"]["properties"]["updated_at"] = {
            "type": "string"
        }
        
        # Add annotation for the new property if annotations exist
        if schema_data.get("annotations", {}).get("properties"):
            schema_data["annotations"]["properties"]["updated_at"] = {
                "description": "Last update timestamp"
            }
    
    updated_schema = nexla_client.schemas.update(schema_id, schema_data)
    logger.info(f"Updated schema: {updated_schema.name}")
    
    return updated_schema


def delete_schema(schema_id: str):
    """Delete a schema"""
    logger.info(f"Deleting schema with ID: {schema_id}")
    
    result = nexla_client.schemas.delete(schema_id)
    logger.info(f"Schema deleted successfully")
    
    return result


def schema_lifecycle_example():
    """Demonstrate the complete lifecycle of a schema"""
    logger.info("Starting schema lifecycle example")
    
    # Create a new schema
    schema = create_schema_from_specification()
    schema_id = schema.id
    
    # Get the schema details
    schema = get_schema_by_id(schema_id)
    
    # Update the schema
    updated_schema = update_schema(schema_id)
    
    # List schemas to confirm our schema is included
    schemas = list_all_schemas()
    
    # Delete the schema
    delete_schema(schema_id)
    
    logger.info("Schema lifecycle example completed")


# Execute examples if run directly
if __name__ == "__main__":
    # Execute all examples in sequence
    try:
        # List schemas in different ways
        schemas = list_all_schemas()
        
        if schemas:
            # Work with an existing schema
            first_schema_id = str(schemas[0].id)
            get_schema_by_id(first_schema_id)
            get_schema_with_datasets(first_schema_id)
            
            # Try to create a schema from an existing schema
            schema = create_schema_from_existing(first_schema_id)
            
            # Delete the schema we just created
            if schema:
                delete_schema(str(schema.id))
        
        # Run complete lifecycle example
        schema_lifecycle_example()
        
    except Exception as e:
        logger.error(f"Error in examples: {e}", exc_info=True)
