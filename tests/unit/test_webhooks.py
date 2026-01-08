"""Unit tests for webhooks resource."""
import pytest
import base64
from unittest.mock import MagicMock

from nexla_sdk.resources.webhooks import WebhooksResource
from nexla_sdk.models.webhooks.requests import WebhookSendOptions
from nexla_sdk.models.webhooks.responses import WebhookResponse
from nexla_sdk.exceptions import NexlaError
from nexla_sdk.http_client import HttpClientError
from tests.utils.fixtures import MockHTTPClient
from tests.utils.mock_builders import MockResponseBuilder

pytestmark = pytest.mark.unit


class TestWebhooksResourceModels:
    """Tests for webhook models validation."""

    def test_webhook_send_options_model(self):
        """Test WebhookSendOptions model with all fields."""
        options = WebhookSendOptions(
            include_headers=True,
            include_url_params=True,
            force_schema_detection=True
        )
        assert options.include_headers is True
        assert options.include_url_params is True
        assert options.force_schema_detection is True

    def test_webhook_send_options_defaults(self):
        """Test WebhookSendOptions model defaults to None."""
        options = WebhookSendOptions()
        assert options.include_headers is None
        assert options.include_url_params is None
        assert options.force_schema_detection is None

    def test_webhook_response_model(self):
        """Test WebhookResponse model with all fields."""
        response = WebhookResponse(dataset_id=12345, processed=5)
        assert response.dataset_id == 12345
        assert response.processed == 5

    def test_webhook_response_handles_optional(self):
        """Test WebhookResponse model handles optional fields."""
        response = WebhookResponse()
        assert response.dataset_id is None
        assert response.processed is None


class TestWebhooksResourceUnit:
    """Unit tests for WebhooksResource core functionality."""

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        api_key = "test-api-key-123"
        webhooks = WebhooksResource(api_key=api_key)
        assert webhooks.api_key == api_key
        assert webhooks._http_client is None

    def test_init_with_http_client(self):
        """Test initialization with custom HTTP client."""
        api_key = "test-api-key-123"
        http_client = MockHTTPClient()
        webhooks = WebhooksResource(api_key=api_key, http_client=http_client)
        assert webhooks.api_key == api_key
        assert webhooks._http_client is http_client

    def test_send_one_record_success(self):
        """Test sending a single record successfully."""
        http_client = MockHTTPClient()
        mock_response = MockResponseBuilder.webhook_send_response(
            dataset_id=12345, processed=1
        )
        http_client.add_response("webhook", mock_response)

        webhooks = WebhooksResource(api_key="test-api-key", http_client=http_client)
        record = {"event": "page_view", "user_id": 123}

        response = webhooks.send_one_record(
            webhook_url="https://api.nexla.com/webhook/abc123",
            record=record
        )

        assert isinstance(response, WebhookResponse)
        assert response.dataset_id == 12345
        assert response.processed == 1

        # Verify request was made correctly
        last_request = http_client.get_last_request()
        assert last_request["method"] == "POST"
        assert "webhook/abc123" in last_request["url"]
        assert last_request["json"] == record
        assert last_request["params"]["api_key"] == "test-api-key"

    def test_send_one_record_with_options(self):
        """Test sending a single record with options."""
        http_client = MockHTTPClient()
        mock_response = MockResponseBuilder.webhook_send_response(processed=1)
        http_client.add_response("webhook", mock_response)

        webhooks = WebhooksResource(api_key="test-api-key", http_client=http_client)
        options = WebhookSendOptions(
            include_headers=True,
            include_url_params=True,
            force_schema_detection=True
        )

        response = webhooks.send_one_record(
            webhook_url="https://api.nexla.com/webhook/abc123",
            record={"event": "click"},
            options=options
        )

        assert isinstance(response, WebhookResponse)

        # Verify options were passed as query params
        last_request = http_client.get_last_request()
        assert last_request["params"]["include_headers"] == "true"
        assert last_request["params"]["include_url_params"] == "true"
        assert last_request["params"]["force_schema_detection"] == "true"

    def test_send_one_record_query_auth(self):
        """Test that query auth method passes api_key in query params."""
        http_client = MockHTTPClient()
        mock_response = MockResponseBuilder.webhook_send_response()
        http_client.add_response("webhook", mock_response)

        webhooks = WebhooksResource(api_key="my-secret-key", http_client=http_client)

        webhooks.send_one_record(
            webhook_url="https://api.nexla.com/webhook/abc123",
            record={"data": "test"},
            auth_method="query"
        )

        last_request = http_client.get_last_request()
        assert last_request["params"]["api_key"] == "my-secret-key"
        assert "Authorization" not in last_request["headers"]

    def test_send_one_record_header_auth(self):
        """Test that header auth method uses Basic auth header."""
        http_client = MockHTTPClient()
        mock_response = MockResponseBuilder.webhook_send_response()
        http_client.add_response("webhook", mock_response)

        api_key = "my-secret-key"
        webhooks = WebhooksResource(api_key=api_key, http_client=http_client)

        webhooks.send_one_record(
            webhook_url="https://api.nexla.com/webhook/abc123",
            record={"data": "test"},
            auth_method="header"
        )

        last_request = http_client.get_last_request()

        # Verify Basic auth header is set correctly
        expected_encoded = base64.b64encode(api_key.encode()).decode()
        assert last_request["headers"]["Authorization"] == f"Basic {expected_encoded}"

        # api_key should not be in query params for header auth (params may be None or empty)
        params = last_request.get("params") or {}
        assert "api_key" not in params

    def test_send_many_records_success(self):
        """Test sending multiple records successfully."""
        http_client = MockHTTPClient()
        mock_response = MockResponseBuilder.webhook_send_response(
            dataset_id=54321, processed=3
        )
        http_client.add_response("webhook", mock_response)

        webhooks = WebhooksResource(api_key="test-api-key", http_client=http_client)
        records = [
            {"event": "page_view", "page": "/home"},
            {"event": "page_view", "page": "/about"},
            {"event": "click", "button": "signup"}
        ]

        response = webhooks.send_many_records(
            webhook_url="https://api.nexla.com/webhook/abc123",
            records=records
        )

        assert isinstance(response, WebhookResponse)
        assert response.dataset_id == 54321
        assert response.processed == 3

        # Verify request was made correctly
        last_request = http_client.get_last_request()
        assert last_request["method"] == "POST"
        assert last_request["json"] == records

    def test_send_many_records_empty_list(self):
        """Test sending an empty list of records."""
        http_client = MockHTTPClient()
        mock_response = MockResponseBuilder.webhook_send_response(processed=0)
        http_client.add_response("webhook", mock_response)

        webhooks = WebhooksResource(api_key="test-api-key", http_client=http_client)

        response = webhooks.send_many_records(
            webhook_url="https://api.nexla.com/webhook/abc123",
            records=[]
        )

        assert isinstance(response, WebhookResponse)
        assert response.processed == 0

        last_request = http_client.get_last_request()
        assert last_request["json"] == []

    def test_send_many_records_with_all_options(self):
        """Test sending multiple records with all options."""
        http_client = MockHTTPClient()
        mock_response = MockResponseBuilder.webhook_send_response()
        http_client.add_response("webhook", mock_response)

        webhooks = WebhooksResource(api_key="test-api-key", http_client=http_client)
        options = WebhookSendOptions(
            include_headers=True,
            include_url_params=True,
            force_schema_detection=True
        )

        webhooks.send_many_records(
            webhook_url="https://api.nexla.com/webhook/abc123",
            records=[{"id": 1}, {"id": 2}],
            options=options,
            auth_method="header"
        )

        last_request = http_client.get_last_request()

        # Verify all options are set
        assert last_request["params"]["include_headers"] == "true"
        assert last_request["params"]["include_url_params"] == "true"
        assert last_request["params"]["force_schema_detection"] == "true"

        # Verify header auth
        assert "Authorization" in last_request["headers"]


