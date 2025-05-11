"""
Nexla SDK for Python

A Python SDK for interacting with the Nexla API.

Example:
    from nexla_sdk import NexlaClient
    
    client = NexlaClient(service_key="your-service-key")
    flows = client.flows.list()
"""

from .client import NexlaClient
from .exceptions import NexlaError, NexlaAuthError, NexlaAPIError, NexlaValidationError, NexlaClientError, NexlaNotFoundError
from .http import HttpClientInterface, RequestsHttpClient, HttpClientError

__version__ = "0.1.0"
__all__ = [
    "NexlaClient",
    "NexlaError",
    "NexlaAuthError",
    "NexlaAPIError",
    "NexlaValidationError",
    "NexlaClientError",
    "NexlaNotFoundError",
    "HttpClientInterface",
    "RequestsHttpClient",
    "HttpClientError"
] 