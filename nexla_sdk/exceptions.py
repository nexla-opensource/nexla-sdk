from typing import Optional, Dict, Any, List
import traceback


class NexlaError(Exception):
    """Base exception for all Nexla errors."""
    
    def __init__(self, 
                 message: str, 
                 details: Optional[Dict[str, Any]] = None,
                 operation: Optional[str] = None,
                 resource_type: Optional[str] = None,
                 resource_id: Optional[str] = None,
                 step: Optional[str] = None,
                 context: Optional[Dict[str, Any]] = None,
                 original_error: Optional[Exception] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.operation = operation
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.step = step
        self.context = context or {}
        self.original_error = original_error
        
    def __str__(self):
        """Provide detailed error information."""
        parts = []
        
        if self.step:
            parts.append(f"Step: {self.step}")
        if self.operation:
            parts.append(f"Operation: {self.operation}")
        if self.resource_type:
            parts.append(f"Resource: {self.resource_type}")
        if self.resource_id:
            parts.append(f"ID: {self.resource_id}")
            
        parts.append(f"Error: {self.message}")
        
        if self.details:
            parts.append(f"Details: {self.details}")
        if self.context:
            parts.append(f"Context: {self.context}")
        if self.original_error:
            parts.append(f"Original Error: {self.original_error}")
            
        return " | ".join(parts)
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get structured error information."""
        return {
            "message": self.message,
            "step": self.step,
            "operation": self.operation,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "details": self.details,
            "context": self.context,
            "original_error": str(self.original_error) if self.original_error else None
        }


class AuthenticationError(NexlaError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, operation="authentication", **kwargs)


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
    
    def __init__(self, message: str, credential_id: Optional[str] = None, **kwargs):
        super().__init__(message, 
                         operation="credential_validation",
                         resource_type="credential",
                         resource_id=credential_id,
                         **kwargs)


class FlowError(NexlaError):
    """Raised when flow operations fail."""
    
    def __init__(self, message: str, flow_id: Optional[str] = None, flow_step: Optional[str] = None, **kwargs):
        super().__init__(message, 
                         operation="flow_operation",
                         resource_type="flow",
                         resource_id=flow_id,
                         step=flow_step,
                         **kwargs)


class TransformError(NexlaError):
    """Raised when transform operations fail."""
    
    def __init__(self, message: str, transform_id: Optional[str] = None, **kwargs):
        super().__init__(message, 
                         operation="transform_operation",
                         resource_type="transform",
                         resource_id=transform_id,
                         **kwargs)
