"""Property-based tests for flows resource."""
import pytest
from hypothesis import given, strategies as st, assume, settings
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, Bundle
from unittest.mock import MagicMock
from typing import Dict, List, Any, Optional

from nexla_sdk import NexlaClient
from nexla_sdk.models.flows.responses import FlowResponse, FlowMetrics
from nexla_sdk.models.flows.requests import FlowCopyOptions
from nexla_sdk.models.common import FlowNode
from nexla_sdk.exceptions import ValidationError

from tests.utils.fixtures import create_test_client
from tests.utils.mock_builders import MockDataFactory


# Strategies for flow-specific types
flow_status_strategy = st.sampled_from(["ACTIVE", "PAUSED", "DRAFT", "ERROR", "INIT"])
resource_type_strategy = st.sampled_from(["data_sources", "data_sets", "data_sinks"])


class TestFlowsProperty:
    """Property-based tests for flows resource."""
    
    @given(
        depth=st.integers(min_value=1, max_value=5),
        children_per_node=st.integers(min_value=0, max_value=3)
    )
    @settings(max_examples=50)
    def test_flow_node_structure_invariants(self, depth, children_per_node):
        """Test that flow node structures maintain invariants."""
        # Create a mock flow structure
        factory = MockDataFactory()
        
        def create_node_with_children(parent_id: Optional[int], current_depth: int) -> Dict[str, Any]:
            node_id = factory.fake.random_int(1, 10000)
            node = {
                "id": node_id,
                "parent_data_set_id": parent_id,
                "data_source": {"id": factory.fake.random_int(1, 10000)} if parent_id is None else None,
                "data_sinks": [],
                "sharers": {"sharers": [], "external_sharers": []},
                "children": []
            }
            
            if current_depth < depth:
                for _ in range(children_per_node):
                    child = create_node_with_children(node_id, current_depth + 1)
                    node["children"].append(child)
            else:
                # Leaf nodes might have sinks
                node["data_sinks"] = [factory.fake.random_int(1, 10000) for _ in range(factory.fake.random_int(0, 2))]
            
            return node
        
        # Create root node
        root = create_node_with_children(None, 1)
        
        # Validate invariants
        self._validate_node_invariants(root)
    
    def _validate_node_invariants(self, node: Dict[str, Any], parent_id: Optional[int] = None) -> None:
        """Validate flow node invariants."""
        # Every node must have an ID
        assert "id" in node
        assert isinstance(node["id"], int)
        assert node["id"] > 0
        
        # Parent relationship must be consistent
        assert node.get("parent_data_set_id") == parent_id
        
        # Root nodes (no parent) should have data source
        if parent_id is None:
            assert node.get("data_source") is not None
        
        # Children must be a list
        assert isinstance(node.get("children", []), list)
        
        # Recursively validate children
        for child in node.get("children", []):
            self._validate_node_invariants(child, node["id"])
    
    @given(
        include_elements=st.booleans(),
        num_flows=st.integers(min_value=0, max_value=5),
        include_metrics=st.booleans()
    )
    @settings(max_examples=50)
    def test_flow_response_parsing(self, include_elements, num_flows, include_metrics):
        """Test that flow responses are properly parsed regardless of structure."""
        # Arrange
        client = create_test_client()
        factory = MockDataFactory()
        
        # Create mock response
        mock_response = {
            "flows": [factory.create_mock_flow_node() for _ in range(num_flows)]
        }
        
        if include_elements:
            mock_response.update({
                "data_sources": [factory.create_mock_source() for _ in range(2)],
                "data_sets": [factory.create_mock_nexset() for _ in range(3)],
                "data_sinks": [factory.create_mock_destination() for _ in range(2)],
                "data_credentials": [factory.create_mock_credential() for _ in range(1)]
            })
        
        if include_metrics:
            mock_response["metrics"] = [factory.create_mock_flow_metrics() for _ in range(3)]
        
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        flows = client.flows.list()
        
        # Assert
        assert len(flows) == 1
        flow = flows[0]
        assert isinstance(flow, FlowResponse)
        assert len(flow.flows) == num_flows
        
        if include_elements:
            assert flow.data_sources is not None
            assert flow.data_sets is not None
            assert flow.data_sinks is not None
            assert flow.data_credentials is not None
        
        if include_metrics:
            assert flow.metrics is not None
            assert len(flow.metrics) == 3
    
    @given(
        reuse_credentials=st.booleans(),
        copy_access=st.booleans(),
        copy_dependent=st.booleans(),
        owner_id=st.one_of(st.none(), st.integers(min_value=1, max_value=10000)),
        org_id=st.one_of(st.none(), st.integers(min_value=1, max_value=10000))
    )
    def test_flow_copy_options_validation(self, reuse_credentials, copy_access, copy_dependent, owner_id, org_id):
        """Test that flow copy options are properly validated."""
        # Act & Assert - should not raise
        options = FlowCopyOptions(
            reuse_data_credentials=reuse_credentials,
            copy_access_controls=copy_access,
            copy_dependent_data_flows=copy_dependent,
            owner_id=owner_id,
            org_id=org_id
        )
        
        # Verify all fields are set correctly
        assert options.reuse_data_credentials == reuse_credentials
        assert options.copy_access_controls == copy_access
        assert options.copy_dependent_data_flows == copy_dependent
        assert options.owner_id == owner_id
        assert options.org_id == org_id
    
    @given(st.data())
    @settings(max_examples=20)
    def test_flow_api_parameter_combinations(self, data):
        """Test various API parameter combinations."""
        # Arrange
        client = create_test_client()
        factory = MockDataFactory()
        
        # Generate random parameters
        flows_only = data.draw(st.booleans())
        include_metrics = data.draw(st.booleans())
        page = data.draw(st.one_of(st.none(), st.integers(min_value=1, max_value=100)))
        per_page = data.draw(st.one_of(st.none(), st.integers(min_value=1, max_value=100)))
        
        # Create appropriate mock response
        mock_response = factory.create_mock_flow_response(include_elements=not flows_only)
        if include_metrics:
            mock_response["metrics"] = [factory.create_mock_flow_metrics()]
        
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Build kwargs
        kwargs = {}
        if flows_only:
            kwargs["flows_only"] = True
        if include_metrics:
            kwargs["include_run_metrics"] = True
        if page:
            kwargs["page"] = page
        if per_page:
            kwargs["per_page"] = per_page
        
        # Act
        flows = client.flows.list(**kwargs)
        
        # Assert
        assert len(flows) == 1
        assert isinstance(flows[0], FlowResponse)
        
        # Verify parameters were passed correctly
        _, _, call_kwargs = client.http_client.request.mock_calls[0]
        params = call_kwargs["params"]
        
        if flows_only:
            assert params.get("flows_only") == 1
        if include_metrics:
            assert params.get("include_run_metrics") == 1
        if page:
            assert params.get("page") == page
        if per_page:
            assert params.get("per_page") == per_page


