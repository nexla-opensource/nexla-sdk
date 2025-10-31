from datetime import datetime
from typing import Any, Dict, Optional

from nexla_sdk.models.base import BaseModel


class AsyncTask(BaseModel):
    id: int
    type: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AsyncTaskResult(BaseModel):
    task_id: Optional[int] = None
    result: Optional[Dict[str, Any]] = None


class DownloadLink(BaseModel):
    url: str
    expires_at: Optional[datetime] = None

