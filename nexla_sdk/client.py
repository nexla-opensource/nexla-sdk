"""
Nexla API client
"""
import logging
import time
from typing import Dict, Any, Optional, Type, TypeVar, Union, List, cast
import base64

import requests
from pydantic import BaseModel, ValidationError

from .exceptions import NexlaError, NexlaAuthError, NexlaAPIError, NexlaValidationError, NexlaClientError, NexlaNotFoundError
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

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)


class NexlaClient:
    """
    Client for the Nexla API
    
    Example:
        # Using service key
        client = NexlaClient(service_key="your-service-key")
        
        # List flows
        flows = client.flows.list()
    """
    
    def __init__(self, 
                 service_key: str, 
                 api_url: str = "https://dataops.nexla.com/nexla-api", 
                 api_version: str = "v1",
                 token_refresh_margin: int = 300):
        """
        Initialize the Nexla client
        
        Args:
            service_key: Nexla service key for authentication
            api_url: Nexla API URL
            api_version: API version to use
            token_refresh_margin: Seconds before token expiry to trigger refresh (default: 5 minutes)
        """
        self.service_key = service_key
        self.api_url = api_url.rstrip('/')
        self.api_version = api_version
        self.token_refresh_margin = token_refresh_margin
        
        # Session token management
        self._access_token = None
        self._token_expiry = 0
        
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
        
        # Obtain session token
        self.obtain_session_token()

    def obtain_session_token(self) -> None:
        """
        Obtains a session token using the service key
        
        Raises:
            NexlaAuthError: If authentication fails
        """
        url = f"{self.api_url}/token"
        headers = {
            "Authorization": f"Basic {self.service_key}",
            "Accept": f"application/vnd.nexla.api.{self.api_version}+json",
            "Content-Length": "0"
        }
        
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            self._access_token = token_data.get("access_token")
            # Calculate expiry time (current time + expires_in seconds)
            expires_in = token_data.get("expires_in", 3600)
            self._token_expiry = time.time() + expires_in
            
            logger.debug("Session token obtained successfully")
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise NexlaAuthError("Authentication failed. Check your service key.") from e
            
            error_msg = f"Failed to obtain session token: {e}"
            error_data = {}
            
            if response.content:
                try:
                    error_data = response.json()
                    if "message" in error_data:
                        error_msg = f"Authentication error: {error_data['message']}"
                    elif "error" in error_data:
                        error_msg = f"Authentication error: {error_data['error']}"
                except ValueError:
                    error_msg = f"Authentication error: {response.text}"
                    
            raise NexlaAPIError(error_msg, status_code=response.status_code, response=error_data) from e
            
        except requests.exceptions.RequestException as e:
            raise NexlaError(f"Failed to obtain session token: {e}") from e

    def refresh_session_token(self) -> None:
        """
        Refreshes the session token before it expires
        
        Raises:
            NexlaAuthError: If token refresh fails
        """
        if not self._access_token:
            self.obtain_session_token()
            return
        
        url = f"{self.api_url}/token/refresh"
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": f"application/vnd.nexla.api.{self.api_version}+json",
            "Content-Length": "0"
        }
        
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            self._access_token = token_data.get("access_token")
            # Calculate expiry time (current time + expires_in seconds)
            expires_in = token_data.get("expires_in", 3600)
            self._token_expiry = time.time() + expires_in
            
            logger.debug("Session token refreshed successfully")
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                # If refresh fails with 401, try obtaining a new token
                logger.warning("Token refresh failed with 401, obtaining new session token")
                self.obtain_session_token()
                return
                
            error_msg = f"Failed to refresh session token: {e}"
            error_data = {}
            
            if response.content:
                try:
                    error_data = response.json()
                    if "message" in error_data:
                        error_msg = f"Token refresh error: {error_data['message']}"
                    elif "error" in error_data:
                        error_msg = f"Token refresh error: {error_data['error']}"
                except ValueError:
                    error_msg = f"Token refresh error: {response.text}"
                    
            raise NexlaAPIError(error_msg, status_code=response.status_code, response=error_data) from e
            
        except requests.exceptions.RequestException as e:
            raise NexlaError(f"Failed to refresh session token: {e}") from e
    
    def _ensure_valid_token(self) -> None:
        """
        Ensures a valid session token is available, refreshing if necessary
        """
        current_time = time.time()
        
        # If no token or token expired/about to expire
        if not self._access_token or (self._token_expiry - current_time) < self.token_refresh_margin:
            if self._access_token:
                # Refresh existing token
                self.refresh_session_token()
            else:
                # Obtain new token
                self.obtain_session_token()

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
            
    def request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """
        Send a request to the Nexla API
        
        Args:
            method: HTTP method
            path: API path
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            API response as a dictionary
            
        Raises:
            NexlaAuthError: If authentication fails
            NexlaAPIError: If the API returns an error
        """
        # Ensure we have a valid token
        self._ensure_valid_token()
            
        url = f"{self.api_url}{path}"
        headers = {
            "Accept": f"application/vnd.nexla.api.{self.api_version}+json",
            "Content-Type": "application/json"
        }
        
        # Add authorization header
        headers["Authorization"] = f"Bearer {self._access_token}"
        
        # If custom headers are provided, merge them with the default headers
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))
            
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            
            # Return empty dict for 204 No Content
            if response.status_code == 204:
                return {}
                
            # Parse JSON response
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                # If authentication failed, try refreshing the token
                logger.warning("Request failed with 401, refreshing session token and retrying")
                self.obtain_session_token()  # Get a new token
                
                # Update headers with new token
                headers["Authorization"] = f"Bearer {self._access_token}"
                
                # Retry the request with the new token
                try:
                    response = requests.request(method, url, headers=headers, **kwargs)
                    response.raise_for_status()
                    
                    # Return empty dict for 204 No Content
                    if response.status_code == 204:
                        return {}
                    
                    # Parse JSON response
                    return response.json()
                except requests.exceptions.HTTPError:
                    # If retry also fails, fall through to error handling
                    pass
            
            # Handle error response
            if response.status_code == 401:
                raise NexlaAuthError("Authentication failed. Check your service key.") from e
            
            error_msg = f"API request failed: {e}"
            error_data = {}
            
            if response.content:
                try:
                    error_data = response.json()
                    if "message" in error_data:
                        error_msg = f"API error: {error_data['message']}"
                    elif "error" in error_data:
                        error_msg = f"API error: {error_data['error']}"
                except ValueError:
                    error_msg = f"API error: {response.text}"
                    
            raise NexlaAPIError(error_msg, status_code=response.status_code, response=error_data) from e
            
        except requests.exceptions.RequestException as e:
            raise NexlaError(f"Request failed: {e}") from e 