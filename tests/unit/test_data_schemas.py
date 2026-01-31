import pytest

from nexla_sdk import NexlaClient
from nexla_sdk.models.common import LogEntry

pytestmark = pytest.mark.unit


@pytest.fixture
def client(mock_client: NexlaClient) -> NexlaClient:
    return mock_client


class TestDataSchemasResource:
    def test_audit_log(self, client, mock_http_client):
        log = {
            "id": 2,
            "item_type": "DATA_SCHEMA",
            "item_id": 9,
            "event": "created",
            "change_summary": ["created"],
            "object_changes": {},
            "request_ip": "127.0.0.1",
            "request_user_agent": "pytest",
            "request_url": "http://x",
            "user": {"id": 2},
            "org_id": 1,
            "owner_id": 1,
            "owner_email": "a@b.com",
            "created_at": "2023-01-01T00:00:00Z",
        }
        mock_http_client.add_response("/data_schemas/9/audit_log", [log])
        out = client.data_schemas.get_audit_log(9)
        assert isinstance(out[0], LogEntry)
        mock_http_client.assert_request_made("GET", "/data_schemas/9/audit_log")
