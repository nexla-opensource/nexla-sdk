import pytest

from nexla_sdk import NexlaClient
from nexla_sdk.models.transforms.requests import TransformCreate, TransformUpdate
from nexla_sdk.models.transforms.responses import Transform, TransformCodeOp

pytestmark = pytest.mark.unit


@pytest.fixture
def client(mock_client: NexlaClient) -> NexlaClient:
    return mock_client


class TestTransformsResource:
    def test_list_public_get_crud_copy(self, client, mock_http_client):
        mock_http_client.add_response("/transforms", [{"id": 10, "name": "t"}])
        out = client.transforms.list()
        assert isinstance(out[0], Transform)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/transforms/public", [{"id": 11, "name": "tp"}])
        pub = client.transforms.list_public()
        assert isinstance(pub[0], Transform)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/transforms/10", {"id": 10, "name": "t"})
        got = client.transforms.get(10)
        assert isinstance(got, Transform)

        mock_http_client.clear_responses()
        create = TransformCreate(
            name="t",
            output_type="json",
            code_type="python",
            code_encoding="utf-8",
            code=[TransformCodeOp(operation="map", spec={})],
        )
        mock_http_client.add_response("/transforms", {"id": 12, "name": "t"})
        created = client.transforms.create(create)
        assert isinstance(created, Transform)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/transforms/12", {"id": 12, "name": "t2"})
        upd = client.transforms.update(12, TransformUpdate(name="t2"))
        assert upd.name == "t2"

        mock_http_client.clear_responses()
        mock_http_client.add_response(
            "/transforms/12/copy", {"id": 13, "name": "t-copy"}
        )
        cp = client.transforms.copy(12)
        assert isinstance(cp, Transform)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/transforms/13", {"status": "deleted"})
        res = client.transforms.delete(13)
        assert res.get("status") == "deleted"
