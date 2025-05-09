"""
Integration tests for the Transforms API

These tests verify that the Transforms API endpoints work correctly against a real Nexla instance.
"""

import logging
import pytest
import base64
import time
from typing import Optional, List

from nexla_sdk import NexlaClient
from nexla_sdk.models.transforms import (
    Transform, TransformList, AttributeTransform, 
    CreateTransformRequest, UpdateTransformRequest, DeleteTransformResponse,
    CreateAttributeTransformRequest, CodeType, OutputType, CodeEncoding
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the marker to skip tests if no integration credentials
from tests.conftest import skip_if_no_integration_creds


@pytest.fixture
def create_test_transform(nexla_client: NexlaClient) -> Transform:
    """
    Fixture to create a test transform for testing.
    Automatically cleans up after the test.
    """
    # Create a test transform to work with
    transform_data = CreateTransformRequest(
        name=f"SDK Test Transform {time.time()}",
        description="Test transform created for SDK integration tests",
        output_type=OutputType.RECORD,
        reusable=True,
        code_type=CodeType.JOLT_STANDARD,
        code_encoding=CodeEncoding.NONE,
        code=[
            {
                "operation": "shift",
                "spec": {
                    "test_input": "test_output"
                }
            }
        ],
        tags=["sdk-test", "integration-test"]
    )
    
    transform = nexla_client.transforms.create(transform_data)
    logger.info(f"Created test transform with ID: {transform.id}")
    
    yield transform
    
    # Clean up after the test
    try:
        nexla_client.transforms.delete(transform.id)
        logger.info(f"Deleted test transform with ID: {transform.id}")
    except Exception as e:
        logger.warning(f"Failed to delete test transform with ID {transform.id}: {e}")


@pytest.fixture
def create_test_attribute_transform(nexla_client: NexlaClient) -> AttributeTransform:
    """
    Fixture to create a test attribute transform for testing.
    Automatically cleans up after the test.
    """
    # Example Python code for an attribute transform (Base64 encoded)
    python_code = """
def transform(input_value):
    if isinstance(input_value, str):
        return input_value.upper()
    return input_value
"""
    encoded_code = base64.b64encode(python_code.encode()).decode()
    
    # Create a test attribute transform to work with
    transform_data = CreateAttributeTransformRequest(
        name=f"SDK Test Attribute Transform {time.time()}",
        description="Test attribute transform created for SDK integration tests",
        code_type=CodeType.PYTHON,
        code=encoded_code,
        tags=["sdk-test", "integration-test"]
    )
    
    attribute_transform = nexla_client.transforms.create_attribute_transform(transform_data)
    logger.info(f"Created test attribute transform with ID: {attribute_transform.id}")
    
    yield attribute_transform
    
    # Clean up after the test
    try:
        nexla_client.transforms.delete_attribute_transform(attribute_transform.id)
        logger.info(f"Deleted test attribute transform with ID: {attribute_transform.id}")
    except Exception as e:
        logger.warning(f"Failed to delete test attribute transform with ID {attribute_transform.id}: {e}")


@skip_if_no_integration_creds
class TestTransformsIntegration:
    """Integration tests for the Transforms API"""
    
    def test_list_transforms(self, nexla_client: NexlaClient):
        """Test listing transforms with different reusable options"""
        # Default should return a list of transforms
        transforms = nexla_client.transforms.list()
        assert isinstance(transforms, TransformList)
        
        # All transforms (both reusable and non-reusable)
        all_transforms = nexla_client.transforms.list(reusable="all")
        assert isinstance(all_transforms, TransformList)
        
        # Only reusable transforms
        reusable_transforms = nexla_client.transforms.list(reusable="1")
        assert isinstance(reusable_transforms, TransformList)
        
        # Only non-reusable transforms
        non_reusable_transforms = nexla_client.transforms.list(reusable="0")
        assert isinstance(non_reusable_transforms, TransformList)
        
        # Pagination
        page_1 = nexla_client.transforms.list(page=1, per_page=5)
        assert isinstance(page_1, TransformList)
        assert len(page_1.items) <= 5
    
    def test_list_public_transforms(self, nexla_client: NexlaClient):
        """Test listing public transforms"""
        public_transforms = nexla_client.transforms.list_public()
        assert isinstance(public_transforms, list)
        for transform in public_transforms:
            assert isinstance(transform, Transform)
    
    def test_create_get_update_delete_transform(self, nexla_client: NexlaClient):
        """Test the complete lifecycle of a transform"""
        # Create a new transform
        transform_data = CreateTransformRequest(
            name=f"SDK Test Transform {time.time()}",
            description="Test transform created for SDK integration tests",
            output_type=OutputType.RECORD,
            reusable=True,
            code_type=CodeType.JOLT_STANDARD,
            code_encoding=CodeEncoding.NONE,
            code=[
                {
                    "operation": "shift",
                    "spec": {
                        "test_input": "test_output"
                    }
                }
            ],
            tags=["sdk-test", "lifecycle-test"]
        )
        
        # Create
        new_transform = nexla_client.transforms.create(transform_data)
        assert isinstance(new_transform, Transform)
        assert new_transform.name == transform_data.name
        assert new_transform.description == transform_data.description
        assert new_transform.reusable == transform_data.reusable
        
        # Get
        retrieved_transform = nexla_client.transforms.get(new_transform.id)
        assert isinstance(retrieved_transform, Transform)
        assert retrieved_transform.id == new_transform.id
        assert retrieved_transform.name == new_transform.name
        
        # Update
        update_data = UpdateTransformRequest(
            name=f"{new_transform.name} (Updated)",
            description=f"{new_transform.description} - Updated",
            output_type=OutputType.RECORD,
            reusable=True,
            code_type=CodeType.JOLT_STANDARD,
            code_encoding=CodeEncoding.NONE,
            code=[
                {
                    "operation": "shift",
                    "spec": {
                        "test_input": "test_output_updated",
                        "new_field": "new_output"
                    }
                }
            ],
            tags=["sdk-test", "lifecycle-test", "updated"]
        )
        
        updated_transform = nexla_client.transforms.update(new_transform.id, update_data)
        assert isinstance(updated_transform, Transform)
        assert updated_transform.id == new_transform.id
        assert updated_transform.name == update_data.name
        assert updated_transform.description == update_data.description
        
        # Delete
        delete_response = nexla_client.transforms.delete(new_transform.id)
        assert isinstance(delete_response, DeleteTransformResponse)
        assert hasattr(delete_response, 'code')
        assert hasattr(delete_response, 'message')
    
    def test_copy_transform(self, nexla_client: NexlaClient, create_test_transform: Transform):
        """Test copying a transform"""
        # Use the fixture to get a test transform
        source_transform = create_test_transform
        
        # Copy the transform
        copied_transform = nexla_client.transforms.copy(source_transform.id)
        assert isinstance(copied_transform, Transform)
        assert copied_transform.id != source_transform.id
        assert "copy" in copied_transform.name.lower() or "copied" in copied_transform.name.lower()
        
        # Clean up the copied transform
        delete_response = nexla_client.transforms.delete(copied_transform.id)
        assert isinstance(delete_response, DeleteTransformResponse)
    
    def test_list_attribute_transforms(self, nexla_client: NexlaClient):
        """Test listing attribute transforms"""
        # Get attribute transforms
        attribute_transforms = nexla_client.transforms.list_attribute_transforms()
        assert isinstance(attribute_transforms, list)
        
        # Test pagination
        page_1 = nexla_client.transforms.list_attribute_transforms(page=1, per_page=5)
        assert isinstance(page_1, list)
        assert len(page_1) <= 5
    
    def test_list_public_attribute_transforms(self, nexla_client: NexlaClient):
        """Test listing public attribute transforms"""
        public_attribute_transforms = nexla_client.transforms.list_public_attribute_transforms()
        assert isinstance(public_attribute_transforms, list)
        for transform in public_attribute_transforms:
            assert isinstance(transform, AttributeTransform)
    
    def test_create_get_update_delete_attribute_transform(self, nexla_client: NexlaClient):
        """Test the complete lifecycle of an attribute transform"""
        # Example Python code for an attribute transform (Base64 encoded)
        python_code = """
def transform(input_value):
    if isinstance(input_value, str):
        return input_value.upper()
    return input_value
"""
        encoded_code = base64.b64encode(python_code.encode()).decode()
        
        # Create a test attribute transform
        transform_data = CreateAttributeTransformRequest(
            name=f"SDK Test Attribute Transform {time.time()}",
            description="Test attribute transform created for SDK integration tests",
            code_type=CodeType.PYTHON,
            code=encoded_code,
            tags=["sdk-test", "attribute-test"]
        )
        
        # Create
        new_attribute_transform = nexla_client.transforms.create_attribute_transform(transform_data)
        assert isinstance(new_attribute_transform, AttributeTransform)
        assert new_attribute_transform.name == transform_data.name
        assert new_attribute_transform.description == transform_data.description
        
        # Get
        retrieved_transform = nexla_client.transforms.get_attribute_transform(new_attribute_transform.id)
        assert isinstance(retrieved_transform, AttributeTransform)
        assert retrieved_transform.id == new_attribute_transform.id
        assert retrieved_transform.name == new_attribute_transform.name
        
        # Update
        # Updated Python code
        updated_python_code = """
def transform(input_value):
    if input_value is None:
        return None
    if isinstance(input_value, str):
        return input_value.upper()
    return str(input_value).upper()
"""
        updated_encoded_code = base64.b64encode(updated_python_code.encode()).decode()
        
        update_data = CreateAttributeTransformRequest(
            name=f"{new_attribute_transform.name} (Updated)",
            description=f"{new_attribute_transform.description} - Updated",
            code_type=CodeType.PYTHON,
            code=updated_encoded_code,
            tags=["sdk-test", "attribute-test", "updated"]
        )
        
        updated_transform = nexla_client.transforms.update_attribute_transform(
            new_attribute_transform.id, update_data
        )
        assert isinstance(updated_transform, AttributeTransform)
        assert updated_transform.id == new_attribute_transform.id
        assert updated_transform.name == update_data.name
        assert updated_transform.description == update_data.description
        
        # Delete
        delete_response = nexla_client.transforms.delete_attribute_transform(new_attribute_transform.id)
        assert isinstance(delete_response, DeleteTransformResponse)
        assert hasattr(delete_response, 'code')
        assert hasattr(delete_response, 'message')

    def test_get_attribute_transform(self, nexla_client: NexlaClient, create_test_attribute_transform: AttributeTransform):
        """Test getting an attribute transform by ID"""
        # Use the fixture to get a test attribute transform
        attribute_transform = create_test_attribute_transform
        
        # Get the transform
        retrieved_transform = nexla_client.transforms.get_attribute_transform(attribute_transform.id)
        assert isinstance(retrieved_transform, AttributeTransform)
        assert retrieved_transform.id == attribute_transform.id
        assert retrieved_transform.name == attribute_transform.name 