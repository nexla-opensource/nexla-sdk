"""
Base API client
"""
import logging
from typing import Dict, Any, Optional, Type, TypeVar, Union, List

import requests
from pydantic import BaseModel

from ..exceptions import NexlaAPIError, NexlaAuthError, NexlaError, NexlaNotFoundError

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)


class BaseAPI:
    """Base API client for all Nexla API endpoints"""

    def __init__(self, client):
        """
        Initialize the API client
        
        Args:
            client: The NexlaClient instance
        """
        self.client = client
        
    def _request(self, method: str, path: str, model_class: Optional[Type[T]] = None, **kwargs) -> Union[Dict[str, Any], T, List[T]]:
        """
        Send a request to the API
        
        Args:
            method: HTTP method
            path: API path
            model_class: Optional Pydantic model class to convert the response to
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response data, either as a dict or converted to the specified model
            
        Raises:
            NexlaAuthError: If authentication fails
            NexlaAPIError: If the API returns an error
        """
        url = f"{self.client.api_url}{path}"
        headers = {
            "Accept": f"application/vnd.nexla.api.{self.client.api_version}+json",
            "Content-Type": "application/json"
        }
        
        # Add authorization header if we have an API key
        if self.client.api_key:
            headers["Authorization"] = f"Bearer {self.client.api_key}"
        
        # If custom headers are provided, merge them with the default headers
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))
            
        try:
            logger.debug(f"Requesting {method} {url}")
            logger.debug(f"Headers: {headers}")
            response = requests.request(method, url, headers=headers, **kwargs)
            logger.debug(f"Response Status Code: {response.status_code}")
            response.raise_for_status()
            
            # Return empty dict for 204 No Content
            if response.status_code == 204:
                return {}
                
            # Parse JSON response
            data = response.json()
            
            # Convert to model if specified
            if model_class:
                return self.client._convert_to_model(data, model_class)
                
            return data
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTPError encountered: {e}")
            logger.error(f"Response Status Code: {response.status_code}")
            logger.error(f"Response Content: {response.content}")
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
            logger.error(f"RequestException encountered: {e}")
            raise NexlaError(f"Request failed: {e}") from e
            
    def _get(self, path: str, model_class: Optional[Type[T]] = None, **kwargs) -> Union[Dict[str, Any], T]:
        """
        Send a GET request
        
        Args:
            path: API path
            model_class: Optional Pydantic model class to convert the response to
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response data
        """
        return self._request("GET", path, model_class=model_class, **kwargs)
        
    def _post(self, path: str, model_class: Optional[Type[T]] = None, **kwargs) -> Union[Dict[str, Any], T]:
        """
        Send a POST request
        
        Args:
            path: API path
            model_class: Optional Pydantic model class to convert the response to
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response data
        """
        return self._request("POST", path, model_class=model_class, **kwargs)
        
    def _put(self, path: str, model_class: Optional[Type[T]] = None, **kwargs) -> Union[Dict[str, Any], T]:
        """
        Send a PUT request
        
        Args:
            path: API path
            model_class: Optional Pydantic model class to convert the response to
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response data
        """
        return self._request("PUT", path, model_class=model_class, **kwargs)
        
    def _patch(self, path: str, model_class: Optional[Type[T]] = None, **kwargs) -> Union[Dict[str, Any], T]:
        """
        Send a PATCH request
        
        Args:
            path: API path
            model_class: Optional Pydantic model class to convert the response to
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response data
        """
        return self._request("PATCH", path, model_class=model_class, **kwargs)
        
    def _delete(self, path: str, model_class: Optional[Type[T]] = None, **kwargs) -> Union[Dict[str, Any], T]:
        """
        Send a DELETE request
        
        Args:
            path: API path
            model_class: Optional Pydantic model class to convert the response to
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response data
        """
        return self._request("DELETE", path, model_class=model_class, **kwargs) 