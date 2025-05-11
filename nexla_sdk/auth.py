"""
Authentication utilities for the Nexla SDK
"""
import logging
import time
from typing import Dict, Any, Optional, Union

from .exceptions import NexlaError, NexlaAuthError, NexlaAPIError
from .http import HttpClientInterface, RequestsHttpClient, HttpClientError

logger = logging.getLogger(__name__)


class TokenAuthHandler:
    """
    Handles authentication and token management for Nexla API
    
    Responsible for:
    - Obtaining access tokens using service key
    - Refreshing tokens before they expire
    - Ensuring valid tokens are available for API requests
    """
    
    def __init__(self,
                 service_key: str,
                 api_url: str,
                 api_version: str,
                 token_refresh_margin: int = 300,
                 http_client: Optional[HttpClientInterface] = None):
        """
        Initialize the token authentication handler
        
        Args:
            service_key: Nexla service key for authentication
            api_url: Nexla API URL
            api_version: API version to use
            token_refresh_margin: Seconds before token expiry to trigger refresh (default: 5 minutes)
            http_client: HTTP client implementation (defaults to RequestsHttpClient)
        """
        self.service_key = service_key
        self.api_url = api_url.rstrip('/')
        self.api_version = api_version
        self.token_refresh_margin = token_refresh_margin
        self.http_client = http_client or RequestsHttpClient()
        
        # Session token management
        self._access_token = None
        self._token_expiry = 0

    def get_access_token(self) -> str:
        """
        Get the current access token
        
        Returns:
            Current access token
            
        Raises:
            NexlaAuthError: If no valid token is available
        """
        if not self._access_token:
            raise NexlaAuthError("No access token available. Authentication required.")
        return self._access_token

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
            token_data = self.http_client.request("POST", url, headers=headers)
            self._access_token = token_data.get("access_token")
            # Calculate expiry time (current time + expires_in seconds)
            expires_in = token_data.get("expires_in", 3600)
            self._token_expiry = time.time() + expires_in
            
            logger.debug("Session token obtained successfully")
            
        except HttpClientError as e:
            if getattr(e, 'status_code', None) == 401:
                raise NexlaAuthError("Authentication failed. Check your service key.") from e
            
            error_msg = f"Failed to obtain session token: {e}"
            error_data = getattr(e, 'response', {})
            
            if error_data:
                if "message" in error_data:
                    error_msg = f"Authentication error: {error_data['message']}"
                elif "error" in error_data:
                    error_msg = f"Authentication error: {error_data['error']}"
                    
            raise NexlaAPIError(
                error_msg, 
                status_code=getattr(e, 'status_code', None), 
                response=error_data
            ) from e
            
        except Exception as e:
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
            token_data = self.http_client.request("POST", url, headers=headers)
            self._access_token = token_data.get("access_token")
            # Calculate expiry time (current time + expires_in seconds)
            expires_in = token_data.get("expires_in", 3600)
            self._token_expiry = time.time() + expires_in
            
            logger.debug("Session token refreshed successfully")
            
        except HttpClientError as e:
            if getattr(e, 'status_code', None) == 401:
                # If refresh fails with 401, try obtaining a new token
                logger.warning("Token refresh failed with 401, obtaining new session token")
                self.obtain_session_token()
                return
                
            error_msg = f"Failed to refresh session token: {e}"
            error_data = getattr(e, 'response', {})
            
            if error_data:
                if "message" in error_data:
                    error_msg = f"Token refresh error: {error_data['message']}"
                elif "error" in error_data:
                    error_msg = f"Token refresh error: {error_data['error']}"
                    
            raise NexlaAPIError(
                error_msg, 
                status_code=getattr(e, 'status_code', None), 
                response=error_data
            ) from e
            
        except Exception as e:
            raise NexlaError(f"Failed to refresh session token: {e}") from e
    
    def ensure_valid_token(self) -> str:
        """
        Ensures a valid session token is available, refreshing if necessary
        
        Returns:
            Current valid access token
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
                
        return self._access_token
        
    def execute_authenticated_request(self, method: str, url: str, headers: Dict[str, str], **kwargs) -> Union[Dict[str, Any], None]:
        """
        Execute a request with authentication handling
        
        Args:
            method: HTTP method
            url: Full URL to call
            headers: HTTP headers
            **kwargs: Additional arguments to pass to the HTTP client
            
        Returns:
            API response as a dictionary or None for 204 No Content responses
            
        Raises:
            NexlaAuthError: If authentication fails
            NexlaAPIError: If the API returns an error
        """
        # Get a valid token
        access_token = self.ensure_valid_token()
        
        # Add authorization header
        headers["Authorization"] = f"Bearer {access_token}"
        
        try:
            return self.http_client.request(method, url, headers=headers, **kwargs)
            
        except HttpClientError as e:
            if getattr(e, 'status_code', None) == 401:
                # If authentication failed, try refreshing the token
                logger.warning("Request failed with 401, refreshing session token and retrying")
                self.obtain_session_token()  # Get a new token
                
                # Update headers with new token
                headers["Authorization"] = f"Bearer {self.get_access_token()}"
                
                # Retry the request with the new token
                return self.http_client.request(method, url, headers=headers, **kwargs)
            
            # For other errors, let the caller handle them
            raise 