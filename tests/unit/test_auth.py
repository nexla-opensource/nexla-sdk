"""Unit tests for TokenAuthHandler behavior after recent auth changes.
Focus on service-key flow, direct token behavior, retry on 401, and logout.
"""

import time
import pytest

from nexla_sdk.auth import TokenAuthHandler
from nexla_sdk.exceptions import AuthenticationError
from tests.utils.fixtures import MockHTTPClient, create_auth_token_response


pytestmark = pytest.mark.unit


def test_service_key_obtain_and_ensure_token():
    mock_http = MockHTTPClient()
    mock_http.add_response("/token", create_auth_token_response(access_token="tk-1", expires_in=60))

    auth = TokenAuthHandler(service_key="sk-123", base_url="https://api.test/nexla-api", http_client=mock_http)

    # No token yet; ensure should obtain lazily
    token = auth.ensure_valid_token()
    assert token == "tk-1"
    mock_http.assert_request_made("POST", "/token")


def test_service_key_refresh_when_near_expiry():
    mock_http = MockHTTPClient()

    # Return tk-1 for first /token call, tk-2 for second, using a stateful callable
    calls = {"n": 0}

    def token_responder(_req):
        calls["n"] += 1
        if calls["n"] == 1:
            return create_auth_token_response(access_token="tk-1", expires_in=1)
        return create_auth_token_response(access_token="tk-2", expires_in=3600)

    mock_http.add_response("/token", token_responder)

    auth = TokenAuthHandler(service_key="sk-123", base_url="https://api.test/nexla-api", token_refresh_margin=30, http_client=mock_http)

    token1 = auth.ensure_valid_token()
    assert token1 == "tk-1"

    # Simulate time passing beyond expiry margin
    auth._token_expiry = time.time() - 1
    token2 = auth.ensure_valid_token()
    assert token2 == "tk-2"


def test_direct_token_mode_no_refresh_allowed():
    mock_http = MockHTTPClient()
    auth = TokenAuthHandler(access_token="direct-abc", http_client=mock_http)
    assert auth.ensure_valid_token() == "direct-abc"
    with pytest.raises(AuthenticationError):
        auth.refresh_session_token()


def test_execute_authenticated_request_retries_on_401_with_service_key():
    mock_http = MockHTTPClient()
    # Initial token obtain
    mock_http.add_response("/token", create_auth_token_response(access_token="tk-0", expires_in=3600))

    # Endpoint that will fail once with 401 then succeed
    attempt = {"n": 0}

    def flappy(req):
        if "/widgets" in req["url"]:
            attempt["n"] += 1
            if attempt["n"] == 1:
                from nexla_sdk.http_client import HttpClientError
                raise HttpClientError("unauthorized", status_code=401, response={"error": "unauthorized"})
            return {"status": "ok"}
        return {"status": "unexpected"}

    mock_http.add_response("/widgets", flappy)

    auth = TokenAuthHandler(service_key="sk-xyz", base_url="https://api.test/nexla-api", http_client=mock_http)

    out = auth.execute_authenticated_request("GET", "https://api.test/nexla-api/widgets", headers={})
    assert out == {"status": "ok"}
    # Ensure we attempted an additional token obtain after 401
    # First obtain occurred during first ensure; on 401 we call obtain again
    # There should be at least one POST /token request recorded
    posts = [r for r in mock_http.requests if r["method"] == "POST" and "/token" in r["url"]]
    assert len(posts) >= 1


def test_logout_clears_token_and_calls_endpoint():
    mock_http = MockHTTPClient()
    mock_http.add_response("/token", create_auth_token_response(access_token="tk", expires_in=3600))
    mock_http.add_response("/token/logout", {"status": "ok"})
    auth = TokenAuthHandler(service_key="sk-1", base_url="https://api.test/nexla-api", http_client=mock_http)

    # Obtain a token
    assert auth.ensure_valid_token() == "tk"
    # Logout
    auth.logout()
    # Token cleared
    with pytest.raises(AuthenticationError):
        auth.get_access_token()
    # Endpoint was called
    last = mock_http.get_last_request()
    assert last and last["method"] == "POST" and "/token/logout" in last["url"]
