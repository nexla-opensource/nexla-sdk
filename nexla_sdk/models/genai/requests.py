from typing import Optional, Dict, Any

from nexla_sdk.models.base import BaseModel


class GenAiConfigPayload(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    # API accepts 'active'/'paused' (OpenAPI shows lowercase); keep string passthrough
    status: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    type: Optional[str] = None  # genai_openai | genai_googleai
    data_credentials_id: Optional[int] = None


class GenAiConfigCreatePayload(BaseModel):
    name: str
    type: str  # genai_openai | genai_googleai
    config: Dict[str, Any]
    data_credentials_id: int
    description: Optional[str] = None


class GenAiOrgSettingPayload(BaseModel):
    org_id: Optional[int] = None
    gen_ai_config_id: int
    gen_ai_usage: str  # all | gen_docs | check_code

