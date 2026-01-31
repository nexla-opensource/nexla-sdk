"""Unit tests for lookups resource."""

import pytest
from pydantic import ValidationError

from nexla_sdk.exceptions import NotFoundError
from nexla_sdk.http_client import HttpClientError
from nexla_sdk.models.lookups.requests import LookupCreate, LookupUpdate
from nexla_sdk.models.lookups.responses import Lookup
from tests.utils.mock_builders import MockDataFactory


@pytest.mark.unit
class TestLookupsUnit:
    """Unit tests for lookups resource."""

    def test_list_lookups(self, mock_client):
        """Test listing all lookups."""
        # Arrange
        mock_factory = MockDataFactory()
        mock_lookups = [
            mock_factory.create_mock_lookup(id=1001, name="Event Code Lookup"),
            mock_factory.create_mock_lookup(id=1002, name="Status Code Lookup"),
        ]
        mock_client.http_client.add_response("/data_maps", mock_lookups)

        # Act
        result = mock_client.lookups.list()

        # Assert
        assert len(result) == 2
        assert all(isinstance(lookup, Lookup) for lookup in result)
        mock_client.http_client.assert_request_made("GET", "/data_maps")

    def test_list_lookups_with_parameters(self, mock_client):
        """Test listing lookups with query parameters."""
        # Arrange
        mock_factory = MockDataFactory()
        mock_lookups = [mock_factory.create_mock_lookup()]
        mock_client.http_client.add_response("/data_maps", mock_lookups)

        # Act
        result = mock_client.lookups.list(
            page=2, per_page=50, access_role="collaborator"
        )

        # Assert
        assert len(result) == 1
        mock_client.http_client.assert_request_made("GET", "/data_maps")

        # Verify parameters were sent
        request = mock_client.http_client.get_last_request()
        assert request["params"].get("page") == 2
        assert request["params"].get("per_page") == 50
        assert request["params"].get("access_role") == "collaborator"

    def test_get_lookup(self, mock_client):
        """Test getting a specific lookup by ID."""
        # Arrange
        lookup_id = 1001
        mock_factory = MockDataFactory()
        mock_lookup = mock_factory.create_mock_lookup(
            id=lookup_id, name="Event Code Lookup"
        )
        mock_client.http_client.add_response(f"/data_maps/{lookup_id}", mock_lookup)

        # Act
        result = mock_client.lookups.get(lookup_id)

        # Assert
        assert isinstance(result, Lookup)
        assert result.id == lookup_id
        mock_client.http_client.assert_request_made("GET", f"/data_maps/{lookup_id}")

    def test_get_lookup_with_expand(self, mock_client):
        """Test getting a lookup with expanded details."""
        # Arrange
        lookup_id = 1001
        mock_factory = MockDataFactory()
        mock_lookup = mock_factory.create_mock_lookup(id=lookup_id)
        mock_client.http_client.add_response(f"/data_maps/{lookup_id}", mock_lookup)

        # Act
        result = mock_client.lookups.get(lookup_id, expand=True)

        # Assert
        assert isinstance(result, Lookup)
        mock_client.http_client.assert_request_made("GET", f"/data_maps/{lookup_id}")

        # Verify expand parameter was sent
        request = mock_client.http_client.get_last_request()
        assert request["params"].get("expand") == 1

    def test_create_lookup(self, mock_client):
        """Test creating a new lookup."""
        # Arrange
        create_data = LookupCreate(
            name="New Event Lookup",
            data_type="string",
            map_primary_key="eventId",
            description="Maps event IDs to descriptions",
            data_defaults={"eventId": "Unknown", "description": "Unknown Event"},
            emit_data_default=True,
        )

        mock_factory = MockDataFactory()
        mock_lookup = mock_factory.create_mock_lookup(
            id=1003,
            name="New Event Lookup",
            data_type="string",
            map_primary_key="eventId",
        )
        mock_client.http_client.add_response("/data_maps", mock_lookup)

        # Act
        result = mock_client.lookups.create(create_data)

        # Assert
        assert isinstance(result, Lookup)
        assert result.id == 1003
        mock_client.http_client.assert_request_made("POST", "/data_maps")

        # Verify request body
        request = mock_client.http_client.get_last_request()
        assert request["json"]["name"] == "New Event Lookup"
        assert request["json"]["data_type"] == "string"
        assert request["json"]["map_primary_key"] == "eventId"

    def test_update_lookup(self, mock_client):
        """Test updating an existing lookup."""
        # Arrange
        lookup_id = 1001
        update_data = LookupUpdate(
            name="Updated Event Lookup",
            description="Updated description",
            emit_data_default=False,
        )

        mock_factory = MockDataFactory()
        mock_lookup = mock_factory.create_mock_lookup(
            id=lookup_id, name="Updated Event Lookup", description="Updated description"
        )
        mock_client.http_client.add_response(f"/data_maps/{lookup_id}", mock_lookup)

        # Act
        result = mock_client.lookups.update(lookup_id, update_data)

        # Assert
        assert isinstance(result, Lookup)
        assert result.name == "Updated Event Lookup"
        mock_client.http_client.assert_request_made("PUT", f"/data_maps/{lookup_id}")

    def test_delete_lookup(self, mock_client):
        """Test deleting a lookup."""
        # Arrange
        lookup_id = 1001
        mock_client.http_client.add_response(
            f"/data_maps/{lookup_id}", {"status": "deleted"}
        )

        # Act
        result = mock_client.lookups.delete(lookup_id)

        # Assert
        assert result == {"status": "deleted"}
        mock_client.http_client.assert_request_made("DELETE", f"/data_maps/{lookup_id}")

    def test_upsert_entries(self, mock_client):
        """Test upserting entries in a lookup."""
        # Arrange
        lookup_id = 1001
        entries = [
            {"eventId": "001", "description": "Login", "category": "Auth"},
            {"eventId": "002", "description": "Logout", "category": "Auth"},
        ]

        mock_response = [
            {"eventId": "001", "description": "Login", "category": "Auth"},
            {"eventId": "002", "description": "Logout", "category": "Auth"},
        ]
        mock_client.http_client.add_response(
            f"/data_maps/{lookup_id}/entries", mock_response
        )

        # Act
        result = mock_client.lookups.upsert_entries(lookup_id, entries)

        # Assert
        assert result == mock_response
        assert len(result) == 2
        mock_client.http_client.assert_request_made(
            "PUT", f"/data_maps/{lookup_id}/entries"
        )

    def test_get_entries_single_key(self, mock_client):
        """Test getting specific entries by single key."""
        # Arrange
        lookup_id = 1001
        entry_key = "001"
        mock_response = [{"eventId": "001", "description": "Login", "category": "Auth"}]
        mock_client.http_client.add_response(
            f"/data_maps/{lookup_id}/entries/{entry_key}", mock_response
        )

        # Act
        result = mock_client.lookups.get_entries(lookup_id, entry_key)

        # Assert
        assert result == mock_response
        assert len(result) == 1
        mock_client.http_client.assert_request_made(
            "GET", f"/data_maps/{lookup_id}/entries/{entry_key}"
        )

    def test_get_entries_multiple_keys(self, mock_client):
        """Test getting specific entries by multiple keys."""
        # Arrange
        lookup_id = 1001
        entry_keys = ["001", "002"]
        mock_response = [
            {"eventId": "001", "description": "Login", "category": "Auth"},
            {"eventId": "002", "description": "Logout", "category": "Auth"},
        ]
        mock_client.http_client.add_response(
            f"/data_maps/{lookup_id}/entries/001,002", mock_response
        )

        # Act
        result = mock_client.lookups.get_entries(lookup_id, entry_keys)

        # Assert
        assert result == mock_response
        assert len(result) == 2
        mock_client.http_client.assert_request_made(
            "GET", f"/data_maps/{lookup_id}/entries/001,002"
        )

    def test_delete_entries_single_key(self, mock_client):
        """Test deleting specific entries by single key."""
        # Arrange
        lookup_id = 1001
        entry_key = "001"
        mock_client.http_client.add_response(
            f"/data_maps/{lookup_id}/entries/{entry_key}", {"status": "deleted"}
        )

        # Act
        result = mock_client.lookups.delete_entries(lookup_id, entry_key)

        # Assert
        assert result == {"status": "deleted"}
        mock_client.http_client.assert_request_made(
            "DELETE", f"/data_maps/{lookup_id}/entries/{entry_key}"
        )

    def test_delete_entries_multiple_keys(self, mock_client):
        """Test deleting specific entries by multiple keys."""
        # Arrange
        lookup_id = 1001
        entry_keys = ["001", "002"]
        mock_client.http_client.add_response(
            f"/data_maps/{lookup_id}/entries/001,002", {"status": "deleted"}
        )

        # Act
        result = mock_client.lookups.delete_entries(lookup_id, entry_keys)

        # Assert
        assert result == {"status": "deleted"}
        mock_client.http_client.assert_request_made(
            "DELETE", f"/data_maps/{lookup_id}/entries/001,002"
        )

    def test_http_error_handling(self, mock_client):
        """Test HTTP error handling."""
        # Arrange
        mock_client.http_client.add_error(
            "/data_maps/9999",
            HttpClientError(
                "Not found", status_code=404, response={"message": "Lookup not found"}
            ),
        )

        # Act & Assert
        with pytest.raises(NotFoundError):
            mock_client.lookups.get(9999)

    def test_validation_error_handling(self, mock_client):
        """Test handling of invalid lookup response."""
        # Arrange
        invalid_response = {
            # Missing required 'id' field
            "name": "Invalid Lookup",
            "map_primary_key": "key",
        }
        mock_client.http_client.add_response("/data_maps/1001", invalid_response)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            mock_client.lookups.get(1001)

        # Check that the error mentions the missing fields
        error_str = str(exc_info.value)
        assert "id" in error_str

    def test_empty_list_response(self, mock_client):
        """Test handling of empty list response."""
        # Arrange
        mock_client.http_client.add_response("/data_maps", [])

        # Act
        result = mock_client.lookups.list()

        # Assert
        assert result == []
        assert len(result) == 0
