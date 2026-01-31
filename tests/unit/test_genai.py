import pytest

from nexla_sdk import NexlaClient
from nexla_sdk.models.genai.requests import (
    GenAiConfigCreatePayload,
    GenAiConfigPayload,
    GenAiOrgSettingPayload,
)
from nexla_sdk.models.genai.responses import (
    ActiveConfigView,
    GenAiConfig,
    GenAiOrgSetting,
)

pytestmark = pytest.mark.unit


@pytest.fixture
def client(mock_client: NexlaClient) -> NexlaClient:
    return mock_client


class TestGenAIResource:
    def test_configs_crud(self, client, mock_http_client):
        mock_http_client.add_response(
            "/gen_ai_integration_configs", [{"id": 10, "name": "OpenAI"}]
        )
        cfgs = client.genai.list_configs()
        assert isinstance(cfgs[0], GenAiConfig) and cfgs[0].id == 10

        mock_http_client.clear_responses()
        create_payload = GenAiConfigCreatePayload(
            name="OpenAI",
            type="genai_openai",
            config={"api_key": "x"},
            data_credentials_id=1,
        )
        mock_http_client.add_response(
            "/gen_ai_integration_configs", {"id": 11, "name": "OpenAI"}
        )
        created = client.genai.create_config(create_payload)
        assert isinstance(created, GenAiConfig) and created.id == 11

        mock_http_client.clear_responses()
        mock_http_client.add_response(
            "/gen_ai_integration_configs/11", {"id": 11, "name": "OpenAI"}
        )
        got = client.genai.get_config(11)
        assert got.id == 11

        mock_http_client.clear_responses()
        update_payload = GenAiConfigPayload(description="desc")
        mock_http_client.add_response(
            "/gen_ai_integration_configs/11", {"id": 11, "name": "OpenAI-2"}
        )
        upd = client.genai.update_config(11, update_payload)
        assert upd.name == "OpenAI-2"

        mock_http_client.clear_responses()
        mock_http_client.add_response(
            "/gen_ai_integration_configs/11", {"status": "ok"}
        )
        d = client.genai.delete_config(11)
        assert d.get("status") == "ok"

    def test_org_settings_and_active(self, client, mock_http_client):
        mock_http_client.add_response(
            "/gen_ai_org_settings", [{"id": 100, "gen_ai_usage": "all"}]
        )
        items = client.genai.list_org_settings(org_id=9, all=True)
        assert isinstance(items[0], GenAiOrgSetting)

        mock_http_client.clear_responses()
        payload = GenAiOrgSettingPayload(gen_ai_config_id=11, gen_ai_usage="all")
        mock_http_client.add_response(
            "/gen_ai_org_settings", {"id": 101, "gen_ai_usage": "all"}
        )
        created = client.genai.create_org_setting(payload)
        assert isinstance(created, GenAiOrgSetting) and created.id == 101

        mock_http_client.clear_responses()
        mock_http_client.add_response(
            "/gen_ai_org_settings/101", {"id": 101, "gen_ai_usage": "all"}
        )
        got = client.genai.get_org_setting(101)
        assert got.id == 101

        mock_http_client.clear_responses()
        mock_http_client.add_response("/gen_ai_org_settings/101", {"status": "ok"})
        d = client.genai.delete_org_setting(101)
        assert d.get("status") == "ok"

        mock_http_client.clear_responses()
        mock_http_client.add_response(
            "/gen_ai_org_settings/active_config",
            {"gen_ai_usage": "all", "active_config": {}},
        )
        view = client.genai.show_active_config("all")
        assert isinstance(view, ActiveConfigView) and view.gen_ai_usage == "all"
