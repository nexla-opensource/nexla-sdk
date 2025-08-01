"""Unit tests for nexsets resource."""
import pytest
from unittest.mock import MagicMock
from typing import List, Dict, Any

from nexla_sdk import NexlaClient
from nexla_sdk.models.nexsets import Nexset, NexsetSample, NexsetCreate, NexsetUpdate, NexsetCopyOptions
from nexla_sdk.exceptions import ServerError, AuthenticationError, ValidationError
from nexla_sdk.http_client import HttpClientError
from tests.utils.fixtures import create_test_client
from tests.utils.mock_builders import MockDataFactory, MockResponseBuilder
from tests.utils.assertions import NexlaAssertions


class TestNexsetsResource:
    """Test nexsets resource methods."""

    @pytest.fixture
    def mock_client(self) -> NexlaClient:
        """Create a test client with mocked HTTP."""
        return create_test_client()

    @pytest.fixture
    def mock_factory(self) -> MockDataFactory:
        """Create a mock data factory."""
        return MockDataFactory()

    @pytest.fixture
    def assertions(self):
        """Create assertions helper."""
        return NexlaAssertions()

    def test_list_nexsets(self, mock_client, mock_factory, assertions):
        """Test listing nexsets."""
        # Arrange
        mock_nexset1 = mock_factory.create_mock_nexset(id=1001, name="Dataset 1")
        mock_nexset2 = mock_factory.create_mock_nexset(id=1002, name="Dataset 2")
        mock_response = [mock_nexset1, mock_nexset2]
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        nexsets = mock_client.nexsets.list()
        
        # Assert
        assert len(nexsets) == 2
        for i, nexset in enumerate(nexsets):
            expected_data = mock_response[i]
            assertions.assert_nexset_response(nexset, expected_data)
        
        # Verify API call
        mock_client.http_client.request.assert_called_once_with(
            'GET', 
            f'{mock_client.api_url}/data_sets',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params={}
        )

    def test_list_nexsets_with_parameters(self, mock_client, mock_factory):
        """Test listing nexsets with query parameters."""
        # Arrange
        mock_response = [mock_factory.create_mock_nexset()]
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        mock_client.nexsets.list(page=2, per_page=50, access_role="collaborator")
        
        # Assert
        expected_params = {
            'page': 2,
            'per_page': 50,
            'access_role': 'collaborator'
        }
        mock_client.http_client.request.assert_called_once_with(
            'GET', 
            f'{mock_client.api_url}/data_sets',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params=expected_params
        )

    def test_get_nexset(self, mock_client, mock_factory, assertions):
        """Test getting single nexset."""
        # Arrange
        nexset_id = 1001
        mock_response = mock_factory.create_mock_nexset(id=nexset_id, name="Test Dataset")
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        nexset = mock_client.nexsets.get(nexset_id)
        
        # Assert
        assertions.assert_nexset_response(nexset, {"id": nexset_id, "name": "Test Dataset"})
        mock_client.http_client.request.assert_called_once_with(
            'GET', 
            f'{mock_client.api_url}/data_sets/1001',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params={}
        )

    def test_get_nexset_with_expand(self, mock_client, mock_factory):
        """Test getting nexset with expand parameter."""
        # Arrange
        nexset_id = 1001
        mock_response = mock_factory.create_mock_nexset(id=nexset_id)
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        mock_client.nexsets.get(nexset_id, expand=True)
        
        # Assert
        mock_client.http_client.request.assert_called_once_with(
            'GET', 
            f'{mock_client.api_url}/data_sets/1001',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params={'expand': 1}
        )

    def test_create_nexset(self, mock_client, mock_factory, assertions):
        """Test creating nexset."""
        # Arrange
        create_data = NexsetCreate(
            name="New Dataset",
            parent_data_set_id=2001,
            has_custom_transform=True,
            description="Test dataset creation"
        )
        mock_response = mock_factory.create_mock_nexset(id=1001, name="New Dataset")
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        nexset = mock_client.nexsets.create(create_data)
        
        # Assert
        assertions.assert_nexset_response(nexset, {"id": 1001, "name": "New Dataset"})
        mock_client.http_client.request.assert_called_once_with(
            'POST', 
            f'{mock_client.api_url}/data_sets',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            json=create_data.to_dict()
        )

    def test_update_nexset(self, mock_client, mock_factory, assertions):
        """Test updating nexset."""
        # Arrange
        nexset_id = 1001
        update_data = NexsetUpdate(
            name="Updated Dataset",
            description="Updated description"
        )
        mock_response = mock_factory.create_mock_nexset(id=nexset_id, name="Updated Dataset")
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        nexset = mock_client.nexsets.update(nexset_id, update_data)
        
        # Assert
        assertions.assert_nexset_response(nexset, {"id": nexset_id, "name": "Updated Dataset"})
        mock_client.http_client.request.assert_called_once_with(
            'PUT', 
            f'{mock_client.api_url}/data_sets/1001',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            json=update_data.to_dict()
        )

    def test_delete_nexset(self, mock_client):
        """Test deleting nexset."""
        # Arrange
        nexset_id = 1001
        mock_response = {"message": "Dataset deleted successfully"}
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        result = mock_client.nexsets.delete(nexset_id)
        
        # Assert
        assert result["message"] == "Dataset deleted successfully"
        mock_client.http_client.request.assert_called_once_with(
            'DELETE', 
            f'{mock_client.api_url}/data_sets/1001',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            }
        )

    def test_activate_nexset(self, mock_client, mock_factory, assertions):
        """Test activating nexset."""
        # Arrange
        nexset_id = 1001
        mock_response = mock_factory.create_mock_nexset(id=nexset_id, status="ACTIVE")
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        nexset = mock_client.nexsets.activate(nexset_id)
        
        # Assert
        assertions.assert_nexset_response(nexset, {"id": nexset_id, "status": "ACTIVE"})
        mock_client.http_client.request.assert_called_once_with(
            'PUT', 
            f'{mock_client.api_url}/data_sets/1001/activate',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            }
        )

    def test_pause_nexset(self, mock_client, mock_factory, assertions):
        """Test pausing nexset."""
        # Arrange
        nexset_id = 1001
        mock_response = mock_factory.create_mock_nexset(id=nexset_id, status="PAUSED")
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        nexset = mock_client.nexsets.pause(nexset_id)
        
        # Assert
        assertions.assert_nexset_response(nexset, {"id": nexset_id, "status": "PAUSED"})
        mock_client.http_client.request.assert_called_once_with(
            'PUT', 
            f'{mock_client.api_url}/data_sets/1001/pause',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            }
        )

    def test_get_samples(self, mock_client, mock_factory, assertions):
        """Test getting nexset samples."""
        # Arrange
        nexset_id = 1001
        mock_sample1 = mock_factory.create_mock_nexset_sample()
        mock_sample2 = mock_factory.create_mock_nexset_sample()
        mock_response = [mock_sample1, mock_sample2]
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        samples = mock_client.nexsets.get_samples(nexset_id, count=5, include_metadata=True)
        
        # Assert
        assert len(samples) == 2
        for sample in samples:
            assertions.assert_nexset_sample(sample)
        
        expected_params = {
            'count': 5,
            'include_metadata': True,
            'live': False
        }
        mock_client.http_client.request.assert_called_once_with(
            'GET', 
            f'{mock_client.api_url}/data_sets/1001/samples',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params=expected_params
        )

    def test_get_samples_with_live_option(self, mock_client, mock_factory):
        """Test getting live samples."""
        # Arrange
        nexset_id = 1001
        mock_response = [mock_factory.create_mock_nexset_sample()]
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        mock_client.nexsets.get_samples(nexset_id, live=True)
        
        # Assert
        expected_params = {
            'count': 10,
            'include_metadata': False,
            'live': True
        }
        mock_client.http_client.request.assert_called_once_with(
            'GET', 
            f'{mock_client.api_url}/data_sets/1001/samples',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params=expected_params
        )

    def test_copy_nexset(self, mock_client, mock_factory, assertions):
        """Test copying nexset."""
        # Arrange
        nexset_id = 1001
        copy_options = NexsetCopyOptions(
            copy_access_controls=True,
            owner_id=123
        )
        mock_response = mock_factory.create_mock_nexset(id=1002, copied_from_id=nexset_id)
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        copied_nexset = mock_client.nexsets.copy(nexset_id, copy_options)
        
        # Assert
        assertions.assert_nexset_response(copied_nexset, {"id": 1002, "copied_from_id": nexset_id})
        mock_client.http_client.request.assert_called_once_with(
            'POST', 
            f'{mock_client.api_url}/data_sets/1001/copy',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            json=copy_options.to_dict()
        )

    def test_copy_nexset_without_options(self, mock_client, mock_factory):
        """Test copying nexset without options."""
        # Arrange
        nexset_id = 1001
        mock_response = mock_factory.create_mock_nexset(id=1002)
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        mock_client.nexsets.copy(nexset_id)
        
        # Assert
        mock_client.http_client.request.assert_called_once_with(
            'POST', 
            f'{mock_client.api_url}/data_sets/1001/copy',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            json={}
        )

    def test_http_error_handling(self, mock_client):
        """Test HTTP error handling."""
        # Arrange
        mock_client.http_client.request = MagicMock(
            side_effect=HttpClientError(
                "Server Error",
                status_code=500,
                response={"message": "Internal server error"}
            )
        )
        
        # Act & Assert
        with pytest.raises(ServerError) as exc_info:
            mock_client.nexsets.list()
        
        assert exc_info.value.status_code == 500
        assert "API error" in str(exc_info.value)

    def test_validation_error_handling(self, mock_client):
        """Test validation error handling."""
        # Arrange
        invalid_response = {
            # Missing required 'id' field
            "name": "Invalid Dataset"
        }
        mock_client.http_client.request = MagicMock(return_value=invalid_response)
        
        # Act & Assert
        from pydantic import ValidationError
        with pytest.raises(ValidationError) as exc_info:
            mock_client.nexsets.get(1001)
        
        # Check that the error mentions the missing fields
        error_str = str(exc_info.value)
        assert "id" in error_str

    def test_empty_list_response(self, mock_client):
        """Test handling empty list response."""
        # Arrange
        mock_client.http_client.request = MagicMock(return_value=[])
        
        # Act
        nexsets = mock_client.nexsets.list()
        
        # Assert
        assert nexsets == []
        assert len(nexsets) == 0 