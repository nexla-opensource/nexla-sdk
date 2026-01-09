"""Unit tests for nexsets resource."""
import pytest
from pydantic import ValidationError

from nexla_sdk.models.nexsets.responses import Nexset, NexsetSample
from nexla_sdk.models.nexsets.requests import NexsetCreate, NexsetUpdate, NexsetCopyOptions
from nexla_sdk.exceptions import ServerError, NotFoundError
from nexla_sdk.http_client import HttpClientError
from tests.utils.mock_builders import MockDataFactory
from tests.utils.assertions import NexlaAssertions, assert_model_list_valid


@pytest.mark.unit
class TestNexsetsResource:
    """Test nexsets resource methods."""

    def test_list_nexsets(self, mock_client):
        """Test listing nexsets."""
        # Arrange
        mock_factory = MockDataFactory()
        mock_nexset1 = mock_factory.create_mock_nexset(id=1001, name="Dataset 1")
        mock_nexset2 = mock_factory.create_mock_nexset(id=1002, name="Dataset 2")
        mock_response = [mock_nexset1, mock_nexset2]
        mock_client.http_client.add_response("/data_sets", mock_response)

        # Act
        nexsets = mock_client.nexsets.list()

        # Assert
        assert len(nexsets) == 2
        assert all(isinstance(nexset, Nexset) for nexset in nexsets)
        mock_client.http_client.assert_request_made("GET", "/data_sets")

    def test_list_nexsets_with_parameters(self, mock_client):
        """Test listing nexsets with query parameters."""
        # Arrange
        mock_factory = MockDataFactory()
        mock_response = [mock_factory.create_mock_nexset()]
        mock_client.http_client.add_response("/data_sets", mock_response)

        # Act
        mock_client.nexsets.list(page=2, per_page=50, access_role="collaborator")

        # Assert
        mock_client.http_client.assert_request_made("GET", "/data_sets")
        request = mock_client.http_client.get_last_request()
        assert request["params"].get("page") == 2
        assert request["params"].get("per_page") == 50
        assert request["params"].get("access_role") == "collaborator"

    def test_get_nexset(self, mock_client):
        """Test getting single nexset."""
        # Arrange
        nexset_id = 1001
        mock_factory = MockDataFactory()
        mock_response = mock_factory.create_mock_nexset(id=nexset_id, name="Test Dataset")
        mock_client.http_client.add_response(f"/data_sets/{nexset_id}", mock_response)

        # Act
        nexset = mock_client.nexsets.get(nexset_id)

        # Assert
        assert isinstance(nexset, Nexset)
        assert nexset.id == nexset_id
        assert nexset.name == "Test Dataset"
        mock_client.http_client.assert_request_made("GET", f"/data_sets/{nexset_id}")

    def test_get_nexset_with_expand(self, mock_client):
        """Test getting nexset with expand parameter."""
        # Arrange
        nexset_id = 1001
        mock_factory = MockDataFactory()
        mock_response = mock_factory.create_mock_nexset(id=nexset_id)
        mock_client.http_client.add_response(f"/data_sets/{nexset_id}", mock_response)

        # Act
        mock_client.nexsets.get(nexset_id, expand=True)

        # Assert
        mock_client.http_client.assert_request_made("GET", f"/data_sets/{nexset_id}")
        request = mock_client.http_client.get_last_request()
        assert request["params"].get("expand") == 1

    def test_create_nexset(self, mock_client):
        """Test creating nexset."""
        # Arrange
        create_data = NexsetCreate(
            name="New Dataset",
            parent_data_set_id=2001,
            has_custom_transform=True,
            description="Test dataset creation"
        )
        mock_factory = MockDataFactory()
        mock_response = mock_factory.create_mock_nexset(id=1001, name="New Dataset")
        mock_client.http_client.add_response("/data_sets", mock_response)

        # Act
        nexset = mock_client.nexsets.create(create_data)

        # Assert
        assert isinstance(nexset, Nexset)
        assert nexset.id == 1001
        assert nexset.name == "New Dataset"
        mock_client.http_client.assert_request_made("POST", "/data_sets")

        # Verify request body
        request = mock_client.http_client.get_last_request()
        assert request["json"]["name"] == "New Dataset"

    def test_update_nexset(self, mock_client):
        """Test updating nexset."""
        # Arrange
        nexset_id = 1001
        update_data = NexsetUpdate(
            name="Updated Dataset",
            description="Updated description"
        )
        mock_factory = MockDataFactory()
        mock_response = mock_factory.create_mock_nexset(id=nexset_id, name="Updated Dataset")
        mock_client.http_client.add_response(f"/data_sets/{nexset_id}", mock_response)

        # Act
        nexset = mock_client.nexsets.update(nexset_id, update_data)

        # Assert
        assert isinstance(nexset, Nexset)
        assert nexset.name == "Updated Dataset"
        mock_client.http_client.assert_request_made("PUT", f"/data_sets/{nexset_id}")

    def test_delete_nexset(self, mock_client):
        """Test deleting nexset."""
        # Arrange
        nexset_id = 1001
        mock_response = {"message": "Dataset deleted successfully"}
        mock_client.http_client.add_response(f"/data_sets/{nexset_id}", mock_response)

        # Act
        result = mock_client.nexsets.delete(nexset_id)

        # Assert
        assert result["message"] == "Dataset deleted successfully"
        mock_client.http_client.assert_request_made("DELETE", f"/data_sets/{nexset_id}")

    def test_activate_nexset(self, mock_client):
        """Test activating nexset."""
        # Arrange
        nexset_id = 1001
        mock_factory = MockDataFactory()
        mock_response = mock_factory.create_mock_nexset(id=nexset_id, status="ACTIVE")
        mock_client.http_client.add_response(f"/data_sets/{nexset_id}/activate", mock_response)

        # Act
        nexset = mock_client.nexsets.activate(nexset_id)

        # Assert
        assert isinstance(nexset, Nexset)
        assert nexset.status == "ACTIVE"
        mock_client.http_client.assert_request_made("PUT", f"/data_sets/{nexset_id}/activate")

    def test_pause_nexset(self, mock_client):
        """Test pausing nexset."""
        # Arrange
        nexset_id = 1001
        mock_factory = MockDataFactory()
        mock_response = mock_factory.create_mock_nexset(id=nexset_id, status="PAUSED")
        mock_client.http_client.add_response(f"/data_sets/{nexset_id}/pause", mock_response)

        # Act
        nexset = mock_client.nexsets.pause(nexset_id)

        # Assert
        assert isinstance(nexset, Nexset)
        assert nexset.status == "PAUSED"
        mock_client.http_client.assert_request_made("PUT", f"/data_sets/{nexset_id}/pause")

    def test_get_samples(self, mock_client):
        """Test getting nexset samples."""
        # Arrange
        nexset_id = 1001
        mock_factory = MockDataFactory()
        mock_sample1 = mock_factory.create_mock_nexset_sample()
        mock_sample2 = mock_factory.create_mock_nexset_sample()
        mock_response = [mock_sample1, mock_sample2]
        mock_client.http_client.add_response(f"/data_sets/{nexset_id}/samples", mock_response)

        # Act
        samples = mock_client.nexsets.get_samples(nexset_id, count=5, include_metadata=True)

        # Assert
        assert len(samples) == 2
        mock_client.http_client.assert_request_made("GET", f"/data_sets/{nexset_id}/samples")

        # Verify parameters
        request = mock_client.http_client.get_last_request()
        assert request["params"].get("count") == 5
        assert request["params"].get("include_metadata") == True

    def test_get_samples_with_live_option(self, mock_client):
        """Test getting live samples."""
        # Arrange
        nexset_id = 1001
        mock_factory = MockDataFactory()
        mock_response = [mock_factory.create_mock_nexset_sample()]
        mock_client.http_client.add_response(f"/data_sets/{nexset_id}/samples", mock_response)

        # Act
        mock_client.nexsets.get_samples(nexset_id, live=True)

        # Assert
        mock_client.http_client.assert_request_made("GET", f"/data_sets/{nexset_id}/samples")
        request = mock_client.http_client.get_last_request()
        assert request["params"].get("live") == True

    def test_copy_nexset(self, mock_client):
        """Test copying nexset."""
        # Arrange
        nexset_id = 1001
        copy_options = NexsetCopyOptions(
            copy_access_controls=True,
            owner_id=123
        )
        mock_factory = MockDataFactory()
        mock_response = mock_factory.create_mock_nexset(id=1002, copied_from_id=nexset_id)
        mock_client.http_client.add_response(f"/data_sets/{nexset_id}/copy", mock_response)

        # Act
        copied_nexset = mock_client.nexsets.copy(nexset_id, copy_options)

        # Assert
        assert isinstance(copied_nexset, Nexset)
        assert copied_nexset.id == 1002
        mock_client.http_client.assert_request_made("POST", f"/data_sets/{nexset_id}/copy")

    def test_copy_nexset_without_options(self, mock_client):
        """Test copying nexset without options."""
        # Arrange
        nexset_id = 1001
        mock_factory = MockDataFactory()
        mock_response = mock_factory.create_mock_nexset(id=1002)
        mock_client.http_client.add_response(f"/data_sets/{nexset_id}/copy", mock_response)

        # Act
        mock_client.nexsets.copy(nexset_id)

        # Assert
        mock_client.http_client.assert_request_made("POST", f"/data_sets/{nexset_id}/copy")

    def test_http_error_handling(self, mock_client):
        """Test HTTP error handling."""
        # Arrange
        mock_client.http_client.add_error(
            "/data_sets",
            HttpClientError(
                "Server Error",
                status_code=500,
                response={"message": "Internal server error"}
            )
        )

        # Act & Assert
        with pytest.raises(ServerError) as exc_info:
            mock_client.nexsets.list()

        assert exc_info.value.status_code == 500

    def test_not_found_error(self, mock_client):
        """Test not found error handling."""
        # Arrange
        nexset_id = 99999
        mock_client.http_client.add_error(
            f"/data_sets/{nexset_id}",
            HttpClientError(
                "Not found",
                status_code=404,
                response={"message": "Nexset not found"}
            )
        )

        # Act & Assert
        with pytest.raises(NotFoundError):
            mock_client.nexsets.get(nexset_id)

    def test_validation_error_handling(self, mock_client):
        """Test validation error handling."""
        # Arrange
        invalid_response = {
            # Missing required 'id' field
            "name": "Invalid Dataset"
        }
        mock_client.http_client.add_response("/data_sets/1001", invalid_response)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            mock_client.nexsets.get(1001)

        # Check that the error mentions the missing fields
        error_str = str(exc_info.value)
        assert "id" in error_str

    def test_empty_list_response(self, mock_client):
        """Test handling empty list response."""
        # Arrange
        mock_client.http_client.add_response("/data_sets", [])

        # Act
        nexsets = mock_client.nexsets.list()

        # Assert
        assert nexsets == []
        assert len(nexsets) == 0
