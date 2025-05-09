"""
Integration tests for the Schemas API
"""
import logging
import pytest
import uuid
from typing import Dict, Any

from nexla_sdk import NexlaClient
from nexla_sdk.models.schemas import DataSchema, SchemaList
from nexla_sdk.exceptions import NexlaAPIError

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


@pytest.fixture
def simple_schema() -> Dict[str, Any]:
    """Return a simple schema configuration for testing"""
    return {
        "name": "Test Schema",
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
                }
            },
            "type": "object"
        },
        "template": True  # Create as a template
    }


class TestSchemasIntegration:
    """Integration tests for the Schemas API"""
    
    def test_schema_lifecycle(self, nexla_client: NexlaClient, unique_test_id, simple_schema):
        """
        Test the complete lifecycle of a schema:
        - Create a schema
        - Get the schema
        - Update the schema
        - List schemas
        - Delete the schema
        """
        # Add unique ID to schema name for testing
        simple_schema["name"] = f"{simple_schema['name']} {unique_test_id}"
        
        # Track schema ID for cleanup
        schema_id = None
        
        try:
            # STEP 1: Create a new schema
            logger.info("Step 1: Creating a new schema")
            schema = nexla_client.schemas.create(simple_schema)
            logger.debug(f"Created schema: {schema}")
            
            assert isinstance(schema, DataSchema)
            assert schema.name == simple_schema["name"]
            assert schema.template == simple_schema["template"]
            schema_id = schema.id
            
            # STEP 2: Get the schema by ID
            logger.info(f"Step 2: Getting schema with ID: {schema_id}")
            retrieved_schema = nexla_client.schemas.get(schema_id)
            logger.debug(f"Retrieved schema: {retrieved_schema}")
            
            assert isinstance(retrieved_schema, DataSchema)
            assert retrieved_schema.id == schema_id
            assert retrieved_schema.name == simple_schema["name"]
            
            # STEP 3: Update the schema
            logger.info(f"Step 3: Updating schema with ID: {schema_id}")
            
            # For the update, we'll create a minimal update payload with only the fields we want to change
            update_data = {
                "name": f"{retrieved_schema.name} Updated",
                "description": "Updated test schema",  # Provide a non-null description
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
                        "updated_at": {
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
                        "updated_at": {
                            "description": "Last update timestamp"
                        }
                    },
                    "type": "object"
                },
                "template": retrieved_schema.template
            }
            
            updated_schema = nexla_client.schemas.update(schema_id, update_data)
            logger.debug(f"Updated schema: {updated_schema}")
            
            assert isinstance(updated_schema, DataSchema)
            assert updated_schema.id == schema_id
            assert updated_schema.name == f"{simple_schema['name']} Updated"
            
            # Verify the schema has the new property
            assert updated_schema.schema is not None
            assert updated_schema.schema.properties is not None
            assert "updated_at" in updated_schema.schema.properties
            assert updated_schema.schema.properties["updated_at"].type == "string"
            
            # STEP 4: List schemas and verify our schema is included
            logger.info("Step 4: Listing schemas and verifying our schema is included")
            schemas = nexla_client.schemas.list()
            logger.debug(f"Found {len(schemas.items)} schemas")
            
            # Find our schema in the list
            found = False
            for s in schemas.items:
                if s.id == schema_id:
                    found = True
                    break
                    
            assert found, f"Could not find schema with ID {schema_id} in the list"
            
            # STEP 5: List template schemas and verify our schema is included
            logger.info("Step 5: Listing template schemas")
            template_schemas = nexla_client.schemas.list(template=True)
            logger.debug(f"Found {len(template_schemas.items)} template schemas")
            
            # Find our schema in the list
            found = False
            for s in template_schemas.items:
                if s.id == schema_id:
                    found = True
                    break
                    
            assert found, f"Could not find schema with ID {schema_id} in the template schemas list"
            
            # NOTE: Copying a schema is not supported by the API
            # The API returns the error: "undefined method clone_from_data_schema"
            logger.warning("Skipping schema copying test as it's not supported by the API")
            
        finally:
            # Clean up the test schema if it was created
            if schema_id:
                try:
                    logger.info(f"Cleaning up test schema with ID: {schema_id}")
                    delete_result = nexla_client.schemas.delete(schema_id)
                    logger.debug(f"Delete result: {delete_result}")
                except Exception as e:
                    logger.warning(f"Failed to clean up test schema: {e}")
    
    def test_schema_from_dataset(self, nexla_client: NexlaClient, unique_test_id):
        """
        Test creating a schema from a dataset's schema
        
        Note: This test requires that at least one dataset already exists.
        If no datasets exist, the test will be skipped.
        """
        # First, list datasets to find one to use
        try:
            # Get the first page with a single item
            datasets = nexla_client.nexsets.list(page=1, per_page=1)
            if not datasets or len(datasets.items) == 0:
                pytest.skip("No datasets found to create schema from")
            
            dataset_id = datasets.items[0].id
            
            # STEP 1: Create schema from dataset
            logger.info(f"Creating schema from dataset with ID: {dataset_id}")
            schema = None
            
            try:
                schema = nexla_client.schemas.create_from_dataset(dataset_id, template=True)
                logger.debug(f"Created schema: {schema}")
                
                assert isinstance(schema, DataSchema)
                assert schema.template is True
                
                # Verify the schema was created with the dataset's schema
                retrieved_schema = nexla_client.schemas.get(schema.id)
                logger.debug(f"Retrieved schema: {retrieved_schema}")
                
                assert isinstance(retrieved_schema, DataSchema)
                assert retrieved_schema.id == schema.id
                
            finally:
                # Clean up the test schema if it was created
                if schema:
                    try:
                        logger.info(f"Cleaning up test schema with ID: {schema.id}")
                        delete_result = nexla_client.schemas.delete(schema.id)
                        logger.debug(f"Delete result: {delete_result}")
                    except Exception as e:
                        logger.warning(f"Failed to clean up test schema: {e}")
                
        except NexlaAPIError as e:
            if "404" in str(e) or "Not Found" in str(e):
                pytest.skip("Nexsets API not available")
            else:
                raise 