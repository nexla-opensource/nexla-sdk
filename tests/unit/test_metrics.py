import pytest

from nexla_sdk import NexlaClient
from nexla_sdk.models.metrics.enums import ResourceType
from nexla_sdk.models.metrics.responses import MetricsResponse, MetricsByRunResponse


pytestmark = pytest.mark.unit


@pytest.fixture
def client(mock_client: NexlaClient) -> NexlaClient:
    return mock_client


class TestMetricsResource:
    def test_resource_metrics_rate_limits_and_flow_helpers(self, client, mock_http_client):
        mock_http_client.queue_response({"status": 200, "metrics": []})
        m = client.metrics.get_resource_daily_metrics(ResourceType.DATA_SOURCES.value, 42, from_date="2024-01-01", to_date="2024-01-31")
        assert isinstance(m, MetricsResponse)
        mock_http_client.assert_request_made("GET", "/data_sources/42/metrics")

        mock_http_client.queue_response({"status": 200, "metrics": {"data": [], "meta": {}}})
        br = client.metrics.get_resource_metrics_by_run(ResourceType.DATA_SOURCES.value, 42, groupby="runId", orderby="lastWritten", page=1, size=10)
        assert isinstance(br, MetricsByRunResponse)
        mock_http_client.assert_request_made("GET", "/data_sources/42/metrics/run_summary")

        mock_http_client.clear_responses()
        mock_http_client.add_response("/limits", {"rate_limit": {"limit": 1000}})
        rl = client.metrics.get_rate_limits()
        assert "rate_limit" in rl

        mock_http_client.clear_responses()
        mock_http_client.add_response("/data_flows/data_sources/1/metrics", {"status": "ok"})
        fm = client.metrics.get_flow_metrics("data_sources", 1, from_date="2024-01-01", to_date="2024-01-31", groupby="runId", orderby="lastWritten", page=1, per_page=50)
        assert fm.get("status") == "ok"

        mock_http_client.clear_responses()
        mock_http_client.add_response("/data_flows/data_sources/1/logs", {"status": "ok"})
        fl = client.metrics.get_flow_logs("data_sources", 1, run_id=123, from_ts=1000, to_ts=2000, page=1, per_page=100)
        assert fl.get("status") == "ok"

