import pytest

from nexla_sdk import NexlaClient
from nexla_sdk.models.attribute_transforms.requests import (
    AttributeTransformCreate,
    AttributeTransformUpdate,
)
from nexla_sdk.models.attribute_transforms.responses import AttributeTransform

pytestmark = pytest.mark.unit


@pytest.fixture
def client(mock_client: NexlaClient) -> NexlaClient:
    return mock_client


class TestAttributeTransformsResource:
    def test_list_public_get_crud(self, client, mock_http_client):
        mock_http_client.add_response(
            "/attribute_transforms", [{"id": 20, "name": "at"}]
        )
        out = client.attribute_transforms.list()
        assert isinstance(out[0], AttributeTransform)

        mock_http_client.clear_responses()
        mock_http_client.add_response(
            "/attribute_transforms/public", [{"id": 21, "name": "ap"}]
        )
        pub = client.attribute_transforms.list_public()
        assert isinstance(pub[0], AttributeTransform)

        mock_http_client.clear_responses()
        mock_http_client.add_response(
            "/attribute_transforms/20", {"id": 20, "name": "at"}
        )
        got = client.attribute_transforms.get(20)
        assert isinstance(got, AttributeTransform)

        mock_http_client.clear_responses()
        create = AttributeTransformCreate(
            name="at",
            output_type="json",
            code_type="python",
            code_encoding="utf-8",
            code="return x",
        )
        mock_http_client.add_response("/attribute_transforms", {"id": 22, "name": "at"})
        created = client.attribute_transforms.create(create)
        assert isinstance(created, AttributeTransform)

        mock_http_client.clear_responses()
        mock_http_client.add_response(
            "/attribute_transforms/22", {"id": 22, "name": "at2"}
        )
        upd = client.attribute_transforms.update(
            22, AttributeTransformUpdate(name="at2")
        )
        assert upd.name == "at2"

        mock_http_client.clear_responses()
        mock_http_client.add_response("/attribute_transforms/22", {"status": "deleted"})
        res = client.attribute_transforms.delete(22)
        assert res.get("status") == "deleted"
