"""Unit tests for lookups resource."""
import pytest
from unittest.mock import MagicMock
from typing import List, Dict, Any

from nexla_sdk import NexlaClient
from nexla_sdk.models.lookups.responses import Lookup
from nexla_sdk.models.lookups.requests import LookupCreate, LookupUpdate, LookupEntriesUpsert
from nexla_sdk.exceptions import NexlaError, ServerError
from nexla_sdk.http_client import HttpClientError

from tests.utils.fixtures import MockHTTPClient, create_test_client, create_mock_response
from tests.utils.mock_builders import MockDataFactory
from tests.utils.assertions import NexlaAssertions


class TestLookupsUnit:
    """Unit tests for lookups resource."""
    
    @pytest.fixture
    def mock_client(self) -> NexlaClient:
        """Create a test client with mocked HTTP."""
        return create_test_client()
    
    @pytest.fixture
    def mock_factory(self) -> MockDataFactory:
        """Create a mock data factory."""
        return MockDataFactory()
    
    def test_list_lookups(self, mock_client, mock_factory):
        """Test listing all lookups."""
        # Arrange
        mock_lookups = [
            mock_factory.create_mock_lookup(id=1001, name="Event Code Lookup"),
            mock_factory.create_mock_lookup(id=1002, name="Status Code Lookup")
        ]
        mock_client.http_client.request = MagicMock(return_value=mock_lookups)
        
        # Act
        result = mock_client.lookups.list()
        
        # Assert
        assert len(result) == 2
        assert all(isinstance(lookup, Lookup) for lookup in result)
        NexlaAssertions.assert_lookup_response(result[0], mock_lookups[0])
        NexlaAssertions.assert_lookup_response(result[1], mock_lookups[1])
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "GET", 
            f"{mock_client.api_url}/data_maps",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params={}
        )
    
    def test_list_lookups_with_parameters(self, mock_client, mock_factory):
        """Test listing lookups with query parameters."""
        # Arrange
        mock_lookups = [mock_factory.create_mock_lookup()]
        mock_client.http_client.request = MagicMock(return_value=mock_lookups)
        
        # Act
        result = mock_client.lookups.list(page=2, per_page=50, access_role="collaborator")
        
        # Assert
        assert len(result) == 1
        
        # Verify request with parameters
        mock_client.http_client.request.assert_called_once_with(
            "GET",
            f"{mock_client.api_url}/data_maps",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params={"page": 2, "per_page": 50, "access_role": "collaborator"}
        )
    
    def test_get_lookup(self, mock_client, mock_factory):
        """Test getting a specific lookup by ID."""
        # Arrange
        lookup_id = 1001
        mock_lookup = mock_factory.create_mock_lookup(id=lookup_id, name="Event Code Lookup")
        mock_client.http_client.request = MagicMock(return_value=mock_lookup)
        
        # Act
        result = mock_client.lookups.get(lookup_id)
        
        # Assert
        assert isinstance(result, Lookup)
        NexlaAssertions.assert_lookup_response(result, mock_lookup)
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "GET",
            f"{mock_client.api_url}/data_maps/{lookup_id}",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params={}
        )
    
    def test_get_lookup_with_expand(self, mock_client, mock_factory):
        """Test getting a lookup with expanded details."""
        # Arrange
        lookup_id = 1001
        mock_lookup = mock_factory.create_mock_lookup(id=lookup_id)
        mock_client.http_client.request = MagicMock(return_value=mock_lookup)
        
        # Act
        result = mock_client.lookups.get(lookup_id, expand=True)
        
        # Assert
        assert isinstance(result, Lookup)
        
        # Verify request includes expand parameter
        mock_client.http_client.request.assert_called_once_with(
            "GET",
            f"{mock_client.api_url}/data_maps/{lookup_id}",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params={"expand": 1}
        )
    
    def test_create_lookup(self, mock_client, mock_factory):
        """Test creating a new lookup."""
        # Arrange
        create_data = LookupCreate(
            name="New Event Lookup",
            data_type="string",
            map_primary_key="eventId",
            description="Maps event IDs to descriptions",
            data_defaults={"eventId": "Unknown", "description": "Unknown Event"},
            emit_data_default=True
        )
        
        mock_lookup = mock_factory.create_mock_lookup(
            id=1003,
            name="New Event Lookup",
            data_type="string",
            map_primary_key="eventId"
        )
        mock_client.http_client.request = MagicMock(return_value=mock_lookup)
        
        # Act
        result = mock_client.lookups.create(create_data)
        
        # Assert
        assert isinstance(result, Lookup)
        NexlaAssertions.assert_lookup_response(result, mock_lookup)
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "POST",
            f"{mock_client.api_url}/data_maps",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            json={
                "name": "New Event Lookup",
                "data_type": "string",
                "map_primary_key": "eventId",
                "description": "Maps event IDs to descriptions",
                "data_defaults": {"eventId": "Unknown", "description": "Unknown Event"},
                "emit_data_default": True,
                "tags": []
            }
        )
    
    def test_update_lookup(self, mock_client, mock_factory):
        """Test updating an existing lookup."""
        # Arrange
        lookup_id = 1001
        update_data = LookupUpdate(
            name="Updated Event Lookup",
            description="Updated description",
            emit_data_default=False
        )
        
        mock_lookup = mock_factory.create_mock_lookup(
            id=lookup_id,
            name="Updated Event Lookup",
            description="Updated description"
        )
        mock_client.http_client.request = MagicMock(return_value=mock_lookup)
        
        # Act
        result = mock_client.lookups.update(lookup_id, update_data)
        
        # Assert
        assert isinstance(result, Lookup)
        NexlaAssertions.assert_lookup_response(result, mock_lookup)
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "PUT",
            f"{mock_client.api_url}/data_maps/{lookup_id}",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            json={
                "name": "Updated Event Lookup",
                "description": "Updated description",
                "emit_data_default": False
            }
        )
    
    def test_delete_lookup(self, mock_client):
        """Test deleting a lookup."""
        # Arrange
        lookup_id = 1001
        mock_client.http_client.request = MagicMock(return_value={"status": "deleted"})
        
        # Act
        result = mock_client.lookups.delete(lookup_id)
        
        # Assert
        assert result == {"status": "deleted"}
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "DELETE",
            f"{mock_client.api_url}/data_maps/{lookup_id}",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            }
        )
    
    def test_upsert_entries(self, mock_client, mock_factory):
        """Test upserting entries in a lookup."""
        # Arrange
        lookup_id = 1001
        entries = [
            {"eventId": "001", "description": "Login", "category": "Auth"},
            {"eventId": "002", "description": "Logout", "category": "Auth"}
        ]
        
        mock_response = [
            {"eventId": "001", "description": "Login", "category": "Auth"},
            {"eventId": "002", "description": "Logout", "category": "Auth"}
        ]
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        result = mock_client.lookups.upsert_entries(lookup_id, entries)
        
        # Assert
        assert result == mock_response
        assert len(result) == 2
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "PUT",
            f"{mock_client.api_url}/data_maps/{lookup_id}/entries",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            json={"entries": entries}
        )
    
    def test_get_entries_single_key(self, mock_client):
        """Test getting specific entries by single key."""
        # Arrange
        lookup_id = 1001
        entry_key = "001"
        mock_response = [
            {"eventId": "001", "description": "Login", "category": "Auth"}
        ]
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        result = mock_client.lookups.get_entries(lookup_id, entry_key)
        
        # Assert
        assert result == mock_response
        assert len(result) == 1
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "GET",
            f"{mock_client.api_url}/data_maps/{lookup_id}/entries/{entry_key}",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            }
        )
    
    def test_get_entries_multiple_keys(self, mock_client):
        """Test getting specific entries by multiple keys."""
        # Arrange
        lookup_id = 1001
        entry_keys = ["001", "002"]
        mock_response = [
            {"eventId": "001", "description": "Login", "category": "Auth"},
            {"eventId": "002", "description": "Logout", "category": "Auth"}
        ]
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        result = mock_client.lookups.get_entries(lookup_id, entry_keys)
        
        # Assert
        assert result == mock_response
        assert len(result) == 2
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "GET",
            f"{mock_client.api_url}/data_maps/{lookup_id}/entries/001,002",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            }
        )
    
    def test_delete_entries_single_key(self, mock_client):
        """Test deleting specific entries by single key."""
        # Arrange
        lookup_id = 1001
        entry_key = "001"
        mock_client.http_client.request = MagicMock(return_value={"status": "deleted"})
        
        # Act
        result = mock_client.lookups.delete_entries(lookup_id, entry_key)
        
        # Assert
        assert result == {"status": "deleted"}
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "DELETE",
            f"{mock_client.api_url}/data_maps/{lookup_id}/entries/{entry_key}",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            }
        )
    
    def test_delete_entries_multiple_keys(self, mock_client):
        """Test deleting specific entries by multiple keys."""
        # Arrange
        lookup_id = 1001
        entry_keys = ["001", "002"]
        mock_client.http_client.request = MagicMock(return_value={"status": "deleted"})
        
        # Act
        result = mock_client.lookups.delete_entries(lookup_id, entry_keys)
        
        # Assert
        assert result == {"status": "deleted"}
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "DELETE",
            f"{mock_client.api_url}/data_maps/{lookup_id}/entries/001,002",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            }
        )
    
    def test_http_error_handling(self, mock_client):
        """Test HTTP error handling."""
        # Arrange
        mock_client.http_client.request = MagicMock(
            side_effect=HttpClientError(
                "Not found",
                status_code=404,
                response={"message": "Lookup not found"}
            )
        )
        
        # Act & Assert
        # 404 errors map to NotFoundError which inherits from ServerError
        with pytest.raises(ServerError) as exc_info:
            mock_client.lookups.get(9999)
        
        # Check error details
        assert exc_info.value.status_code == 404
        assert "Resource not found" in str(exc_info.value)
    
    def test_validation_error_handling(self, mock_client):
        """Test handling of invalid lookup response."""
        # Arrange
        invalid_response = {
            # Missing required 'id' field
            "name": "Invalid Lookup",
            "map_primary_key": "key"
        }
        mock_client.http_client.request = MagicMock(return_value=invalid_response)
        
        # Act & Assert
        from pydantic import ValidationError
        with pytest.raises(ValidationError) as exc_info:
            mock_client.lookups.get(1001)
        
        # Check that the error mentions the missing fields
        error_str = str(exc_info.value)
        assert "id" in error_str
    
    def test_empty_list_response(self, mock_client):
        """Test handling of empty list response."""
        # Arrange
        mock_client.http_client.request = MagicMock(return_value=[])
        
        # Act
        result = mock_client.lookups.list()
        
        # Assert
        assert result == []
        assert len(result) == 0 