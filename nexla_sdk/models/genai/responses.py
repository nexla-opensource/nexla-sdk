from datetime import datetime
from typing import Any, Dict, List, Optional

from nexla_sdk.models.base import BaseModel


class GenAiConfig(BaseModel):
    id: int
    name: Optional[str] = None
    provider: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class GenAiOrgSetting(BaseModel):
    id: int
    org_id: Optional[int] = None
    gen_ai_usage: Optional[str] = None
    active_config: Optional[Dict[str, Any]] = None
    configs: Optional[List[Dict[str, Any]]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ActiveConfigView(BaseModel):
    gen_ai_usage: Optional[str] = None
    active_config: Optional[Dict[str, Any]] = None
