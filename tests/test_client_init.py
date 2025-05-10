import pytest
from pydantic import BaseModel

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaClientError, NexlaValidationError

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


def test_client_initialization_with_service_key():
    client = NexlaClient(
        service_key="test_service_key", api_url="http://localhost:8000", api_version="v1"
    )
    assert client.service_key == "test_service_key"
    assert client.api_url == "http://localhost:8000"
    assert client.api_version == "v1"


def test_client_initialization_defaults():
    client = NexlaClient(service_key="test_service_key")
    assert client.service_key == "test_service_key"
    assert client.api_url == "https://dataops.nexla.io/nexla-api"  # Default URL
    assert client.api_version == "v1"  # Default version


def test_client_api_url_strips_trailing_slash():
    client = NexlaClient(service_key="test_service_key", api_url="http://localhost:8000/")
    assert client.api_url == "http://localhost:8000"


class DummyModel(BaseModel):
    id: int
    name: str


def test_convert_to_model_single_item():
    client = NexlaClient(service_key="dummy_service_key")
    data = {"id": 1, "name": "Test"}
    model_instance = client._convert_to_model(data, DummyModel)
    assert isinstance(model_instance, DummyModel)
    assert model_instance.id == 1
    assert model_instance.name == "Test"


def test_convert_to_model_list_of_items():
    client = NexlaClient(service_key="dummy_service_key")
    data = [{"id": 1, "name": "Test1"}, {"id": 2, "name": "Test2"}]
    model_instances = client._convert_to_model(data, DummyModel)
    assert isinstance(model_instances, list)
    assert len(model_instances) == 2
    assert isinstance(model_instances[0], DummyModel)
    assert model_instances[0].name == "Test1"
    assert isinstance(model_instances[1], DummyModel)
    assert model_instances[1].name == "Test2"


def test_convert_to_model_validation_error():
    client = NexlaClient(service_key="dummy_service_key")
    data = {"id": "not_an_int", "name": "Test"}
    with pytest.raises(NexlaValidationError):
        client._convert_to_model(data, DummyModel)


def test_convert_to_model_list_validation_error():
    client = NexlaClient(service_key="dummy_service_key")
    data = [{"id": 1, "name": "Test1"}, {"id": "not_an_int", "name": "Test2"}]
    with pytest.raises(NexlaValidationError):
        client._convert_to_model(data, DummyModel)
