"""
HTTP client interface and implementations for Nexla SDK
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union

import requests
from requests.adapters import HTTPAdapter
try:  # urllib3 Retry API
    from urllib3.util.retry import Retry
except Exception:  # pragma: no cover
    Retry = None

try:
    from importlib.metadata import version  # Python 3.8+
    _SDK_VERSION = version("nexla-sdk")
except Exception:  # pragma: no cover
    _SDK_VERSION = "unknown"

# Optional OpenTelemetry imports (guarded by availability)
from . import telemetry
try:  # pragma: no cover - optional dependency
    from opentelemetry.trace import SpanKind, Status, StatusCode  # type: ignore
    from opentelemetry.propagate import inject  # type: ignore
except Exception:  # pragma: no cover
    SpanKind = None  # type: ignore[assignment]
    Status = None  # type: ignore[assignment]
    StatusCode = None  # type: ignore[assignment]

    def inject(carrier: Dict[str, str]) -> None:  # type: ignore[no-redef]
        return None


class HttpClientInterface(ABC):
    """
    Abstract interface for HTTP clients used by the Nexla SDK.
    This allows for different HTTP client implementations or mocks for testing.
    """
    
    @abstractmethod
    def request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Union[Dict[str, Any], None]:
        """
        Send an HTTP request
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            url: Request URL
            headers: Request headers
            **kwargs: Additional arguments for the request
            
        Returns:
            Response data as dictionary or None for 204 No Content responses
            
        Raises:
            HttpClientError: If the request fails
        """
        pass


class HttpClientError(Exception):
    """Base exception for HTTP client errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response or {}
        self.headers = headers or {}


class RequestsHttpClient(HttpClientInterface):
    """HTTP client implementation using the requests library with retries and timeouts."""

    def __init__(
        self,
        timeout: float = 10.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        tracer: Optional[object] = None,
    ):
        self.timeout = timeout
        self.session = requests.Session()
        self.tracer = tracer if tracer is not None else telemetry.get_tracer(False)

        # Configure retries if available
        if Retry is not None:
            retry = Retry(
                total=max_retries,
                read=max_retries,
                connect=max_retries,
                backoff_factor=backoff_factor,
                status_forcelist=[429, 502, 503, 504],
                allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
                raise_on_status=False,
            )
            adapter = HTTPAdapter(max_retries=retry)
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)

    def request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Union[Dict[str, Any], None]:
        """Send an HTTP request using a session with sane defaults."""
        span_name = f"Nexla API {method.upper()}"
        kind = SpanKind.CLIENT if telemetry._opentelemetry_available and SpanKind is not None else None  # type: ignore[assignment]
        with self.tracer.start_as_current_span(span_name, kind=kind):  # type: ignore[arg-type]
            # We intentionally fetch the current span after creating it to set attributes
            span = None
            try:
                # Get the span from the current context if available (best-effort)
                if telemetry._opentelemetry_available and hasattr(telemetry, "trace") and telemetry.trace:
                    span = telemetry.trace.get_current_span()  # type: ignore[attr-defined]
            except Exception:
                span = None

            try:
                timeout = kwargs.pop("timeout", self.timeout)
                # Default headers
                merged_headers = {
                    "User-Agent": f"nexla-sdk/{_SDK_VERSION}",
                    **(headers or {}),
                }

                # Inject trace context for distributed tracing if OTEL is available
                try:
                    if telemetry._opentelemetry_available and inject is not None:
                        inject(merged_headers)  # type: ignore[misc]
                except Exception:
                    # Do not fail the request if injection fails
                    pass

                # Set basic attributes
                try:
                    if span and getattr(span, "is_recording", lambda: False)():
                        span.set_attribute("http.method", method.upper())
                        span.set_attribute("url.full", url)
                        try:
                            span.set_attribute("server.address", url.split("/")[2])
                        except Exception:
                            pass
                        span.set_attribute("component", "nexla-sdk")
                except Exception:
                    pass

                response = self.session.request(method, url, headers=merged_headers, timeout=timeout, **kwargs)
                response.raise_for_status()

                # Add response attributes
                try:
                    if span and getattr(span, "is_recording", lambda: False)():
                        span.set_attribute("http.status_code", response.status_code)
                except Exception:
                    pass

                # Return None for 204 No Content or empty responses
                if response.status_code == 204 or not response.content:
                    return None

                # Check if response content type indicates JSON
                content_type = response.headers.get('content-type', '').lower()
                if 'application/json' in content_type or 'text/json' in content_type:
                    return response.json()

                # Try to parse as JSON anyway, but handle cases where it's not JSON
                try:
                    return response.json()
                except (ValueError, requests.exceptions.JSONDecodeError):
                    # If it's not JSON, return the response as text in a dict
                    return {"raw_text": response.text, "status_code": response.status_code}

            except requests.exceptions.HTTPError as e:
                # Record exception on span
                try:
                    if span and getattr(span, "is_recording", lambda: False)() and telemetry._opentelemetry_available and Status is not None and StatusCode is not None:
                        span.record_exception(e)
                        span.set_status(Status(status_code=StatusCode.ERROR))  # type: ignore[call-arg]
                except Exception:
                    pass

                # Create standardized error with status code and response data
                error_data: Dict[str, Any] = {}
                if 'response' in e.__dict__:
                    resp = e.response
                else:
                    resp = response  # type: ignore[name-defined]

                if resp is not None and getattr(resp, 'content', None):
                    try:
                        error_data = resp.json()
                    except ValueError:
                        error_data = {"raw_text": resp.text}

                raise HttpClientError(
                    message=str(e),
                    status_code=getattr(resp, 'status_code', None),
                    response=error_data,
                    headers=dict(getattr(resp, 'headers', {}) or {})
                ) from e

            except requests.exceptions.RequestException as e:
                # Record exception on span
                try:
                    if span and getattr(span, "is_recording", lambda: False)() and telemetry._opentelemetry_available and Status is not None and StatusCode is not None:
                        span.record_exception(e)
                        span.set_status(Status(status_code=StatusCode.ERROR))  # type: ignore[call-arg]
                except Exception:
                    pass

                # Handle general request exceptions (network errors, etc.)
                raise HttpClientError(message=str(e)) from e
