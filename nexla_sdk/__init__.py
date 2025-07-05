"""Nexla Python SDK for data integration and automation."""

__version__ = "0.1.0"

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
from nexla_sdk.utils.exceptions import (
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