class TestWebhooksErrorHandling:
    """Tests for webhook error handling."""

    def test_send_one_record_network_error(self):
        """Test that network errors are wrapped in NexlaError."""
        http_client = MockHTTPClient()
        http_client.add_response(
            "webhook",
            HttpClientError(
                message="Connection refused",
                status_code=500,
                response={"error": "Server error"}
            )
        )

        webhooks = WebhooksResource(api_key="test-api-key", http_client=http_client)

        with pytest.raises(NexlaError) as exc_info:
            webhooks.send_one_record(
                webhook_url="https://api.nexla.com/webhook/abc123",
                record={"data": "test"}
            )

        assert "Webhook request failed" in str(exc_info.value)

    def test_send_many_records_network_error(self):
        """Test that network errors in send_many_records are wrapped."""
        http_client = MockHTTPClient()
        http_client.add_response(
            "webhook",
            HttpClientError(
                message="Timeout",
                status_code=504,
                response={"error": "Gateway timeout"}
            )
        )

        webhooks = WebhooksResource(api_key="test-api-key", http_client=http_client)

        with pytest.raises(NexlaError) as exc_info:
            webhooks.send_many_records(
                webhook_url="https://api.nexla.com/webhook/abc123",
                records=[{"id": 1}]
            )

        assert "Webhook request failed" in str(exc_info.value)

    def test_error_includes_context(self):
        """Test that errors include useful context information."""
        http_client = MockHTTPClient()
        http_client.add_response(
            "webhook",
            HttpClientError(
                message="Bad Request",
                status_code=400,
                response={"error": "Invalid payload"}
            )
        )

        webhooks = WebhooksResource(api_key="test-api-key", http_client=http_client)
        webhook_url = "https://api.nexla.com/webhook/test123"

        with pytest.raises(NexlaError) as exc_info:
            webhooks.send_one_record(
                webhook_url=webhook_url,
                record={"invalid": "data"}
            )

        error = exc_info.value
        assert error.operation == "webhook_send"
        assert error.context is not None
        assert error.context["url"] == webhook_url
        assert error.context["method"] == "POST"


class TestWebhooksHTTPClientCreation:
    """Tests for HTTP client lazy creation."""

    def test_creates_http_client_on_demand(self):
        """Test that HTTP client is created on first request if not provided."""
        # This test verifies the _get_http_client method creates a client
        webhooks = WebhooksResource(api_key="test-api-key")
        assert webhooks._http_client is None

        # Getting the http client should create one
        http_client = webhooks._get_http_client()
        assert http_client is not None
        assert webhooks._http_client is http_client

        # Calling again should return the same instance
        http_client2 = webhooks._get_http_client()
        assert http_client is http_client2

    def test_uses_provided_http_client(self):
        """Test that provided HTTP client is used instead of creating new one."""
        mock_client = MockHTTPClient()
        webhooks = WebhooksResource(api_key="test-api-key", http_client=mock_client)

        returned_client = webhooks._get_http_client()
        assert returned_client is mock_client
