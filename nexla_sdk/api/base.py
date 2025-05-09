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
        # Use the client's request method which handles authentication
        response = self.client.request(method, path, **kwargs)
        
        # Convert to model if specified
        if model_class:
            logger.debug(f"Converting response to model {model_class.__name__}")
            result = self.client._convert_to_model(response, model_class)
            logger.debug(f"Converted model result: {result}")
            return result
            
        return response
        
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