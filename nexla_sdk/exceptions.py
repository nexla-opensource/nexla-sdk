"""
Nexla SDK Exceptions
"""
from typing import Optional, Dict, Any


class NexlaError(Exception):
    """Base exception for Nexla SDK"""
    pass


class NexlaAuthError(NexlaError):
    """Authentication error"""
    pass


class NexlaAPIError(NexlaError):
    """API error"""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class NexlaValidationError(NexlaError):
    """Data validation error"""
    pass


class NexlaClientError(NexlaError):
    """Client configuration error"""
    pass


class NexlaNotFoundError(NexlaAPIError):
    """Resource not found error"""
    
    def __init__(self, message: str, resource_type: Optional[str] = None, resource_id: Optional[str] = None):
        super().__init__(message, status_code=404)
        self.resource_type = resource_type
        self.resource_id = resource_id 