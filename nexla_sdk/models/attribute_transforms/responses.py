from datetime import datetime
from typing import Any, Dict, List, Optional

from nexla_sdk.models.base import BaseModel


class AttributeTransform(BaseModel):
    id: int
    name: str
    resource_type: Optional[str] = None
    reusable: Optional[bool] = None
    owner: Optional[Dict[str, Any]] = None
    org: Optional[Dict[str, Any]] = None
    access_roles: Optional[Dict[str, Any]] = None
    data_credentials: Optional[Dict[str, Any]] = None
    runtime_data_credentials: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    code_type: Optional[str] = None
    output_type: Optional[str] = None
    code_config: Optional[Dict[str, Any]] = None
    custom_config: Optional[Dict[str, Any]] = None
    code_encoding: Optional[str] = None
    code: Optional[str] = None
    managed: Optional[bool] = None
    data_sets: Optional[List[int]] = None
    copied_from_id: Optional[int] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    tags: Optional[List[str]] = None

