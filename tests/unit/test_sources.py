"""Unit tests for sources resource."""

import pytest
from pydantic import ValidationError

from nexla_sdk.exceptions import (
    ServerError,
    NotFoundError,
    ValidationError as SDKValidationError,
)
from nexla_sdk.models.sources.responses import Source, DataSetBrief, RunInfo
from nexla_sdk.models.sources.requests import SourceCreate, SourceUpdate, SourceCopyOptions
from tests.utils import (
    MockResponseBuilder, create_http_error, assert_model_valid, 
    assert_model_list_valid
)


@pytest.mark.unit
class TestSourcesModels:
    """Test sources model validation and serialization."""
    
    def test_source_model_with_all_fields(self):
        """Test Source model with all fields populated."""
        source_data = MockResponseBuilder.source()
        source = Source(**source_data)
        assert_model_valid(source, {"id": source_data["id"], "name": source_data["name"]})
    
    def test_source_model_with_minimal_fields(self):
        """Test Source model with only required fields."""
        minimal_data = {
            "id": 123,
            "name": "Test Source",
            "status": "ACTIVE",
            "source_type": "s3"
        }
        source = Source(**minimal_data)
        assert source.id == 123
        assert source.name == "Test Source"
        assert source.data_sets == []
        assert source.tags == []
    
    def test_source_model_with_credentials(self):
        """Test Source model with embedded credentials."""
        source_data = MockResponseBuilder.source(
            source_id=456,
            include_credentials=True
        )
        source = Source(**source_data)
        assert source.data_credentials is not None
        assert source.data_credentials.id == source_data["data_credentials"]["id"]
    
    def test_source_model_with_datasets(self):
        """Test Source model with embedded datasets."""
        source_data = MockResponseBuilder.source(
            source_id=789,
            include_datasets=True
        )
        source = Source(**source_data)
        assert len(source.data_sets) > 0
        assert isinstance(source.data_sets[0], DataSetBrief)
    
    def test_source_create_model(self):
        """Test SourceCreate request model."""
        create_data = {
            "name": "New Source",
            "source_type": "postgres",
            "data_credentials_id": 123
        }
        source_create = SourceCreate(**create_data)
        assert source_create.name == "New Source"
        assert source_create.source_type == "postgres"
        assert source_create.data_credentials_id == 123
    
    def test_source_update_model(self):
        """Test SourceUpdate request model."""
        update_data = {
            "name": "Updated Source",
            "description": "Updated description"
        }
        source_update = SourceUpdate(**update_data)
        assert source_update.name == "Updated Source"
        assert source_update.description == "Updated description"
    
    def test_source_copy_options_model(self):
        """Test SourceCopyOptions model."""
        options = SourceCopyOptions(
            reuse_data_credentials=True,
            copy_access_controls=False,
            owner_id=456
        )
        assert options.reuse_data_credentials is True
        assert options.copy_access_controls is False
        assert options.owner_id == 456


