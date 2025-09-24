"""Nexla Python SDK for data integration and automation."""

# Package version
try:
    from importlib.metadata import version, PackageNotFoundError  # Python 3.8+
except Exception:  # pragma: no cover
    version = None
    PackageNotFoundError = Exception

try:  # Prefer distribution name for accurate version resolution
    __version__ = version("nexla-sdk") if version else "unknown"
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

# Import main client
from nexla_sdk.client import NexlaClient

# Import resources
from nexla_sdk.resources import (
    CredentialsResource,
    FlowsResource,
    SourcesResource,
    DestinationsResource,
    NexsetsResource,
    LookupsResource,
    UsersResource,
    OrganizationsResource,
    TeamsResource,
    ProjectsResource,
    NotificationsResource,
    MetricsResource,
)

# Import common models
from nexla_sdk.models import (
    BaseModel,
    Owner,
    Organization,
    Connector,
    LogEntry,
    FlowNode,
)

# Import exceptions
from nexla_sdk.exceptions import (
    NexlaError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    ResourceConflictError,
    CredentialError,
    FlowError,
    TransformError,
)

# Import enums
from nexla_sdk.models.enums import (
    AccessRole,
    ResourceStatus,
    ResourceType,
    NotificationLevel,
    NotificationChannel,
    UserTier,
    UserStatus,
    OrgMembershipStatus,
    ConnectorCategory,
)

__all__ = [
    # Client
    'NexlaClient',
    
    # Resources
    'CredentialsResource',
    'FlowsResource',
    'SourcesResource',
    'DestinationsResource',
    'NexsetsResource',
    'LookupsResource',
    'UsersResource',
    'OrganizationsResource',
    'TeamsResource',
    'ProjectsResource',
    'NotificationsResource',
    'MetricsResource',
    
    # Models
    'BaseModel',
    'Owner',
    'Organization',
    'Connector',
    'LogEntry',
    'FlowNode',
    
    # Exceptions
    'NexlaError',
    'AuthenticationError',
    'AuthorizationError',
    'NotFoundError',
    'ValidationError',
    'RateLimitError',
    'ServerError',
    'ResourceConflictError',
    'CredentialError',
    'FlowError',
    'TransformError',
    
    # Enums
    'AccessRole',
    'ResourceStatus',
    'ResourceType',
    'NotificationLevel',
    'NotificationChannel',
    'UserTier',
    'UserStatus',
    'OrgMembershipStatus',
    'ConnectorCategory',
]
