"""Unit tests for flows resource."""
import pytest
from unittest.mock import MagicMock
from typing import List

from nexla_sdk import NexlaClient
from nexla_sdk.models.flows.responses import FlowResponse, FlowMetrics
from nexla_sdk.models.flows.requests import FlowCopyOptions
from nexla_sdk.models.common import FlowNode
from nexla_sdk.exceptions import NexlaError, ServerError, ValidationError

from tests.utils.fixtures import MockHTTPClient, create_test_client, create_mock_response
from tests.utils.mock_builders import MockDataFactory
from tests.utils.assertions import NexlaAssertions


class TestFlowsUnit:
    """Unit tests for flows resource."""
    
    @pytest.fixture
    def mock_client(self) -> NexlaClient:
        """Create a test client with mocked HTTP."""
        return create_test_client()
    
    @pytest.fixture
    def mock_factory(self) -> MockDataFactory:
        """Create mock data factory."""
        return MockDataFactory()
    
    def test_list_flows(self, mock_client, mock_factory):
        """Test listing all flows."""
        # Arrange
        mock_response = mock_factory.create_mock_flow_response()
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flows = mock_client.flows.list()
        
        # Assert
        assert len(flows) == 1  # API returns single FlowResponse object for list
        assert isinstance(flows[0], FlowResponse)
        assert len(flows[0].flows) == len(mock_response["flows"])
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "GET", 
            f"{mock_client.api_url}/flows",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params={}
        )
    
    def test_list_flows_with_params(self, mock_client, mock_factory):
        """Test listing flows with query parameters."""
        # Arrange
        mock_response = mock_factory.create_mock_flow_response(include_elements=False)
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flows = mock_client.flows.list(flows_only=True, include_run_metrics=True)
        
        # Assert
        assert len(flows) == 1
        assert flows[0].data_sources is None  # No expanded elements
        
        # Verify request params
        _, _, kwargs = mock_client.http_client.request.mock_calls[0]
        assert kwargs["params"]["flows_only"] == 1
        assert kwargs["params"]["include_run_metrics"] == 1
    
    def test_get_flow(self, mock_client, mock_factory):
        """Test getting a single flow by ID."""
        # Arrange
        flow_id = 5059
        mock_response = mock_factory.create_mock_flow_response()
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flow = mock_client.flows.get(flow_id)
        
        # Assert
        assert isinstance(flow, FlowResponse)
        NexlaAssertions.assert_flow_response(flow, mock_response)
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "GET",
            f"{mock_client.api_url}/flows/{flow_id}",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params={}
        )
    
    def test_get_flow_by_resource(self, mock_client, mock_factory):
        """Test getting flow by resource type and ID."""
        # Arrange
        resource_type = "data_sources"
        resource_id = 5023
        mock_response = mock_factory.create_mock_flow_response()
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flow = mock_client.flows.get_by_resource(resource_type, resource_id)
        
        # Assert
        assert isinstance(flow, FlowResponse)
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "GET",
            f"{mock_client.api_url}/{resource_type}/{resource_id}/flow",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params={}
        )
    
    def test_activate_flow(self, mock_client, mock_factory):
        """Test activating a flow."""
        # Arrange
        flow_id = 5059
        mock_response = mock_factory.create_mock_flow_response()
        # Set all statuses to ACTIVE
        for flow in mock_response["flows"]:
            self._set_flow_status(flow, "ACTIVE")
        
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flow = mock_client.flows.activate(flow_id)
        
        # Assert
        assert isinstance(flow, FlowResponse)
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "PUT",
            f"{mock_client.api_url}/flows/{flow_id}/activate",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params={}
        )
    
    def test_activate_flow_all(self, mock_client, mock_factory):
        """Test activating entire flow tree."""
        # Arrange
        flow_id = 5059
        mock_response = mock_factory.create_mock_flow_response()
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flow = mock_client.flows.activate(flow_id, all=True)
        
        # Assert
        _, _, kwargs = mock_client.http_client.request.mock_calls[0]
        assert kwargs["params"]["all"] == 1
    
    def test_pause_flow(self, mock_client, mock_factory):
        """Test pausing a flow."""
        # Arrange
        flow_id = 5059
        mock_response = mock_factory.create_mock_flow_response()
        # Set all statuses to PAUSED
        for flow in mock_response["flows"]:
            self._set_flow_status(flow, "PAUSED")
        
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flow = mock_client.flows.pause(flow_id)
        
        # Assert
        assert isinstance(flow, FlowResponse)
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "PUT",
            f"{mock_client.api_url}/flows/{flow_id}/pause",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params={}
        )
    
    def test_copy_flow(self, mock_client, mock_factory):
        """Test copying a flow."""
        # Arrange
        flow_id = 5059
        copy_options = FlowCopyOptions(
            reuse_data_credentials=True,
            copy_access_controls=True,
            copy_dependent_data_flows=False,
            owner_id=123,
            org_id=456
        )
        mock_response = mock_factory.create_mock_flow_response()
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flow = mock_client.flows.copy(flow_id, copy_options)
        
        # Assert
        assert isinstance(flow, FlowResponse)
        
        # Verify request
        mock_client.http_client.request.assert_called_once()
        args, kwargs = mock_client.http_client.request.call_args
        assert args[0] == "POST"
        assert f"flows/{flow_id}/copy" in args[1]
        assert kwargs["json"]["reuse_data_credentials"] is True
        assert kwargs["json"]["copy_access_controls"] is True
        assert kwargs["json"]["owner_id"] == 123
    
    def test_delete_flow(self, mock_client):
        """Test deleting a flow."""
        # Arrange
        flow_id = 5059
        mock_response = {"status": "ok"}
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        result = mock_client.flows.delete(flow_id)
        
        # Assert
        assert result == mock_response
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "DELETE",
            f"{mock_client.api_url}/flows/{flow_id}",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            }
        )
    
    def test_delete_flow_active_error(self, mock_client):
        """Test deleting active flow returns error."""
        # Arrange
        flow_id = 5059
        error_response = {
            "data_sources": [5023],
            "data_sets": [5059, 5061, 5062],
            "message": "Active flow resources must be paused before flow deletion!"
        }
        
        # Mock the HTTP client to raise HttpClientError (which will be converted to ServerError)
        from nexla_sdk.http_client import HttpClientError
        mock_client.http_client.request = MagicMock(
            side_effect=HttpClientError(
                "Method not allowed",
                status_code=405,
                response=error_response
            )
        )
        
        # Act & Assert
        with pytest.raises(ServerError) as exc_info:
            mock_client.flows.delete(flow_id)
        
        assert exc_info.value.status_code == 405
        assert "Active flow resources must be paused" in str(exc_info.value)
    
    def test_delete_by_resource(self, mock_client):
        """Test deleting flow by resource."""
        # Arrange
        resource_type = "data_sources"
        resource_id = 5023
        mock_response = {"status": "ok"}
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        result = mock_client.flows.delete_by_resource(resource_type, resource_id)
        
        # Assert
        assert result == mock_response
        
        # Verify request
        mock_client.http_client.request.assert_called_once_with(
            "DELETE",
            f"{mock_client.api_url}/{resource_type}/{resource_id}/flow",
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            }
        )
    
    def test_activate_by_resource(self, mock_client, mock_factory):
        """Test activating flow by resource."""
        # Arrange
        resource_type = "data_sets"
        resource_id = 5061
        mock_response = mock_factory.create_mock_flow_response()
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flow = mock_client.flows.activate_by_resource(resource_type, resource_id, all=True)
        
        # Assert
        assert isinstance(flow, FlowResponse)
        
        # Verify request
        mock_client.http_client.request.assert_called_once()
        args, kwargs = mock_client.http_client.request.call_args
        assert args[0] == "PUT"
        assert f"{resource_type}/{resource_id}/activate" in args[1]
        assert kwargs["params"]["all"] == 1
    
    def test_pause_by_resource(self, mock_client, mock_factory):
        """Test pausing flow by resource."""
        # Arrange
        resource_type = "data_sinks"
        resource_id = 5029
        mock_response = mock_factory.create_mock_flow_response()
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flow = mock_client.flows.pause_by_resource(resource_type, resource_id)
        
        # Assert
        assert isinstance(flow, FlowResponse)
        
        # Verify request
        mock_client.http_client.request.assert_called_once()
        args, _ = mock_client.http_client.request.call_args
        assert args[0] == "PUT"
        assert f"{resource_type}/{resource_id}/pause" in args[1]
    
    def test_flow_with_metrics(self, mock_client, mock_factory):
        """Test flow response with metrics."""
        # Arrange
        mock_response = mock_factory.create_mock_flow_response()
        mock_response["metrics"] = [
            mock_factory.create_mock_flow_metrics() for _ in range(3)
        ]
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flows = mock_client.flows.list(include_run_metrics=True)
        
        # Assert
        assert len(flows) == 1
        flow = flows[0]
        assert flow.metrics is not None
        assert len(flow.metrics) == 3
        assert all(isinstance(m, FlowMetrics) for m in flow.metrics)
    
    def test_flow_node_parsing(self, mock_client, mock_factory):
        """Test parsing of nested flow node structure."""
        # Arrange
        # Create a deep flow structure
        mock_response = {
            "flows": [
                mock_factory.create_mock_flow_node(max_depth=4)
            ]
        }
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flows = mock_client.flows.list(flows_only=True)
        
        # Assert
        assert len(flows) == 1
        flow = flows[0]
        assert len(flow.flows) == 1
        
        # Check nested structure
        root_node = flow.flows[0]
        assert isinstance(root_node, FlowNode)
        assert root_node.parent_node_id is None  # Root node
        
        # Verify children exist and are properly parsed
        if root_node.children:
            for child in root_node.children:
                assert isinstance(child, FlowNode)
                assert child.parent_node_id == root_node.id
    
    def test_empty_flow_response(self, mock_client):
        """Test handling empty flow response."""
        # Arrange
        mock_response = {"flows": []}
        mock_client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flows = mock_client.flows.list()
        
        # Assert
        assert len(flows) == 1
        assert len(flows[0].flows) == 0
    
    def test_validation_error_handling(self, mock_client):
        """Test handling of invalid flow response."""
        # Arrange
        invalid_response = {
            "flows": [
                {
                    # Missing required 'id' field
                    "parent_data_set_id": None,
                    "data_source": {"id": 123}
                }
            ]
        }
        mock_client.http_client.request = MagicMock(return_value=invalid_response)
        
        # Act & Assert
        from pydantic import ValidationError
        with pytest.raises(ValidationError) as exc_info:
            mock_client.flows.list()
        
        # Check that the error mentions the missing fields
        error_str = str(exc_info.value)
        assert "id" in error_str
        assert "Field required" in error_str
    
    # Helper methods
    def _set_flow_status(self, flow_node: dict, status: str) -> None:
        """Recursively set status on flow nodes."""
        # This would typically update the data source/sink statuses
        # For unit tests, we're just demonstrating the concept
        if flow_node.get("children"):
            for child in flow_node["children"]:
                self._set_flow_status(child, status) 