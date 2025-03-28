"""
Transform models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList


class Transform(Resource):
    """Transform resource model"""
    transform_type: str = Field(..., description="Type of transform")
    code: Optional[str] = Field(None, description="Transform code")
    language: Optional[str] = Field(None, description="Code language")
    is_public: bool = Field(default=False, description="Whether the transform is public")
    owner_id: Optional[str] = Field(None, description="Owner user ID")
    org_id: Optional[str] = Field(None, description="Organization ID")


class TransformList(PaginatedList[Transform]):
    """Paginated list of transforms"""
    pass


class AttributeTransform(Resource):
    """Attribute transform resource model"""
    transform_type: str = Field(..., description="Type of attribute transform")
    code: Optional[str] = Field(None, description="Transform code")
    language: Optional[str] = Field(None, description="Code language")
    is_public: bool = Field(default=False, description="Whether the transform is public")
    owner_id: Optional[str] = Field(None, description="Owner user ID")
    org_id: Optional[str] = Field(None, description="Organization ID")


class AttributeTransformList(PaginatedList[AttributeTransform]):
    """Paginated list of attribute transforms"""
    pass 