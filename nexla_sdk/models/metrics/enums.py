from enum import Enum


class ResourceType(str, Enum):
    """Valid resource types for metrics endpoints."""

    # For resource metrics endpoints (/{resource_type}/{resource_id}/metrics)
    DATA_SOURCES = "data_sources"
    DATA_SINKS = "data_sinks"
    DATA_SETS = "data_sets"


class UserMetricResourceType(str, Enum):
    """Valid resource types for user metrics endpoints."""

    # For user metrics endpoints (/users/{user_id}/metrics)
    SOURCE = "SOURCE"
    SINK = "SINK"
