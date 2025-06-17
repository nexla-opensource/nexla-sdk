"""
Nexla API client
"""
import logging
import time
from typing import Dict, Any, Optional, Type, TypeVar, Union, List, cast
import base64

from pydantic import BaseModel, ValidationError

from .exceptions import NexlaError, NexlaAuthError, NexlaAPIError, NexlaValidationError, NexlaClientError, NexlaNotFoundError
from .auth import TokenAuthHandler
from .http import HttpClientInterface, RequestsHttpClient, HttpClientError
from .api.flows import FlowsAPI
from .api.sources import SourcesAPI
from .api.destinations import DestinationsAPI
from .api.credentials import CredentialsAPI
from .api.lookups import LookupsAPI
from .api.transforms import TransformsAPI
from .api.nexsets import NexsetsAPI
from .api.webhooks import WebhooksAPI
from .api.organizations import OrganizationsAPI
from .api.users import UsersAPI
from .api.teams import TeamsAPI
from .api.projects import ProjectsAPI
from .api.notifications import NotificationsApi
from .api.metrics import MetricsAPI
from .api.audit_logs import AuditLogsAPI
from .api.session import SessionAPI
from .api.access import AccessControlAPI
from .api.quarantine_settings import QuarantineSettingsAPI
from .api.schemas import SchemasAPI

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)


