"""
Session management API for the Nexla SDK
"""
import base64
from typing import Dict, Any, Optional

from .base import BaseAPI
from ..models.session import LoginResponse, LogoutResponse

class SessionAPI(BaseAPI):
    """API client for session management operations"""

    def login_with_basic_auth(self, email: str, password: str) -> LoginResponse:
        """
        Log in with basic authentication (email and password)
        
        Args:
            email: User email
            password: User password
            
        Returns:
            LoginResponse: Response containing session information
            
        Raises:
            NexlaAuthError: If authentication fails
        """
        # Create basic auth credentials
        credentials = base64.b64encode(f"{email}:{password}".encode()).decode()
        
        # Send login request
        response = self._post(
            "/token",
            model_class=LoginResponse,
            headers={"Authorization": f"Basic {credentials}"}
        )
        
        # Update client token
        if hasattr(self.client, "api_key") and response.access_token:
            self.client.api_key = response.access_token
            
        return response
    
    def logout(self) -> LogoutResponse:
        """
        Log out and invalidate the current session token
        
        Returns:
            LogoutResponse: Response confirming successful logout
            
        Raises:
            NexlaAuthError: If not authenticated or logout fails
        """
        response = self._post(
            "/token/logout",
            model_class=LogoutResponse
        )
        
        # Clear client token
        if hasattr(self.client, "api_key"):
            self.client.api_key = None
            
        return response 