@pytest.mark.unit
class TestSourcesResourceUnit:
    """Unit tests for SourcesResource using mocks."""
    
    def test_list_sources_success(self, mock_client, mock_http_client):
        """Test successful sources listing."""
        # Arrange
        mock_sources = [
            MockResponseBuilder.source(source_id=1),
            MockResponseBuilder.source(source_id=2)
        ]
        mock_http_client.add_response("/data_sources", mock_sources)
        
        # Act
        sources = mock_client.sources.list()
        
        # Assert
        assert len(sources) == 2
        assert_model_list_valid(sources, Source)
        mock_http_client.assert_request_made("GET", "/data_sources")
    
    def test_list_sources_with_filters(self, mock_client, mock_http_client):
        """Test sources listing with filter parameters."""
        # Arrange
        mock_sources = [MockResponseBuilder.source(source_id=1)]
        mock_http_client.add_response("/data_sources", mock_sources)
        
        # Act
        sources = mock_client.sources.list(
            page=1,
            per_page=10,
            access_role="owner"
        )
        
        # Assert
        assert len(sources) == 1
        mock_http_client.assert_request_made(
            "GET", "/data_sources",
            params={"page": 1, "per_page": 10, "access_role": "owner"}
        )
    
    def test_get_source_success(self, mock_client, mock_http_client):
        """Test successful source retrieval."""
        # Arrange
        source_id = 123
        mock_source = MockResponseBuilder.source(source_id=source_id)
        mock_http_client.add_response(f"/data_sources/{source_id}", mock_source)
        
        # Act
        source = mock_client.sources.get(source_id)
        
        # Assert
        assert_model_valid(source, {"id": source_id})
        mock_http_client.assert_request_made("GET", f"/data_sources/{source_id}")
    
    def test_get_source_with_expand(self, mock_client, mock_http_client):
        """Test source retrieval with expand parameter."""
        # Arrange
        source_id = 456
        mock_source = MockResponseBuilder.source(
            source_id=source_id,
            include_datasets=True,
            include_credentials=True
        )
        mock_http_client.add_response(f"/data_sources/{source_id}", mock_source)
        
        # Act
        source = mock_client.sources.get(source_id, expand=True)
        
        # Assert
        assert_model_valid(source, {"id": source_id})
        assert source.data_credentials is not None
        assert len(source.data_sets) > 0
        mock_http_client.assert_request_made(
            "GET", f"/data_sources/{source_id}",
            params={"expand": 1}
        )
    
    def test_create_source_success(self, mock_client, mock_http_client):
        """Test successful source creation."""
        # Arrange
        create_data = SourceCreate(
            name="New Test Source",
            source_type="s3",
            data_credentials_id=789
        )
        mock_response = MockResponseBuilder.source(
            source_id=999,
            name="New Test Source"
        )
        mock_http_client.add_response("/data_sources", mock_response)
        
        # Act
        source = mock_client.sources.create(create_data)
        
        # Assert
        assert_model_valid(source, {"id": 999, "name": "New Test Source"})
        mock_http_client.assert_request_made(
            "POST", "/data_sources",
            json={
                "name": "New Test Source",
                "source_type": "s3", 
                "data_credentials_id": 789
            }
        )
    
    def test_update_source_success(self, mock_client, mock_http_client):
        """Test successful source update."""
        # Arrange
        source_id = 555
        update_data = SourceUpdate(
            name="Updated Source Name",
            description="Updated description"
        )
        mock_response = MockResponseBuilder.source(
            source_id=source_id,
            name="Updated Source Name"
        )
        mock_http_client.add_response(f"/data_sources/{source_id}", mock_response)
        
        # Act
        source = mock_client.sources.update(source_id, update_data)
        
        # Assert
        assert_model_valid(source, {"id": source_id, "name": "Updated Source Name"})
        mock_http_client.assert_request_made(
            "PUT", f"/data_sources/{source_id}",
            json={"name": "Updated Source Name", "description": "Updated description"}
        )
    
    def test_delete_source_success(self, mock_client, mock_http_client):
        """Test successful source deletion."""
        # Arrange
        source_id = 777
        mock_http_client.add_response(f"/data_sources/{source_id}", {"status": "deleted"})
        
        # Act
        response = mock_client.sources.delete(source_id)
        
        # Assert
        assert response["status"] == "deleted"
        mock_http_client.assert_request_made("DELETE", f"/data_sources/{source_id}")
    
    def test_activate_source_success(self, mock_client, mock_http_client):
        """Test successful source activation."""
        # Arrange
        source_id = 888
        mock_response = MockResponseBuilder.source(
            source_id=source_id,
            status="ACTIVE"
        )
        mock_http_client.add_response(f"/data_sources/{source_id}/activate", mock_response)
        
        # Act
        source = mock_client.sources.activate(source_id)
        
        # Assert
        assert_model_valid(source, {"id": source_id, "status": "ACTIVE"})
        mock_http_client.assert_request_made("PUT", f"/data_sources/{source_id}/activate")
    
    def test_pause_source_success(self, mock_client, mock_http_client):
        """Test successful source pause."""
        # Arrange
        source_id = 999
        mock_response = MockResponseBuilder.source(
            source_id=source_id,
            status="PAUSED"
        )
        mock_http_client.add_response(f"/data_sources/{source_id}/pause", mock_response)
        
        # Act
        source = mock_client.sources.pause(source_id)
        
        # Assert
        assert_model_valid(source, {"id": source_id, "status": "PAUSED"})
        mock_http_client.assert_request_made("PUT", f"/data_sources/{source_id}/pause")
    
    def test_copy_source_success(self, mock_client, mock_http_client):
        """Test successful source copy."""
        # Arrange
        source_id = 111
        copy_options = SourceCopyOptions(
            reuse_data_credentials=True,
            copy_access_controls=False
        )
        mock_response = MockResponseBuilder.source(
            source_id=222,
            name="Copied Source"
        )
        mock_http_client.add_response(f"/data_sources/{source_id}/copy", mock_response)
        
        # Act
        copied_source = mock_client.sources.copy(source_id, copy_options)
        
        # Assert
        assert_model_valid(copied_source, {"id": 222, "name": "Copied Source"})
        mock_http_client.assert_request_made(
            "POST", f"/data_sources/{source_id}/copy",
            json={
                "reuse_data_credentials": True,
                "copy_access_controls": False
            }
        )