class NexlaClient:
    """
    Client for the Nexla API
    
    The Nexla API supports two authentication methods:
    
    1. **Service Key Authentication** (Recommended for programmatic access):
       Service keys are "forever keys" created in the Nexla UI that can be used to 
       programmatically obtain session tokens. The SDK automatically handles token 
       obtaining and refreshing.
       
    2. **Direct Access Token Authentication**:
       Access tokens obtained can be used directly. Note that these tokens expire 
       (typically after 1 hour) and cannot be automatically refreshed by the SDK.
    
    Examples:
        # Method 1: Using service key (recommended for automation)
        client = NexlaClient(service_key="your-service-key")
        
        # Method 2: Using access token directly (manual/short-term use)
        client = NexlaClient(access_token="your-access-token")
        
        # Using the client (same regardless of authentication method)
        flows = client.flows.list()
        
    Note:
        - Service keys should be treated as highly sensitive credentials
        - Only provide either service_key OR access_token, not both
        - When using direct access tokens, ensure they have sufficient lifetime
          for your operations as they cannot be automatically refreshed
    """
    
    def __init__(self, 
                 service_key: Optional[str] = None,
                 access_token: Optional[str] = None,
                 api_url: str = "https://dataops.nexla.io/nexla-api", 
                 api_version: str = "v1",
                 token_refresh_margin: int = 300,
                 http_client: Optional[HttpClientInterface] = None):
        """
        Initialize the Nexla client
        
        Args:
            service_key: Nexla service key for authentication (mutually exclusive with access_token)
            access_token: Nexla access token for direct authentication (mutually exclusive with service_key)
            api_url: Nexla API URL
            api_version: API version to use
            token_refresh_margin: Seconds before token expiry to trigger refresh (default: 5 minutes)
            http_client: HTTP client implementation (defaults to RequestsHttpClient)
            
        Raises:
            NexlaClientError: If neither or both authentication methods are provided
        """
        # Validate authentication parameters
        if not service_key and not access_token:
            raise NexlaClientError("Either service_key or access_token must be provided")
        if service_key and access_token:
            raise NexlaClientError("Cannot provide both service_key and access_token. Choose one authentication method.")
            
        self.api_url = api_url.rstrip('/')
        self.api_version = api_version
        self.http_client = http_client or RequestsHttpClient()
        
        # Initialize authentication handler
        self.auth_handler = TokenAuthHandler(
            service_key=service_key,
            access_token=access_token,
            api_url=api_url,
            api_version=api_version,
            token_refresh_margin=token_refresh_margin,
            http_client=self.http_client
        )
        
        # Initialize API endpoints
        self.flows = FlowsAPI(self)
        self.sources = SourcesAPI(self)
        self.destinations = DestinationsAPI(self)
        self.credentials = CredentialsAPI(self)
        self.lookups = LookupsAPI(self)
        self.transforms = TransformsAPI(self)
        self.nexsets = NexsetsAPI(self)
        self.webhooks = WebhooksAPI(self)
        self.organizations = OrganizationsAPI(self)
        self.users = UsersAPI(self)
        self.teams = TeamsAPI(self)
        self.projects = ProjectsAPI(self)
        self.notifications = NotificationsApi(self)
        self.metrics = MetricsAPI(self)
        self.audit_logs = AuditLogsAPI(self)
        self.session = SessionAPI(self)
        self.access_control = AccessControlAPI(self)
        self.quarantine_settings = QuarantineSettingsAPI(self)
        self.schemas = SchemasAPI(self)

    def get_access_token(self) -> str:
        """
        Get a valid access token, automatically refreshing if necessary
        
        This method ensures that the returned token is valid and not expired.
        If the token is about to expire (within the token_refresh_margin), 
        it will be automatically refreshed before being returned.
        
        Returns:
            A valid access token string
            
        Raises:
            NexlaAuthError: If no valid token is available or refresh fails
            
        Examples:
            # Get a valid access token
            token = client.get_access_token()
            
            # Use the token for external API calls
            headers = {"Authorization": f"Bearer {token}"}
        """
        return self.auth_handler.ensure_valid_token()

    def _convert_to_model(self, data: Union[Dict[str, Any], List[Dict[str, Any]]], model_class: Type[T]) -> Union[T, List[T]]:
        """
        Convert API response data to a Pydantic model
        
        Args:
            data: API response data, either a dict or a list of dicts
            model_class: Pydantic model class to convert to
            
        Returns:
            Pydantic model instance or list of instances
            
        Raises:
            NexlaValidationError: If validation fails
        """
        try:
            logger.debug(f"Converting data to model: {model_class.__name__}")
            logger.debug(f"Data to convert: {data}")
            
            if isinstance(data, list):
                result = [model_class.model_validate(item) for item in data]
                logger.debug(f"Converted list result: {result}")
                return result
            
            result = model_class.model_validate(data)
            logger.debug(f"Converted single result: {result}")
            return result
        except ValidationError as e:
            # Log the validation error details
            logger.error(f"Validation error converting to {model_class.__name__}: {e}")
            raise NexlaValidationError(f"Failed to convert API response to {model_class.__name__}: {e}")
            
    def request(self, method: str, path: str, **kwargs) -> Union[Dict[str, Any], None]:
        """
        Send a request to the Nexla API
        
        Args:
            method: HTTP method
            path: API path
            **kwargs: Additional arguments to pass to HTTP client
            
        Returns:
            API response as a dictionary or None for 204 No Content responses
            
        Raises:
            NexlaAuthError: If authentication fails
            NexlaAPIError: If the API returns an error
        """
        url = f"{self.api_url}{path}"
        headers = {
            "Accept": f"application/vnd.nexla.api.{self.api_version}+json",
            "Content-Type": "application/json"
        }
        
        # If custom headers are provided, merge them with the default headers
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))
            
        try:
            # Let auth handler manage getting a valid token and handling auth retries
            return self.auth_handler.execute_authenticated_request(
                method=method,
                url=url,
                headers=headers,
                **kwargs
            )
        except HttpClientError as e:
            # Map HTTP client errors to appropriate Nexla exceptions
            self._handle_http_error(e)
        except Exception as e:
            raise NexlaError(f"Request failed: {e}") from e

    def _handle_http_error(self, error: HttpClientError):
        """
        Handle HTTP client errors by mapping them to appropriate Nexla exceptions
        
        Args:
            error: The HTTP client error
            
        Raises:
            NexlaAuthError: If authentication fails (401)
            NexlaNotFoundError: If resource not found (404)
            NexlaAPIError: For other API errors
        """
        status_code = getattr(error, 'status_code', None)
        error_data = getattr(error, 'response', {})
        
        error_msg = f"API request failed: {error}"
        
        if error_data:
            if "message" in error_data:
                error_msg = f"API error: {error_data['message']}"
            elif "error" in error_data:
                error_msg = f"API error: {error_data['error']}"
        
        # Map status codes to specific exceptions
        if status_code == 401:
            raise NexlaAuthError("Authentication failed. Check your service key.") from error
        elif status_code == 404:
            resource_type = error_data.get("resource_type", "")
            resource_id = error_data.get("resource_id", "")
            raise NexlaNotFoundError(
                f"Resource not found: {resource_type}/{resource_id}",
                resource_type=resource_type,
                resource_id=resource_id
            ) from error
        else:
            raise NexlaAPIError(
                error_msg,
                status_code=status_code,
                response=error_data
            ) from error 