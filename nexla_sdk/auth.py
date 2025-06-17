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
    
    Supports two authentication flows as per Nexla API documentation:
    
    1. **Service Key Flow**: Uses service keys to obtain session tokens via POST to 
       /token endpoint with "Authorization: Basic <Service-Key>". Automatically 
       refreshes tokens before expiry using /token/refresh endpoint.
       
    2. **Direct Token Flow**: Uses pre-obtained access tokens directly. These tokens
       expire after a configured interval (usually 1 hour).
    
    Responsible for:
    - Obtaining session tokens using service keys (Basic auth)
    - Using directly provided access tokens (Bearer auth)  
    - Refreshing session tokens before expiry (service key flow only)
    - Ensuring valid tokens are available for API requests
    - Handling authentication retries on 401 responses
    """
    
    def __init__(self,
                 service_key: Optional[str] = None,
                 access_token: Optional[str] = None,
                 api_url: str = "https://dataops.nexla.io/nexla-api",
                 api_version: str = "v1",
                 token_refresh_margin: int = 600,
                 http_client: Optional[HttpClientInterface] = None):
        """
        Initialize the token authentication handler
        
        Args:
            service_key: Nexla service key for authentication (mutually exclusive with access_token)
            access_token: Nexla access token for direct authentication (mutually exclusive with service_key)
            api_url: Nexla API URL
            api_version: API version to use
            token_refresh_margin: Seconds before token expiry to trigger refresh (default: 10 minutes)
            http_client: HTTP client implementation (defaults to RequestsHttpClient)
        """
        self.service_key = service_key
        self.api_url = api_url.rstrip('/')
        self.api_version = api_version
        self.token_refresh_margin = token_refresh_margin
        self.http_client = http_client or RequestsHttpClient()
        
        # Session token management
        if access_token:
            self._using_direct_token = True
            self._access_token = access_token
            self._token_expiry = 0
            self.refresh_session_token()
        else:
            # Service key authentication
            self._access_token = None
            self._token_expiry = 0
            self._using_direct_token = False

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
            NexlaAuthError: If authentication fails or no service key available
        """
        if self._using_direct_token:
            raise NexlaAuthError("Cannot obtain session token when using direct access token. Service key required.")
            
        if not self.service_key:
            raise NexlaAuthError("Service key required to obtain session token.")
            
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
        
        Works for both service key tokens and direct access tokens since all valid
        tokens are refreshable according to Nexla API documentation.
        
        Raises:
            NexlaAuthError: If token refresh fails or no token available
        """
        if not self._access_token:
            if self._using_direct_token:
                raise NexlaAuthError("No access token available for refresh")
            else:
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
                if self._using_direct_token:
                    # Direct token is invalid, can't obtain a new one
                    raise NexlaAuthError("Token refresh failed - access token is invalid or expired") from e
                else:
                    # Service key token refresh failed, try obtaining a new token
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
            
        Raises:
            NexlaAuthError: If no token is available or refresh fails
        """
        if not self._access_token:
            if self._using_direct_token:
                raise NexlaAuthError("No access token available")
            else:
                # Obtain new token using service key
                self.obtain_session_token()
                return self._access_token
        
        # Check if token needs refresh (applies to both service key and direct tokens)
        current_time = time.time()
        if (self._token_expiry - current_time) < self.token_refresh_margin:
            self.refresh_session_token()
                
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
                try:
                    self.refresh_session_token()  # Refresh token (works for both service key and direct tokens)
                    
                    # Update headers with new token
                    headers["Authorization"] = f"Bearer {self.get_access_token()}"
                    
                    # Retry the request with the new token
                    return self.http_client.request(method, url, headers=headers, **kwargs)
                    
                except NexlaAuthError:
                    # If refresh fails, re-raise the original authentication error
                    raise NexlaAuthError("Authentication failed and token refresh unsuccessful") from e
            
            # For other errors, let the caller handle them
            raise
