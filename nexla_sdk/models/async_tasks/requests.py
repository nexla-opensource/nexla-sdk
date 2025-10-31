from typing import Any, Dict, Optional

from nexla_sdk.models.base import BaseModel


class AsyncTaskCreate(BaseModel):
    """Generic async task payload wrapper aligned with OpenAPI AsyncTaskPayload.

    Fields:
        type: The task type (e.g., BulkDeleteNotifications)
        priority: Optional task priority
        arguments: Arguments for the task
    """
    type: str
    priority: Optional[int] = None
    arguments: Dict[str, Any]
