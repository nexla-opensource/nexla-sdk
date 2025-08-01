"""Integration tests for lookups resource."""
import os
import pytest
from typing import Optional, List

from nexla_sdk import NexlaClient
from nexla_sdk.models.lookups.responses import Lookup
from nexla_sdk.models.lookups.requests import LookupCreate, LookupUpdate
from nexla_sdk.exceptions import NexlaError, ServerError

from tests.utils.fixtures import get_test_credentials


@pytest.mark.integration
class TestLookupsIntegration:
    """Integration tests for lookups resource."""
    
    @pytest.fixture(scope="class")
    def client(self) -> Optional[NexlaClient]:
        """Create a real Nexla client for integration tests."""
        creds = get_test_credentials()
        if not creds:
            pytest.skip("No test credentials available")
        
        return NexlaClient(**creds)
    
    @pytest.fixture
    def test_lookup_data(self) -> LookupCreate:
        """Create test lookup data."""
        return LookupCreate(
            name="Test SDK Lookup",
            data_type="string",
            map_primary_key="eventId",
            description="Test lookup created by SDK integration tests",
            data_defaults={"eventId": "Unknown", "description": "Unknown Event"},
            emit_data_default=True,
            tags=["test", "sdk", "integration"]
        )
    
    def test_lookup_crud_operations(self, client, test_lookup_data):
        """Test complete CRUD operations for lookups."""
        if not client:
            pytest.skip("No test client available")
        
        created_lookup = None
        try:
            # Create lookup
            created_lookup = client.lookups.create(test_lookup_data)
            assert isinstance(created_lookup, Lookup)
            assert created_lookup.name == test_lookup_data.name
            assert created_lookup.data_type == test_lookup_data.data_type
            assert created_lookup.map_primary_key == test_lookup_data.map_primary_key
            assert created_lookup.description == test_lookup_data.description
            assert "test" in created_lookup.tags
            
            # Get lookup
            retrieved_lookup = client.lookups.get(created_lookup.id)
            assert isinstance(retrieved_lookup, Lookup)
            assert retrieved_lookup.id == created_lookup.id
            assert retrieved_lookup.name == created_lookup.name
            
            # Update lookup
            update_data = LookupUpdate(
                name="Updated Test SDK Lookup",
                description="Updated description for test lookup",
                emit_data_default=False
            )
            updated_lookup = client.lookups.update(created_lookup.id, update_data)
            assert isinstance(updated_lookup, Lookup)
            assert updated_lookup.name == "Updated Test SDK Lookup"
            assert updated_lookup.description == "Updated description for test lookup"
            assert updated_lookup.emit_data_default is False
            
            # List lookups (should include our created lookup)
            lookups = client.lookups.list()
            assert isinstance(lookups, list)
            lookup_ids = [lookup.id for lookup in lookups]
            assert created_lookup.id in lookup_ids
            
        finally:
            # Clean up - delete the lookup
            if created_lookup:
                try:
                    client.lookups.delete(created_lookup.id)
                except Exception as e:
                    print(f"Warning: Failed to clean up test lookup {created_lookup.id}: {e}")
    
    def test_lookup_entry_operations(self, client, test_lookup_data):
        """Test lookup entry operations."""
        if not client:
            pytest.skip("No test client available")
        
        created_lookup = None
        try:
            # Create lookup first
            created_lookup = client.lookups.create(test_lookup_data)
            
            # Test upsert entries
            entries = [
                {"eventId": "001", "description": "Login Event", "category": "Auth"},
                {"eventId": "002", "description": "Logout Event", "category": "Auth"},
                {"eventId": "003", "description": "Purchase Event", "category": "Commerce"}
            ]
            
            upserted_entries = client.lookups.upsert_entries(created_lookup.id, entries)
            assert isinstance(upserted_entries, list)
            assert len(upserted_entries) == 3
            
            # Test get single entry
            single_entry = client.lookups.get_entries(created_lookup.id, "001")
            assert isinstance(single_entry, list)
            assert len(single_entry) == 1
            assert single_entry[0]["eventId"] == "001"
            assert single_entry[0]["description"] == "Login Event"
            
            # Test get multiple entries
            multiple_entries = client.lookups.get_entries(created_lookup.id, ["001", "002"])
            assert isinstance(multiple_entries, list)
            assert len(multiple_entries) == 2
            entry_ids = [entry["eventId"] for entry in multiple_entries]
            assert "001" in entry_ids
            assert "002" in entry_ids
            
            # Test delete single entry
            client.lookups.delete_entries(created_lookup.id, "003")
            
            # Verify entry was deleted (should only have 001 and 002 now)
            remaining_entries = client.lookups.get_entries(created_lookup.id, ["001", "002", "003"])
            assert len(remaining_entries) == 2  # 003 should be gone
            
            # Test delete multiple entries
            client.lookups.delete_entries(created_lookup.id, ["001", "002"])
            
        finally:
            # Clean up
            if created_lookup:
                try:
                    client.lookups.delete(created_lookup.id)
                except Exception as e:
                    print(f"Warning: Failed to clean up test lookup {created_lookup.id}: {e}")
    
    def test_lookup_with_expand(self, client):
        """Test getting lookup with expanded details."""
        if not client:
            pytest.skip("No test client available")
        
        # Get first available lookup
        lookups = client.lookups.list()
        if not lookups:
            pytest.skip("No lookups available for testing expand functionality")
        
        first_lookup = lookups[0]
        
        # Get with expand
        expanded_lookup = client.lookups.get(first_lookup.id, expand=True)
        assert isinstance(expanded_lookup, Lookup)
        assert expanded_lookup.id == first_lookup.id
        # Expanded version may have additional details
    
    def test_list_with_pagination(self, client):
        """Test listing lookups with pagination."""
        if not client:
            pytest.skip("No test client available")
        
        # Test pagination parameters
        page1 = client.lookups.list(page=1, per_page=5)
        assert isinstance(page1, list)
        assert len(page1) <= 5
        
        # Test with access role filter
        filtered_lookups = client.lookups.list(access_role="owner")
        assert isinstance(filtered_lookups, list)
    
    def test_lookup_not_found_error(self, client):
        """Test handling of lookup not found error."""
        if not client:
            pytest.skip("No test client available")
        
        # Try to get a non-existent lookup
        with pytest.raises(ServerError) as exc_info:
            client.lookups.get(999999)  # Very unlikely to exist
        
        assert exc_info.value.status_code == 404
    
    def test_lookup_validation_errors(self, client):
        """Test validation errors during lookup creation."""
        if not client:
            pytest.skip("No test client available")
        
        # Test with missing required fields
        invalid_data = LookupCreate(
            name="",  # Empty name should cause validation error
            data_type="string",
            map_primary_key="key"
        )
        
        with pytest.raises((ServerError, Exception)):
            client.lookups.create(invalid_data) 