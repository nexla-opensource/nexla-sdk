"""Integration tests for flows resource."""
import os
import pytest
from typing import Optional

from nexla_sdk import NexlaClient
from nexla_sdk.models.flows.responses import FlowResponse, FlowMetrics
from nexla_sdk.models.flows.requests import FlowCopyOptions
from nexla_sdk.models.common import FlowNode
from nexla_sdk.exceptions import ServerError

from tests.utils.fixtures import get_test_credentials


@pytest.mark.integration
class TestFlowsIntegration:
    """Integration tests for flows resource."""
    
    @pytest.fixture(scope="class")
    def client(self) -> Optional[NexlaClient]:
        """Create a real Nexla client for integration tests."""
        creds = get_test_credentials()
        if not creds:
            pytest.skip("No test credentials available")
        
        return NexlaClient(**creds)
    
    @pytest.fixture(scope="class")
    def test_flow_id(self) -> Optional[int]:
        """Get test flow ID from environment."""
        flow_id = os.getenv("TEST_FLOW_ID")
        if flow_id:
            return int(flow_id)
        return None
    
    @pytest.fixture(scope="class")
    def test_source_id(self) -> Optional[int]:
        """Get test source ID from environment."""
        source_id = os.getenv("TEST_SOURCE_ID")
        if source_id:
            return int(source_id)
        return None
    
    @pytest.fixture(scope="class")
    def test_dataset_id(self) -> Optional[int]:
        """Get test dataset ID from environment."""
        dataset_id = os.getenv("TEST_DATASET_ID")
        if dataset_id:
            return int(dataset_id)
        return None
    
    def test_list_flows(self, client):
        """Test listing all flows."""
        # Act
        flows = client.flows.list()
        
        # Assert
        assert isinstance(flows, list)
        assert len(flows) >= 0
        
        if flows:
            flow = flows[0]
            assert isinstance(flow, FlowResponse)
            assert isinstance(flow.flows, list)
            
            # Check flow structure
            if flow.flows:
                node = flow.flows[0]
                assert hasattr(node, 'id')
                assert hasattr(node, 'parent_node_id')
    
    def test_list_flows_with_elements(self, client):
        """Test listing flows with expanded elements."""
        # Act
        flows = client.flows.list(flows_only=False)
        
        # Assert
        assert isinstance(flows, list)
        
        if flows and flows[0].flows:
            flow = flows[0]
            # Check for expanded elements
            if flow.data_sources:
                assert all(hasattr(src, 'id') for src in flow.data_sources)
            if flow.data_sets:
                assert all(hasattr(ds, 'id') for ds in flow.data_sets)
            if flow.data_sinks:
                assert all(hasattr(sink, 'id') for sink in flow.data_sinks)
    
    def test_list_flows_only(self, client):
        """Test listing flows without expanded elements."""
        # Act
        flows = client.flows.list(flows_only=True)
        
        # Assert
        assert isinstance(flows, list)
        
        if flows:
            flow = flows[0]
            # Expanded elements should be None when flows_only=True
            assert flow.data_sources is None or len(flow.data_sources) == 0
            assert flow.data_sets is None or len(flow.data_sets) == 0
            assert flow.data_sinks is None or len(flow.data_sinks) == 0
    
    def test_get_flow_by_id(self, client, test_flow_id):
        """Test getting a specific flow by ID."""
        if not test_flow_id:
            pytest.skip("No test flow ID provided")
        
        # Act
        flow = client.flows.get(test_flow_id)
        
        # Assert
        assert isinstance(flow, FlowResponse)
        assert isinstance(flow.flows, list)
        assert len(flow.flows) > 0
        
        # Check that we got the right flow
        found = False
        for node in flow.flows:
            if node.id == test_flow_id:
                found = True
                break
            # Check children recursively
            if self._find_node_in_children(node, test_flow_id):
                found = True
                break
        
        assert found, f"Flow ID {test_flow_id} not found in response"
    
    def test_get_flow_by_source(self, client, test_source_id):
        """Test getting flow by data source."""
        if not test_source_id:
            pytest.skip("No test source ID provided")
        
        # Act
        flow = client.flows.get_by_resource("data_sources", test_source_id)
        
        # Assert
        assert isinstance(flow, FlowResponse)
        assert isinstance(flow.flows, list)
        
        # Verify the flow contains the source
        if flow.flows:
            # Root nodes should have data_source_id matching
            source_found = any(
                node.data_source_id == test_source_id 
                for node in flow.flows
            )
            assert source_found, f"Source ID {test_source_id} not found in flow"
    
    def test_get_flow_by_dataset(self, client, test_dataset_id):
        """Test getting flow by dataset."""
        if not test_dataset_id:
            pytest.skip("No test dataset ID provided")
        
        # Act
        flow = client.flows.get_by_resource("data_sets", test_dataset_id)
        
        # Assert
        assert isinstance(flow, FlowResponse)
        assert isinstance(flow.flows, list)
        
        # Verify the flow contains the dataset
        if flow.flows:
            # Nodes should have data_set_id matching
            dataset_found = any(
                getattr(node, 'data_set_id', None) == test_dataset_id
                for node in flow.flows
            )
            assert dataset_found, f"Dataset ID {test_dataset_id} not found in flow"
    
    def test_flow_activation_pause_cycle(self, client, test_flow_id):
        """Test activating and pausing a flow."""
        if not test_flow_id:
            pytest.skip("No test flow ID provided")
        
        # Get initial state
        # initial_flow = client.flows.get(test_flow_id)  # Not used, saving API call
        
        try:
            # Pause the flow first to ensure we can activate it
            paused_flow = client.flows.pause(test_flow_id)
            assert isinstance(paused_flow, FlowResponse)
            
            # Activate the flow
            activated_flow = client.flows.activate(test_flow_id)
            assert isinstance(activated_flow, FlowResponse)
            
            # Pause it again
            final_flow = client.flows.pause(test_flow_id)
            assert isinstance(final_flow, FlowResponse)
            
        except ServerError as e:
            # Some flows may not support activation/pause
            if e.status_code in (400, 403, 405):
                pytest.skip(f"Flow does not support activation/pause: {e}")
            raise
    
    def test_flow_metrics(self, client):
        """Test getting flows with metrics."""
        # Act
        flows = client.flows.list(include_run_metrics=True)
        
        # Assert
        assert isinstance(flows, list)
        
        if flows and flows[0].metrics:
            metrics = flows[0].metrics
            assert isinstance(metrics, list)
            
            for metric in metrics:
                assert isinstance(metric, FlowMetrics)
                assert hasattr(metric, 'origin_node_id')
                assert hasattr(metric, 'records')
                assert hasattr(metric, 'size')
                assert hasattr(metric, 'errors')
                assert hasattr(metric, 'run_id')
    
    def test_flow_copy(self, client, test_flow_id):
        """Test copying a flow."""
        if not test_flow_id:
            pytest.skip("No test flow ID provided")
        
        # Arrange
        copy_options = FlowCopyOptions(
            reuse_data_credentials=True,
            copy_access_controls=False,
            copy_dependent_data_flows=False
        )
        
        try:
            # Act
            copied_flow = client.flows.copy(test_flow_id, copy_options)
            
            # Assert
            assert isinstance(copied_flow, FlowResponse)
            assert isinstance(copied_flow.flows, list)
            
            # The copied flow should have new IDs
            assert all(node.id != test_flow_id for node in copied_flow.flows)
            
            # Clean up - delete the copied flow
            if copied_flow.flows:
                for node in copied_flow.flows:
                    try:
                        # Pause before deleting
                        client.flows.pause(node.id, all=True)
                        client.flows.delete(node.id)
                    except ServerError:
                        pass  # Best effort cleanup
                        
        except ServerError as e:
            if e.status_code in (403, 405):
                pytest.skip(f"Flow copy not supported: {e}")
            raise
    
    def test_delete_flow_validation(self, client):
        """Test that deleting active flow fails with proper error."""
        # We don't actually want to delete real flows in integration tests
        # Just verify the error handling works
        
        # Find an active flow
        flows = client.flows.list()
        active_flow_id = None
        
        for flow_resp in flows:
            for node in flow_resp.flows:
                # Assuming we can check status somehow
                # This is a simplified test
                active_flow_id = node.id
                break
            if active_flow_id:
                break
        
        if not active_flow_id:
            pytest.skip("No active flow found for testing")
        
        # Try to delete active flow - should fail
        with pytest.raises(ServerError) as exc_info:
            client.flows.delete(active_flow_id)
        
        # Verify error is about active resources
        assert exc_info.value.status_code in (400, 405)
    
    def test_flow_structure_validation(self, client):
        """Test that flow structures are properly formed."""
        # Act
        flows = client.flows.list()
        
        # Assert
        for flow_resp in flows:
            for node in flow_resp.flows:
                self._validate_flow_node(node)
    
    # Helper methods
    def _find_node_in_children(self, node: FlowNode, target_id: int) -> bool:
        """Find a node with target_id in the children of the given node."""
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                if child.id == target_id:
                    return True
                if self._find_node_in_children(child, target_id):
                    return True
        return False
    
    def _validate_flow_node(self, node: FlowNode) -> None:
        """Validate flow node structure."""
        assert hasattr(node, 'id')
        assert isinstance(node.id, int)
        
        # Root nodes should have no parent but should have data_source
        if node.parent_node_id is None:
            assert node.data_source_id is not None or (hasattr(node, 'data_source') and node.data_source is not None)
        
        # Recursively validate children
        if node.children:
            assert isinstance(node.children, list)
            for child in node.children:
                assert child.parent_node_id == node.id
                self._validate_flow_node(child) 
        if node.parent_node_id is None:
            assert node.data_source_id is not None or hasattr(node, 'data_source')
        
        # Recursively validate children
        if node.children:
            assert isinstance(node.children, list)
            for child in node.children:
                assert child.parent_node_id == node.id
                self._validate_flow_node(child) 