class FlowStateMachine(RuleBasedStateMachine):
    """Stateful testing for flow operations."""
    
    def __init__(self):
        super().__init__()
        self.client = create_test_client()
        self.factory = MockDataFactory()
        self.flows = {}  # Track flows by ID
        self.flow_states = {}  # Track flow states
        
        # Setup default mock
        self.client.http_client.request = MagicMock()
    
    flows_bundle = Bundle('flows')
    
    @rule(target=flows_bundle)
    def create_flow(self):
        """Create a new flow (via list operation)."""
        # Generate a flow
        flow_id = self.factory.fake.random_int(1000, 9999)
        mock_response = self.factory.create_mock_flow_response()
        mock_response["flows"][0]["id"] = flow_id
        
        self.client.http_client.request.return_value = mock_response
        
        # List flows (simulating flow creation)
        flows = self.client.flows.list()
        
        # Track the flow
        self.flows[flow_id] = flows[0]
        self.flow_states[flow_id] = "ACTIVE"
        
        return flow_id
    
    @rule(flow_id=flows_bundle)
    def activate_flow(self, flow_id):
        """Activate a flow."""
        mock_response = self.factory.create_mock_flow_response()
        mock_response["flows"][0]["id"] = flow_id
        
        self.client.http_client.request.return_value = mock_response
        
        # Activate
        self.client.flows.activate(flow_id)
        self.flow_states[flow_id] = "ACTIVE"
    
    @rule(flow_id=flows_bundle)
    def pause_flow(self, flow_id):
        """Pause a flow."""
        mock_response = self.factory.create_mock_flow_response()
        mock_response["flows"][0]["id"] = flow_id
        
        self.client.http_client.request.return_value = mock_response
        
        # Pause
        self.client.flows.pause(flow_id)
        self.flow_states[flow_id] = "PAUSED"
    
    @rule(
        flow_id=flows_bundle,
        resource_type=resource_type_strategy,
        resource_id=st.integers(min_value=1, max_value=10000)
    )
    def get_flow_by_resource(self, flow_id, resource_type, resource_id):
        """Get flow by resource."""
        mock_response = self.factory.create_mock_flow_response()
        self.client.http_client.request.return_value = mock_response
        
        # Get by resource
        flow = self.client.flows.get_by_resource(resource_type, resource_id)
        assert isinstance(flow, FlowResponse)
    
    @invariant()
    def flow_states_consistent(self):
        """Check that flow states remain consistent."""
        # All tracked flows should have a state
        for flow_id in self.flows:
            assert flow_id in self.flow_states
            assert self.flow_states[flow_id] in ["ACTIVE", "PAUSED", "DRAFT", "ERROR"]


# Run the state machine tests
TestFlowStateMachine = FlowStateMachine.TestCase 