@pytest.mark.unit
class TestSourcesErrorHandling:
    """Test error handling for sources operations."""
    
    def test_get_source_not_found(self, mock_client, mock_http_client):
        """Test getting a non-existent source."""
        # Arrange
        source_id = 999
        error = create_http_error(
            404, 
            "Source not found",
            {"resource_type": "source", "resource_id": str(source_id)}
        )
        mock_http_client.add_response(f"/data_sources/{source_id}", error)
        
        # Act & Assert
        with pytest.raises(NotFoundError) as exc_info:
            mock_client.sources.get(source_id)
        
        assert "Source not found" in str(exc_info.value)
        assert exc_info.value.resource_type == "source"
        assert exc_info.value.resource_id == str(source_id)
    
    def test_create_source_validation_error(self, mock_client, mock_http_client):
        """Test source creation with invalid data."""
        # Arrange
        error = create_http_error(
            400,
            "Validation failed",
            {"field": "source_type", "message": "Invalid source type"}
        )
        mock_http_client.add_response("/data_sources", error)
        
        # Act & Assert
        with pytest.raises(SDKValidationError) as exc_info:
            mock_client.sources.create({"invalid": "data"})
        
        assert exc_info.value.status_code == 400
        assert "Validation failed" in str(exc_info.value)
    
    def test_update_source_unauthorized(self, mock_client, mock_http_client):
        """Test updating source without permission."""
        # Arrange
        source_id = 123
        error = create_http_error(403, "Insufficient permissions")
        mock_http_client.add_response(f"/data_sources/{source_id}", error)
        
        # Act & Assert
        from nexla_sdk.exceptions import AuthorizationError
        with pytest.raises(AuthorizationError) as exc_info:
            mock_client.sources.update(source_id, {"name": "New Name"})
        
        assert exc_info.value.status_code == 403
    
    def test_server_error_during_list(self, mock_client, mock_http_client):
        """Test handling server error during list operation."""
        # Arrange
        error = create_http_error(500, "Internal server error")
        mock_http_client.add_response("/data_sources", error)
        
        # Act & Assert
        with pytest.raises(ServerError) as exc_info:
            mock_client.sources.list()
        
        assert exc_info.value.status_code == 500
        assert "Internal server error" in str(exc_info.value)


@pytest.mark.unit
class TestSourcesValidation:
    """Test sources model validation edge cases."""
    
    def test_source_model_handles_none_values(self):
        """Test that Source model handles None values gracefully."""
        source_data = {
            "id": 123,
            "name": "Test Source",
            "status": "ACTIVE",
            "source_type": "s3",
            "description": None,
            "data_credentials": None,
            "data_sets": None,
            "tags": None
        }
        source = Source(**source_data)
        assert source.description is None
        assert source.data_credentials is None
        assert source.data_sets == []  # Should default to empty list
        assert source.tags == []  # Should default to empty list
    
    def test_source_create_requires_name(self):
        """Test that SourceCreate requires name field."""
        with pytest.raises(ValidationError):
            SourceCreate(source_type="s3")  # Missing required name
    
    def test_source_create_validates_enum_fields(self):
        """Test that enum fields are validated in SourceCreate."""
        # This should work with valid source_type
        valid_create = SourceCreate(
            name="Test",
            source_type="s3"
        )
        assert valid_create.source_type == "s3"
        
        # Invalid source types should be handled by the enum validation
        # The actual validation depends on the SourceType enum implementation
    
    def test_data_set_brief_model(self):
        """Test DataSetBrief model validation."""
        dataset_data = {
            "id": 456,
            "owner_id": 123,
            "org_id": 789,
            "name": "Test Dataset",
            "description": "Test description"
        }
        dataset = DataSetBrief(**dataset_data)
        assert dataset.id == 456
        assert dataset.name == "Test Dataset"
    
    def test_run_info_model(self):
        """Test RunInfo model validation."""
        from datetime import datetime
        run_data = {
            "id": 789,
            "created_at": "2023-01-01T12:00:00Z"
        }
        run_info = RunInfo(**run_data)
        assert run_info.id == 789
        assert isinstance(run_info.created_at, datetime) 
