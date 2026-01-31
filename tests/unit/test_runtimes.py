import pytest

from nexla_sdk import NexlaClient
from nexla_sdk.models.runtimes.requests import RuntimeCreate, RuntimeUpdate
from nexla_sdk.models.runtimes.responses import Runtime

pytestmark = pytest.mark.unit


@pytest.fixture
def client(mock_client: NexlaClient) -> NexlaClient:
    return mock_client


class TestRuntimesResource:
    def test_crud_and_state(self, client, mock_http_client):
        mock_http_client.add_response("/runtimes", [{"id": 1, "name": "rt"}])
        lst = client.runtimes.list()
        assert isinstance(lst[0], Runtime)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/runtimes", {"id": 2, "name": "rt"})
        created = client.runtimes.create(RuntimeCreate(name="rt"))
        assert isinstance(created, Runtime)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/runtimes/2", {"id": 2, "name": "rt"})
        got = client.runtimes.get(2)
        assert isinstance(got, Runtime)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/runtimes/2", {"id": 2, "name": "rt2"})
        upd = client.runtimes.update(2, RuntimeUpdate(name="rt2"))
        assert isinstance(upd, Runtime)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/runtimes/2/activate", {"id": 2, "name": "rt2"})
        act = client.runtimes.activate(2)
        assert isinstance(act, Runtime)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/runtimes/2/pause", {"id": 2, "name": "rt2"})
        ps = client.runtimes.pause(2)
        assert isinstance(ps, Runtime)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/runtimes/2", {"status": "deleted"})
        d = client.runtimes.delete(2)
        assert d.get("status") == "deleted"
