from typing import Any, Dict, List, Optional

from nexla_sdk.models.base import BaseModel

from .responses import TransformCodeOp


class TransformCreate(BaseModel):
    name: str
    output_type: str
    reusable: bool = True
    code_type: str
    code_encoding: str
    code: List[TransformCodeOp]

    description: Optional[str] = None
    code_config: Optional[Dict[str, Any]] = None
    custom_config: Optional[Dict[str, Any]] = None
    data_credentials_id: Optional[int] = None
    runtime_data_credentials_id: Optional[int] = None


class TransformUpdate(BaseModel):
    name: Optional[str] = None
    output_type: Optional[str] = None
    reusable: Optional[bool] = None
    code_type: Optional[str] = None
    code_encoding: Optional[str] = None
    code: Optional[List[TransformCodeOp]] = None

    description: Optional[str] = None
    code_config: Optional[Dict[str, Any]] = None
    custom_config: Optional[Dict[str, Any]] = None
    data_credentials_id: Optional[int] = None
    runtime_data_credentials_id: Optional[int] = None
