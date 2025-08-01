"""Integration tests for sources resource with real API calls."""

import pytest
import time
from typing import List

from nexla_sdk.exceptions import AuthenticationError, NotFoundError
from nexla_sdk.models.sources.responses import Source
from nexla_sdk.models.sources.requests import SourceCreate, SourceUpdate, SourceCopyOptions
from tests.utils import MockDataFactory


@pytest.mark.integration
class TestSourcesIntegration:
    """Integration tests for sources using real API."""
    
    def test_list_sources(self, integration_client):
        """Test listing sources with real API."""
        # Act
        sources = integration_client.sources.list()
        
        # Assert
        assert isinstance(sources, list)
        for source in sources:
            assert isinstance(source, Source)
            assert source.id is not None
            assert source.name is not None
            assert source.source_type is not None
    
    def test_list_sources_with_pagination(self, integration_client):
        """Test listing sources with pagination."""
        # Act
        page1 = integration_client.sources.list(page=1, per_page=5)
        page2 = integration_client.sources.list(page=2, per_page=5)
        
        # Assert
        assert isinstance(page1, list)
        assert isinstance(page2, list)
        assert len(page1) <= 5
        assert len(page2) <= 5
        
        # Ensure no overlap (if we have enough sources)
        if len(page1) == 5 and len(page2) > 0:
            page1_ids = {s.id for s in page1}
            page2_ids = {s.id for s in page2}
            assert page1_ids.isdisjoint(page2_ids)
    
    def test_list_sources_with_access_role_filter(self, integration_client):
        """Test listing sources filtered by access role."""
        # Act
        owner_sources = integration_client.sources.list(access_role="owner")
        
        # Assert
        assert isinstance(owner_sources, list)
        for source in owner_sources:
            assert "owner" in source.access_roles
    
    def test_get_source_details(self, integration_client):
        """Test getting detailed source information."""
        # Arrange - Get a source ID from the list
        sources = integration_client.sources.list(per_page=1)
        if not sources:
            pytest.skip("No sources available for testing")
        
        source_id = sources[0].id
        
        # Act
        source = integration_client.sources.get(source_id)
        detailed_source = integration_client.sources.get(source_id, expand=True)
        
        # Assert
        assert isinstance(source, Source)
        assert isinstance(detailed_source, Source)
        assert source.id == source_id
        assert detailed_source.id == source_id
        
        # Expanded version might have more information
        # (depends on actual API response structure)
    
    def test_get_nonexistent_source(self, integration_client):
        """Test getting a source that doesn't exist."""
        # Act & Assert
        with pytest.raises(NotFoundError):
            integration_client.sources.get(999999999)  # Very unlikely to exist
    
    @pytest.mark.skip(reason="Requires specific test credentials and cleanup")
    def test_create_update_delete_source_lifecycle(self, integration_client):
        """Test complete source lifecycle: create, update, delete."""
        # This test is skipped by default as it requires:
        # 1. Valid test credentials for a source type
        # 2. Proper cleanup to avoid leaving test resources
        # 3. Specific test environment setup
        
        # Create source
        create_data = SourceCreate(
            name=f"Integration Test Source {int(time.time())}",
            source_type="api_push",  # Use a safe source type
            description="Integration test source - safe to delete"
        )
        
        # Act - Create
        created_source = integration_client.sources.create(create_data)
        
        try:
            # Assert creation
            assert isinstance(created_source, Source)
            assert created_source.name == create_data.name
            assert created_source.source_type == create_data.source_type
            
            # Act - Update
            update_data = SourceUpdate(
                description="Updated integration test source"
            )
            updated_source = integration_client.sources.update(created_source.id, update_data)
            
            # Assert update
            assert updated_source.description == update_data.description
            
            # Act - Activate/Pause (if supported)
            if created_source.status in ["INIT", "PAUSED"]:
                activated_source = integration_client.sources.activate(created_source.id)
                assert activated_source.status == "ACTIVE"
                
                paused_source = integration_client.sources.pause(created_source.id)
                assert paused_source.status == "PAUSED"
        
        finally:
            # Cleanup - Delete the test source
            try:
                integration_client.sources.delete(created_source.id)
            except Exception as e:
                # Log but don't fail the test on cleanup issues
                print(f"Warning: Failed to clean up test source {created_source.id}: {e}")
    
    def test_source_access_control(self, integration_client):
        """Test source access control operations."""
        # Arrange - Get a source the user owns
        owner_sources = integration_client.sources.list(access_role="owner", per_page=1)
        if not owner_sources:
            pytest.skip("No owned sources available for access control testing")
        
        source_id = owner_sources[0].id
        
        # Act - Get current accessors
        accessors = integration_client.sources.get_accessors(source_id)
        
        # Assert
        assert isinstance(accessors, list)
        # Should at least have the owner's access
        assert len(accessors) >= 1
    
    def test_source_audit_log(self, integration_client):
        """Test getting source audit log."""
        # Arrange - Get a source ID
        sources = integration_client.sources.list(per_page=1)
        if not sources:
            pytest.skip("No sources available for audit log testing")
        
        source_id = sources[0].id
        
        # Act
        audit_log = integration_client.sources.get_audit_log(source_id)
        
        # Assert
        assert isinstance(audit_log, list)
        # Audit log might be empty for new sources, so just check structure
        for entry in audit_log:
            assert "id" in entry
            assert "event" in entry
            assert "created_at" in entry
    
    def test_source_pagination_consistency(self, integration_client):
        """Test that pagination returns consistent results."""
        # Act - Get first page twice
        page1_first = integration_client.sources.list(page=1, per_page=3)
        page1_second = integration_client.sources.list(page=1, per_page=3)
        
        # Assert - Should be identical (assuming no concurrent modifications)
        assert len(page1_first) == len(page1_second)
        for i in range(len(page1_first)):
            assert page1_first[i].id == page1_second[i].id
    
    @pytest.mark.performance
    def test_list_sources_performance(self, integration_client):
        """Test that listing sources completes within reasonable time."""

        # Act
        start_time = time.time()
        sources = integration_client.sources.list(per_page=50)
        end_time = time.time()
        
        # Assert - Should complete within 5 seconds
        elapsed_time = end_time - start_time
        assert elapsed_time < 5.0, f"List sources took {elapsed_time:.2f} seconds"
        
        # Should return some sources (or at least not fail)
        assert isinstance(sources, list)
    
    def test_source_data_structure_consistency(self, integration_client):
        """Test that source data structure is consistent across API calls."""
        # Arrange
        sources = integration_client.sources.list(per_page=5)
        if not sources:
            pytest.skip("No sources available for consistency testing")
        
        # Act & Assert - Check each source has consistent structure
        for source in sources:
            # Required fields should always be present
            assert source.id is not None
            assert source.name is not None
            assert source.status is not None
            assert source.source_type is not None
            assert isinstance(source.access_roles, list)
            
            # Optional fields should be properly typed when present
            if source.description is not None:
                assert isinstance(source.description, str)
            
            if source.data_sets is not None:
                assert isinstance(source.data_sets, list)
            
            if source.tags is not None:
                assert isinstance(source.tags, list)
    
    def test_error_handling_with_invalid_requests(self, integration_client):
        """Test error handling with various invalid requests."""
        # Test invalid source ID
        with pytest.raises(NotFoundError):
            integration_client.sources.get(-1)
        
        # Test invalid pagination parameters
        try:
            # Very large page number should either return empty list or error gracefully
            result = integration_client.sources.list(page=999999, per_page=1)
            assert isinstance(result, list)  # Should be empty list
        except Exception as e:
            # If it raises an exception, it should be a reasonable one
            assert not isinstance(e, AuthenticationError)  # Should not be auth error
    
    @pytest.mark.slow
    def test_comprehensive_source_fields(self, integration_client):
        """Test that sources have all expected fields from the API documentation."""
        # Arrange
        sources = integration_client.sources.list(per_page=10)
        if not sources:
            pytest.skip("No sources available for field testing")
        
        # Get detailed view of first source
        source = integration_client.sources.get(sources[0].id, expand=True)
        
        # Assert - Check for expected fields based on API documentation
        expected_fields = [
            'id', 'name', 'status', 'source_type', 'access_roles',
            'owner', 'org', 'created_at', 'updated_at'
        ]
        
        for field in expected_fields:
            assert hasattr(source, field), f"Source missing expected field: {field}"
        
        # Check owner structure
        if source.owner:
            assert hasattr(source.owner, 'id')
            assert hasattr(source.owner, 'full_name')
        
        # Check org structure  
        if source.org:
            assert hasattr(source.org, 'id')
            assert hasattr(source.org, 'name') 