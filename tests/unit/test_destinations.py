"""Unit tests for destinations resource."""
import pytest
from unittest.mock import MagicMock

from nexla_sdk import NexlaClient
from nexla_sdk.models.destinations import DestinationCreate, DestinationUpdate, DestinationCopyOptions
from nexla_sdk.exceptions import ServerError
from nexla_sdk.http_client import HttpClientError
from tests.utils.fixtures import create_test_client
from tests.utils.mock_builders import MockDataFactory, MockResponseBuilder
from tests.utils.assertions import NexlaAssertions


class TestDestinationsResource:
    """Test destinations resource methods."""

    @pytest.fixture
    def mock_client(self) -> NexlaClient:
        """Create a test client with mocked HTTP."""
        return create_test_client()

    @pytest.fixture
    def assertions(self) -> NexlaAssertions:
        """Create assertions helper."""
        return NexlaAssertions()

    @pytest.fixture
    def mock_factory(self) -> MockDataFactory:
        """Create mock data factory."""
        return MockDataFactory()

    def test_list_destinations(self, mock_client, assertions):
        """Test listing destinations."""
        # Arrange
        mock_destinations = [
            MockResponseBuilder.destination({"id": 1, "name": "Dest 1"}),
            MockResponseBuilder.destination({"id": 2, "name": "Dest 2"})
        ]
        mock_client.http_client.request = MagicMock(return_value=mock_destinations)
        
        # Act
        destinations = mock_client.destinations.list()
        
        # Assert
        assert len(destinations) == 2
        for i, destination in enumerate(destinations):
            assertions.assert_destination_response(destination, mock_destinations[i])
        
        # Check the call was made (verify call happened)
        mock_client.http_client.request.assert_called_once()
        call_args = mock_client.http_client.request.call_args
        assert call_args[0][0] == 'GET'  # Method
        assert '/data_sinks' in call_args[0][1]  # URL contains path

    def test_list_destinations_with_parameters(self, mock_client, assertions):
        """Test listing destinations with query parameters."""
        # Arrange
        mock_destinations = [MockResponseBuilder.destination()]
        mock_client.http_client.request = MagicMock(return_value=mock_destinations)
        
        # Act
        destinations = mock_client.destinations.list(
            page=2, 
            per_page=50,
            access_role="owner"
        )
        
        # Assert
        assert len(destinations) == 1
        assertions.assert_destination_response(destinations[0], mock_destinations[0])
        
        # Check the call was made with parameters
        mock_client.http_client.request.assert_called_once()
        call_args = mock_client.http_client.request.call_args
        assert call_args[0][0] == 'GET'
        assert '/data_sinks' in call_args[0][1]
        assert 'params' in call_args[1]

    def test_get_destination(self, mock_client, assertions):
        """Test getting single destination."""
        # Arrange
        destination_id = 12345
        mock_response = MockResponseBuilder.destination({"id": destination_id, "name": "Test Destination"})
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = mock_client.destinations.get(destination_id)
        
        # Assert
        assertions.assert_destination_response(destination, {"id": destination_id, "name": "Test Destination"})
        
        # Check the call was made
        mock_client.http_client.request.assert_called_once()
        call_args = mock_client.http_client.request.call_args
        assert call_args[0][0] == 'GET'
        assert f'/data_sinks/{destination_id}' in call_args[0][1]

    def test_get_destination_with_expand(self, mock_client, assertions):
        """Test getting destination with expand parameter."""
        # Arrange
        destination_id = 12345
        mock_response = MockResponseBuilder.destination({
            "id": destination_id,
            "name": "Test Destination",
            "data_set": MockResponseBuilder.data_set_info()
        })
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = mock_client.destinations.get(destination_id, expand=True)
        
        # Assert
        assertions.assert_destination_response(destination, mock_response)
        assert hasattr(destination, 'data_set')
        
        # Check the call was made with expand parameter
        mock_client.http_client.request.assert_called_once()
        call_args = mock_client.http_client.request.call_args
        assert call_args[0][0] == 'GET'
        assert f'/data_sinks/{destination_id}' in call_args[0][1]
        assert 'params' in call_args[1]

    def test_create_destination(self, mock_client, assertions):
        """Test creating destination."""
        # Arrange
        create_data = DestinationCreate(
            name="Test Destination",
            sink_type="s3",
            data_credentials_id=100,
            data_set_id=200,
            description="Test description"
        )
        mock_response = MockResponseBuilder.destination({
            "id": 12345,
            "name": "Test Destination",
            "sink_type": "s3"
        })
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = mock_client.destinations.create(create_data)
        
        # Assert
        assertions.assert_destination_response(destination, {
            "id": 12345,
            "name": "Test Destination", 
            "sink_type": "s3"
        })
        
        # Verify the request
        mock_client.http_client.request.assert_called_once()
        call_args = mock_client.http_client.request.call_args
        assert call_args[0][0] == 'POST'
        assert '/data_sinks' in call_args[0][1]
        assert 'json' in call_args[1]

    def test_update_destination(self, mock_client, assertions):
        """Test updating destination."""
        # Arrange
        destination_id = 12345
        update_data = DestinationUpdate(
            name="Updated Destination",
            description="Updated description"
        )
        mock_response = MockResponseBuilder.destination({
            "id": destination_id,
            "name": "Updated Destination"
        })
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = mock_client.destinations.update(destination_id, update_data)
        
        # Assert
        assertions.assert_destination_response(destination, {
            "id": destination_id,
            "name": "Updated Destination"
        })
        
        # Verify the request
        mock_client.http_client.request.assert_called_once()
        call_args = mock_client.http_client.request.call_args
        assert call_args[0][0] == 'PUT'
        assert f'/data_sinks/{destination_id}' in call_args[0][1]

    def test_delete_destination(self, mock_client):
        """Test deleting destination."""
        # Arrange
        destination_id = 12345
        mock_client.http_client.request = MagicMock(return_value={"status": "deleted"})
        
        # Act
        result = mock_client.destinations.delete(destination_id)
        
        # Assert
        assert result == {"status": "deleted"}
        
        # Verify the request
        mock_client.http_client.request.assert_called_once()
        call_args = mock_client.http_client.request.call_args
        assert call_args[0][0] == 'DELETE'
        assert f'/data_sinks/{destination_id}' in call_args[0][1]

    def test_activate_destination(self, mock_client, assertions):
        """Test activating destination."""
        # Arrange
        destination_id = 12345
        mock_response = MockResponseBuilder.destination({
            "id": destination_id,
            "status": "ACTIVE"
        })
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = mock_client.destinations.activate(destination_id)
        
        # Assert
        assertions.assert_destination_response(destination, {
            "id": destination_id,
            "status": "ACTIVE"
        })
        
        # Verify the request
        mock_client.http_client.request.assert_called_once()
        call_args = mock_client.http_client.request.call_args
        assert call_args[0][0] == 'PUT'
        assert f'/data_sinks/{destination_id}/activate' in call_args[0][1]

    def test_pause_destination(self, mock_client, assertions):
        """Test pausing destination."""
        # Arrange
        destination_id = 12345
        mock_response = MockResponseBuilder.destination({
            "id": destination_id,
            "status": "PAUSED"
        })
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = mock_client.destinations.pause(destination_id)
        
        # Assert
        assertions.assert_destination_response(destination, {
            "id": destination_id,
            "status": "PAUSED"
        })
        
        # Verify the request
        mock_client.http_client.request.assert_called_once()
        call_args = mock_client.http_client.request.call_args
        assert call_args[0][0] == 'PUT'
        assert f'/data_sinks/{destination_id}/pause' in call_args[0][1]

    def test_copy_destination(self, mock_client, assertions):
        """Test copying destination."""
        # Arrange
        destination_id = 12345
        copy_options = DestinationCopyOptions(
            reuse_data_credentials=True,
            copy_access_controls=False
        )
        mock_response = MockResponseBuilder.destination({
            "id": 54321,
            "name": "Copied Destination"
        })
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = mock_client.destinations.copy(destination_id, copy_options)
        
        # Assert
        assertions.assert_destination_response(destination, {
            "id": 54321,
            "name": "Copied Destination"
        })
        
        # Verify the request
        mock_client.http_client.request.assert_called_once()
        call_args = mock_client.http_client.request.call_args
        assert call_args[0][0] == 'POST'
        assert f'/data_sinks/{destination_id}/copy' in call_args[0][1]

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
            mock_client.destinations.list()
        
        assert exc_info.value.status_code == 500
        assert "API error" in str(exc_info.value)

    def test_validation_error_handling(self, mock_client):
        """Test validation error handling."""
        # Arrange
        invalid_data = {"invalid": "data"}  # Missing required fields
        
        # Act & Assert  
        with pytest.raises(Exception):  # Will raise validation error during model creation
            DestinationCreate(**invalid_data)

    def test_empty_list_response(self, mock_client):
        """Test handling empty list response."""
        # Arrange
        mock_client.http_client.request = MagicMock(return_value=[])
        
        # Act
        destinations = mock_client.destinations.list()
        
        # Assert
        assert destinations == []
        assert len(destinations) == 0 