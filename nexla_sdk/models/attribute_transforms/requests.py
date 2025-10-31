from typing import Any, Dict, Optional

from nexla_sdk.models.base import BaseModel


class AttributeTransformCreate(BaseModel):
    name: str
    output_type: str
    reusable: bool = True
    code_type: str
    code_encoding: str
    code: str

    description: Optional[str] = None
    code_config: Optional[Dict[str, Any]] = None
    custom_config: Optional[Dict[str, Any]] = None
    data_credentials_id: Optional[int] = None
    runtime_data_credentials_id: Optional[int] = None


class AttributeTransformUpdate(BaseModel):
    name: Optional[str] = None
    output_type: Optional[str] = None
    reusable: Optional[bool] = None
    code_type: Optional[str] = None
    code_encoding: Optional[str] = None
    code: Optional[str] = None

    description: Optional[str] = None
    code_config: Optional[Dict[str, Any]] = None
    custom_config: Optional[Dict[str, Any]] = None
    data_credentials_id: Optional[int] = None
    runtime_data_credentials_id: Optional[int] = None

