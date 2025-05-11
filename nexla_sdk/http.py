"""
HTTP client interface and implementations for Nexla SDK
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union

import requests


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
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response or {}


class RequestsHttpClient(HttpClientInterface):
    """
    HTTP client implementation using the requests library
    """
    
    def request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Union[Dict[str, Any], None]:
        """
        Send an HTTP request using the requests library
        
        Args:
            method: HTTP method
            url: Request URL
            headers: Request headers
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response data as dictionary or None for 204 No Content responses
            
        Raises:
            HttpClientError: If the request fails
        """
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            
            # Return None for 204 No Content
            if response.status_code == 204:
                return None
                
            # Parse JSON response
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            # Create standardized error with status code and response data
            error_data = {}
            if response.content:
                try:
                    error_data = response.json()
                except ValueError:
                    error_data = {"raw_text": response.text}
                    
            raise HttpClientError(
                message=str(e),
                status_code=response.status_code,
                response=error_data
            ) from e
            
        except requests.exceptions.RequestException as e:
            # Handle general request exceptions (network errors, etc.)
            raise HttpClientError(message=str(e)) from e 