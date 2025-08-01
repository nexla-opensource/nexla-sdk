"""Property-based tests for nexsets resource."""
import os
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from unittest.mock import patch, MagicMock

from nexla_sdk import NexlaClient
from nexla_sdk.models.nexsets import Nexset, NexsetCreate, NexsetUpdate, NexsetSample
from tests.utils.fixtures import create_test_client
from tests.utils.mock_builders import MockResponseBuilder
from tests.utils.assertions import NexlaAssertions


# Suppress function-scoped fixture warnings for CI
SETTINGS = settings(
    suppress_health_check=[HealthCheck.function_scoped_fixture],
    max_examples=3 if os.getenv("CI") else 10,
    deadline=None
)


class TestNexsetsProperty:
    """Property-based tests for nexsets resource."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return create_test_client()

    @pytest.fixture
    def assertions(self):
        """Create assertions helper."""
        return NexlaAssertions()

    @given(
        nexset_name=st.text(min_size=1, max_size=100).filter(lambda x: x.strip()),
        nexset_description=st.one_of(st.none(), st.text(max_size=500)),
        parent_id=st.integers(min_value=1, max_value=99999)
    )
    @SETTINGS
    def test_create_nexset_serialization(self, client, nexset_name, nexset_description, parent_id):
        """Test nexset creation with various input combinations."""
        # Arrange
        create_data = NexsetCreate(
            name=nexset_name.strip(),
            description=nexset_description,
            parent_data_set_id=parent_id,
            has_custom_transform=True
        )
        
        mock_response = MockResponseBuilder.nexset({
            "name": nexset_name.strip(),
            "description": nexset_description,
            "parent_data_sets": [{"id": parent_id, "owner_id": 1, "org_id": 1}]
        })
        
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        nexset = client.nexsets.create(create_data)
        
        # Assert
        assert nexset.name == nexset_name.strip()
        assert nexset.description == nexset_description
        
        # Verify serialization
        serialized = create_data.to_dict()
        assert serialized["name"] == nexset_name.strip()
        assert serialized["parent_data_set_id"] == parent_id

    @given(
        response_data=st.fixed_dictionaries({
            "id": st.integers(min_value=1, max_value=999999),
            "name": st.one_of(st.none(), st.text(min_size=1, max_size=200)),
            "status": st.sampled_from(["ACTIVE", "PAUSED", "DRAFT", "PROCESSING", "ERROR"])
        })
    )
    @SETTINGS
    def test_nexset_response_parsing(self, client, assertions, response_data):
        """Test parsing nexset responses with various data combinations."""
        # Arrange
        mock_response = MockResponseBuilder.nexset(response_data)
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        nexset = client.nexsets.get(response_data["id"])
        
        # Assert
        assertions.assert_nexset_response(nexset)
        assert nexset.id == response_data["id"]
        assert nexset.status == response_data["status"]
        if response_data["name"]:
            assert nexset.name == response_data["name"]

    @given(
        nexsets_data=st.lists(
            st.fixed_dictionaries({
                "id": st.integers(min_value=1, max_value=999999),
                "name": st.one_of(st.none(), st.text(min_size=1, max_size=100)),
                "status": st.sampled_from(["ACTIVE", "PAUSED", "DRAFT"])
            }),
            min_size=0,
            max_size=10
        )
    )
    @SETTINGS
    def test_list_nexsets_response_parsing(self, client, assertions, nexsets_data):
        """Test parsing list responses with various data sizes."""
        # Arrange
        mock_response = [MockResponseBuilder.nexset(data) for data in nexsets_data]
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        nexsets = client.nexsets.list()
        
        # Assert
        assert len(nexsets) == len(nexsets_data)
        for i, nexset in enumerate(nexsets):
            assertions.assert_nexset_response(nexset)
            assert nexset.id == nexsets_data[i]["id"]

    @given(
        update_name=st.one_of(st.none(), st.text(min_size=1, max_size=100).filter(lambda x: x.strip())),
        update_description=st.one_of(st.none(), st.text(max_size=500)),
        tags=st.one_of(
            st.none(),
            st.lists(
                st.text(
                    min_size=1, 
                    max_size=30, 
                    alphabet=st.characters(min_codepoint=32, max_codepoint=126)
                ).filter(lambda x: x.strip()), 
                min_size=0, 
                max_size=5
            )
        )
    )
    @SETTINGS
    def test_update_nexset_with_various_data(self, client, update_name, update_description, tags):
        """Test updating nexsets with various field combinations."""
        # Arrange
        nexset_id = 1001
        update_data = NexsetUpdate(
            name=update_name.strip() if update_name else None,
            description=update_description,
            tags=tags
        )
        
        mock_response = MockResponseBuilder.nexset({
            "id": nexset_id,
            "name": update_name.strip() if update_name else "Existing Name",
            "description": update_description,
            "tags": tags or []
        })
        
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        nexset = client.nexsets.update(nexset_id, update_data)
        
        # Assert
        assert nexset.id == nexset_id
        if update_name:
            assert nexset.name == update_name.strip()
        if update_description is not None:
            assert nexset.description == update_description
        assert nexset.tags == (tags or [])

    @given(
        sample_data=st.fixed_dictionaries({
            "field1": st.text(min_size=1, max_size=50),
            "field2": st.integers(),
            "field3": st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False))
        })
    )
    @SETTINGS
    def test_nexset_samples_with_various_data(self, client, assertions, sample_data):
        """Test nexset samples with different data structures."""
        # Arrange
        nexset_id = 1001
        mock_sample = MockResponseBuilder.nexset_sample({
            "raw_message": sample_data
        })
        mock_response = [mock_sample]
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        samples = client.nexsets.get_samples(nexset_id, count=1)
        
        # Assert
        assert len(samples) == 1
        sample = samples[0]
        assertions.assert_nexset_sample(sample)
        assert sample.raw_message["field1"] == sample_data["field1"]
        assert sample.raw_message["field2"] == sample_data["field2"]

    @given(
        count=st.integers(min_value=1, max_value=100),
        include_metadata=st.booleans(),
        live=st.booleans()
    )
    @SETTINGS
    def test_get_samples_parameters(self, client, count, include_metadata, live):
        """Test get_samples with various parameter combinations."""
        # Arrange
        nexset_id = 1001
        mock_response = [MockResponseBuilder.nexset_sample() for _ in range(min(count, 5))]
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        client.nexsets.get_samples(nexset_id, count=count, include_metadata=include_metadata, live=live)
        
        # Assert
        expected_params = {
            'count': count,
            'include_metadata': include_metadata,
            'live': live
        }
        client.http_client.request.assert_called_once_with(
            'GET', 
            f'{client.api_url}/data_sets/{nexset_id}/samples',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            params=expected_params
        )

    @given(
        nexset_name=st.text(min_size=1, max_size=200),
        flow_type=st.one_of(st.none(), st.sampled_from(["batch", "streaming", "real_time"])),
        status=st.sampled_from(["ACTIVE", "PAUSED", "DRAFT", "PROCESSING"])
    )
    @SETTINGS
    def test_nexset_name_and_type_combinations(self, client, assertions, nexset_name, flow_type, status):
        """Test nexsets with various name and type combinations."""
        # Arrange
        mock_response = MockResponseBuilder.nexset({
            "name": nexset_name.strip(),
            "flow_type": flow_type,
            "status": status
        })
        
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        nexset = client.nexsets.get(1001)
        
        # Assert
        assertions.assert_nexset_response(nexset)
        assert nexset.name == nexset_name.strip()
        assert nexset.status == status
        if flow_type:
            assert nexset.flow_type == flow_type

    @given(
        copy_access_controls=st.booleans(),
        owner_id=st.one_of(st.none(), st.integers(min_value=1, max_value=9999)),
        org_id=st.one_of(st.none(), st.integers(min_value=1, max_value=999))
    )
    @SETTINGS
    def test_copy_options_serialization(self, client, copy_access_controls, owner_id, org_id):
        """Test copy options with various parameter combinations."""
        # Arrange
        nexset_id = 1001
        from nexla_sdk.models.nexsets import NexsetCopyOptions
        
        copy_options = NexsetCopyOptions(
            copy_access_controls=copy_access_controls,
            owner_id=owner_id,
            org_id=org_id
        )
        
        mock_response = MockResponseBuilder.nexset({
            "id": 1002,
            "copied_from_id": nexset_id
        })
        
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        client.nexsets.copy(nexset_id, copy_options)
        
        # Assert
        serialized = copy_options.to_dict()
        assert serialized["copy_access_controls"] == copy_access_controls
        assert serialized.get("owner_id") == owner_id
        assert serialized.get("org_id") == org_id
        
        client.http_client.request.assert_called_once_with(
            'POST', 
            f'{client.api_url}/data_sets/{nexset_id}/copy',
            headers={
                "Accept": "application/vnd.nexla.api.v1+json",
                "Content-Type": "application/json",
                "Authorization": "Bearer test-token"
            },
            json=serialized
        ) 