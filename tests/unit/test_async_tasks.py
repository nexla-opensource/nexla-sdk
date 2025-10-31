import pytest

from nexla_sdk import NexlaClient
from nexla_sdk.models.async_tasks.requests import AsyncTaskCreate
from nexla_sdk.models.async_tasks.responses import AsyncTask, DownloadLink


pytestmark = pytest.mark.unit


@pytest.fixture
def client(mock_client: NexlaClient) -> NexlaClient:
    return mock_client


class TestAsyncTasksResource:
    def test_list_types_create_get_result_download_ack_and_filters(self, client, mock_http_client):
        mock_http_client.add_response("/async_tasks", [{"id": 1, "status": "QUEUED"}])
        tasks = client.async_tasks.list()
        assert isinstance(tasks[0], AsyncTask)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/async_tasks/types", ["BulkDeleteNotifications"]) 
        types = client.async_tasks.types()
        assert types[0] == "BulkDeleteNotifications"

        mock_http_client.clear_responses()
        mock_http_client.add_response("/async_tasks/explain_arguments/BulkDeleteNotifications", {"args": []})
        exp = client.async_tasks.explain_arguments("BulkDeleteNotifications")
        assert "args" in exp

        mock_http_client.clear_responses()
        payload = AsyncTaskCreate(type="BulkDeleteNotifications", arguments={"ids": [1, 2]})
        mock_http_client.add_response("/async_tasks", {"id": 5, "status": "QUEUED"})
        created = client.async_tasks.create(payload)
        assert isinstance(created, AsyncTask)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/async_tasks/of_type/BulkDeleteNotifications", [{"id": 5}])
        by_type = client.async_tasks.list_of_type("BulkDeleteNotifications")
        assert isinstance(by_type[0], AsyncTask)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/async_tasks/by_status/QUEUED", [{"id": 5}])
        by_status = client.async_tasks.list_by_status("QUEUED")
        assert isinstance(by_status[0], AsyncTask)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/async_tasks/5", {"id": 5, "status": "DONE"})
        get = client.async_tasks.get(5)
        assert isinstance(get, AsyncTask)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/async_tasks/5/result", {"data": []})
        res = client.async_tasks.result(5)
        assert isinstance(res, dict)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/async_tasks/5/download_link", "https://url")
        link1 = client.async_tasks.download_link(5)
        assert isinstance(link1, str)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/async_tasks/5/download_link", {"url": "https://url"})
        link2 = client.async_tasks.download_link(5)
        assert isinstance(link2, DownloadLink)

        mock_http_client.clear_responses()
        mock_http_client.add_response("/async_tasks/5/acknowledge", {"status": "ok"})
        ack = client.async_tasks.acknowledge(5)
        assert ack.get("status") == "ok"

        mock_http_client.clear_responses()
        mock_http_client.add_response("/async_tasks/5", {"status": "deleted"})
        deleted = client.async_tasks.delete(5)
        assert deleted.get("status") == "deleted"

