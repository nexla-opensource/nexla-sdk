from typing import Optional, Dict, Any


class NexlaError(Exception):
    """Base exception for all Nexla errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AuthenticationError(NexlaError):
    """Raised when authentication fails."""
    pass


class AuthorizationError(NexlaError):
    """Raised when user lacks permission."""
    pass


class NotFoundError(NexlaError):
    """Raised when a resource is not found."""
    pass


class ValidationError(NexlaError):
    """Raised when request validation fails."""
    pass


class RateLimitError(NexlaError):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ServerError(NexlaError):
    """Raised when server returns 5xx error."""
    pass


class ResourceConflictError(NexlaError):
    """Raised when resource conflicts occur."""
    pass


class CredentialError(NexlaError):
    """Raised when credential validation fails."""
    pass


class FlowError(NexlaError):
    """Raised when flow operations fail."""
    pass


class TransformError(NexlaError):
    """Raised when transform operations fail."""
    pass
