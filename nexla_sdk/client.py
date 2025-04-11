"""
Nexla API client
"""
import logging
from typing import Dict, Any, Optional, Type, TypeVar, Union, List, cast

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
        client = NexlaClient("your-api-key")
        flows = client.flows.list()
    """
    
    def __init__(self, api_key: str = None, api_url: str = "https://dataops.nexla.com/nexla-api", api_version: str = "v1"):
        """
        Initialize the Nexla client
        
        Args:
            api_key: Nexla API key (optional, can be set later via login)
            api_url: Nexla API URL
            api_version: API version to use
        """
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.api_version = api_version
        
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
            if isinstance(data, list):
                return [model_class.model_validate(item) for item in data]
            return model_class.model_validate(data)
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
        url = f"{self.api_url}{path}"
        headers = {
            "Accept": f"application/vnd.nexla.api.{self.api_version}+json",
            "Content-Type": "application/json"
        }
        
        # Add authorization header if we have an API key
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
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
                raise NexlaAuthError("Authentication failed. Check your API key.") from e
            
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