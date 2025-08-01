"""Property-based tests for destinations resource."""
import os
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from unittest.mock import MagicMock

from nexla_sdk import NexlaClient
from nexla_sdk.models.destinations import Destination, DestinationCreate, DestinationUpdate
from tests.utils.fixtures import create_test_client
from tests.utils.mock_builders import MockResponseBuilder
from tests.utils.assertions import NexlaAssertions


# Suppress function-scoped fixture warnings for CI
SETTINGS = settings(
    suppress_health_check=[HealthCheck.function_scoped_fixture],
    max_examples=3 if os.getenv("CI") else 10,
    deadline=None
)


class TestDestinationsProperty:
    """Property-based tests for destinations resource."""

    @pytest.fixture
    def client(self):
        """Create a test client with mocked HTTP."""
        return create_test_client()

    @pytest.fixture
    def assertions(self):
        """Create assertions helper."""
        return NexlaAssertions()

    @given(
        destination_name=st.text(min_size=1, max_size=100).filter(lambda x: x.strip()),
        destination_description=st.one_of(st.none(), st.text(max_size=500)),
        sink_type=st.sampled_from(["s3", "gcs", "mysql", "postgres", "snowflake", "bigquery", "kafka", "dropbox"])
    )
    @SETTINGS
    def test_create_destination_serialization(self, client, destination_name, destination_description, sink_type):
        """Test destination creation with various input combinations."""
        # Arrange
        create_data = DestinationCreate(
            name=destination_name.strip(),
            sink_type=sink_type,
            data_credentials_id=1,
            data_set_id=1,
            description=destination_description
        )
        
        mock_response = MockResponseBuilder.destination({
            "name": destination_name.strip(),
            "sink_type": sink_type,
            "description": destination_description
        })
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = client.destinations.create(create_data)
        
        # Assert
        assert destination.name == destination_name.strip()
        assert destination.sink_type == sink_type
        if destination_description:
            assert destination.description == destination_description

    @given(
        response_data=st.fixed_dictionaries({
            "id": st.integers(min_value=1, max_value=999999),
            "name": st.text(min_size=1, max_size=200),
            "sink_type": st.sampled_from(["s3", "gcs", "mysql", "postgres", "snowflake", "bigquery", "kafka"]),
            "status": st.sampled_from(["ACTIVE", "PAUSED", "DRAFT", "ERROR"])
        })
    )
    @SETTINGS
    def test_destination_response_parsing(self, client, assertions, response_data):
        """Test parsing destination responses with various data combinations."""
        # Arrange
        mock_response = MockResponseBuilder.destination(response_data)
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = client.destinations.get(response_data["id"])
        
        # Assert
        assertions.assert_destination_response(destination)
        assert destination.id == response_data["id"]
        assert destination.sink_type == response_data["sink_type"]
        assert destination.status == response_data["status"]

    @given(
        destinations_data=st.lists(
            st.fixed_dictionaries({
                "id": st.integers(min_value=1, max_value=999999),
                "name": st.text(min_size=1, max_size=100),
                "sink_type": st.sampled_from(["s3", "mysql", "bigquery"])
            }),
            min_size=0,
            max_size=5
        )
    )
    @SETTINGS
    def test_list_destinations_response_parsing(self, client, assertions, destinations_data):
        """Test parsing list destinations responses with various data combinations."""
        # Arrange
        mock_destinations = [MockResponseBuilder.destination(data) for data in destinations_data]
        client.http_client.request = MagicMock(return_value=mock_destinations)
        
        # Act
        destinations = client.destinations.list()
        
        # Assert
        assert len(destinations) == len(destinations_data)
        for i, destination in enumerate(destinations):
            assertions.assert_destination_response(destination)
            assert destination.id == destinations_data[i]["id"]
            assert destination.sink_type == destinations_data[i]["sink_type"]

    @given(
        name=st.one_of(st.none(), st.text(min_size=1, max_size=200).filter(lambda x: x.strip())),
        description=st.one_of(st.none(), st.text(max_size=500)),
        data_credentials_id=st.one_of(st.none(), st.integers(min_value=1, max_value=999999)),
        data_set_id=st.one_of(st.none(), st.integers(min_value=1, max_value=999999))
    )
    @SETTINGS
    def test_update_destination_with_various_data(self, client, assertions, name, description, data_credentials_id, data_set_id):
        """Test destination updates with various data combinations."""
        # Arrange
        destination_id = 12345
        update_data = DestinationUpdate(
            name=name,
            description=description,
            data_credentials_id=data_credentials_id,
            data_set_id=data_set_id
        )
        
        # Build expected response
        expected_response = {"id": destination_id}
        if name and name.strip():
            expected_response["name"] = name.strip()
        if description:
            expected_response["description"] = description
        if data_credentials_id:
            expected_response["data_credentials_id"] = data_credentials_id
        if data_set_id:
            expected_response["data_set_id"] = data_set_id
            
        mock_response = MockResponseBuilder.destination(expected_response)
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = client.destinations.update(destination_id, update_data)
        
        # Assert
        assertions.assert_destination_response(destination)
        assert destination.id == destination_id
        if name and name.strip():
            assert destination.name == name.strip()

    @given(
        sink_config_data=st.fixed_dictionaries({
            "data_format": st.sampled_from(["json", "csv", "parquet", "avro"]),
            "path": st.text(min_size=1, max_size=200),
            "mapping": st.fixed_dictionaries({
                "mode": st.sampled_from(["auto", "manual"]),
                "tracker_mode": st.just("NONE")
            })
        })
    )
    @SETTINGS 
    def test_destination_with_various_sink_configs(self, client, assertions, sink_config_data):
        """Test destinations with various sink configuration combinations."""
        # Arrange
        mock_response = MockResponseBuilder.destination({
            "id": 12345,
            "sink_config": sink_config_data
        })
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = client.destinations.get(12345)
        
        # Assert
        assertions.assert_destination_response(destination)
        if hasattr(destination, 'sink_config') and destination.sink_config:
            assert destination.sink_config["data_format"] == sink_config_data["data_format"]
            assert destination.sink_config["mapping"]["mode"] == sink_config_data["mapping"]["mode"]

    @given(
        destination_name=st.text(
            min_size=1, 
            max_size=255,
            alphabet=st.characters(min_codepoint=32, max_codepoint=126)
        ).filter(lambda x: x.strip()),
        sink_type=st.sampled_from(["s3", "mysql", "postgres", "snowflake"])
    )
    @SETTINGS
    def test_destination_name_edge_cases(self, client, assertions, destination_name, sink_type):
        """Test destination creation with various name edge cases."""
        # Arrange
        create_data = DestinationCreate(
            name=destination_name.strip(),
            sink_type=sink_type,
            data_credentials_id=1,
            data_set_id=1
        )
        
        mock_response = MockResponseBuilder.destination({
            "name": destination_name.strip(),
            "sink_type": sink_type
        })
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = client.destinations.create(create_data)
        
        # Assert
        assertions.assert_destination_response(destination)
        assert destination.name == destination_name.strip()
        assert destination.sink_type == sink_type

    @given(
        data_set_info=st.fixed_dictionaries({
            "id": st.integers(min_value=1, max_value=999999),
            "name": st.text(min_size=1, max_size=100),
            "status": st.sampled_from(["ACTIVE", "PAUSED", "DRAFT"])
        }),
        data_map_info=st.fixed_dictionaries({
            "id": st.integers(min_value=1, max_value=999999),
            "owner_id": st.integers(min_value=1, max_value=1000),
            "org_id": st.integers(min_value=1, max_value=100),
            "name": st.text(min_size=1, max_size=100),
            "description": st.text(min_size=1, max_size=200),
            "public": st.booleans(),
            "created_at": st.just("2023-01-01T12:00:00.000Z"),
            "updated_at": st.just("2023-01-01T12:00:00.000Z")
        })
    )
    @SETTINGS
    def test_destination_with_nested_objects(self, client, assertions, data_set_info, data_map_info):
        """Test destinations with various nested object combinations."""
        # Arrange
        mock_response = MockResponseBuilder.destination({
            "id": 12345,
            "data_set": data_set_info,
            "data_map": data_map_info
        })
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = client.destinations.get(12345)
        
        # Assert
        assertions.assert_destination_response(destination)
        if hasattr(destination, 'data_set') and destination.data_set:
            assert destination.data_set.id == data_set_info["id"]
            assert destination.data_set.status == data_set_info["status"]
        if hasattr(destination, 'data_map') and destination.data_map:
            assert destination.data_map.id == data_map_info["id"]
            assert destination.data_map.public == data_map_info["public"]

    @given(
        vendor_data=st.fixed_dictionaries({
            "id": st.integers(min_value=1, max_value=1000),
            "name": st.text(min_size=1, max_size=100),
            "type": st.text(min_size=1, max_size=50)
        }),
        vendor_endpoint=st.fixed_dictionaries({
            "id": st.integers(min_value=1, max_value=1000),
            "name": st.text(min_size=1, max_size=100),
            "url": st.text(min_size=10, max_size=200)
        })
    )
    @SETTINGS
    def test_destination_vendor_configuration(self, client, assertions, vendor_data, vendor_endpoint):
        """Test destinations with various vendor configurations."""
        # Arrange
        mock_response = MockResponseBuilder.destination({
            "id": 12345,
            "vendor": vendor_data,
            "vendor_endpoint": vendor_endpoint,
            "has_template": True
        })
        client.http_client.request = MagicMock(return_value=mock_response)
        
        # Act
        destination = client.destinations.get(12345)
        
        # Assert
        assertions.assert_destination_response(destination)
        if hasattr(destination, 'vendor') and destination.vendor:
            assert destination.vendor["id"] == vendor_data["id"]
            assert destination.vendor["name"] == vendor_data["name"]
        if hasattr(destination, 'vendor_endpoint') and destination.vendor_endpoint:
            assert destination.vendor_endpoint["id"] == vendor_endpoint["id"] 