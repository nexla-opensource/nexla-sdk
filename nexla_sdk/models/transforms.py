"""
Transform models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList, ResourceType, ResourceID, Status
from .access import AccessRole, Owner, Organization
from .credentials import Credential

class CodeType(str, Enum):
    """Code type enumeration for transforms"""
    JOLT_STANDARD = "jolt_standard"
    JOLT_CUSTOM = "jolt_custom"
    PYTHON = "python"
    JAVASCRIPT = "javascript"


class OutputType(str, Enum):
    """Output type enumeration for transforms"""
    RECORD = "record"
    ATTRIBUTE = "attribute"


class CodeEncoding(str, Enum):
    """Code encoding enumeration for transforms"""
    NONE = "none"
    BASE64 = "base64"


class JoltOperation(BaseModel):
    """Jolt operation for record transforms"""
    operation: str = Field(..., description="Jolt operation name")
    spec: Dict[str, Any] = Field(..., description="Jolt specification")


class CustomConfig(BaseModel):
    """Custom configuration for transforms"""
    # This is a placeholder for custom configuration properties
    # The actual structure depends on the transform type
    pass


class Transform(Resource):
    """Transform resource model"""
    resource_type: ResourceType = Field(ResourceType.TRANSFORM, description="Resource type")
    reusable: bool = Field(..., description="Whether the transform is reusable")
    owner: Optional[Owner] = Field(None, description="Owner of the transform")
    org: Optional[Organization] = Field(None, description="Organization of the transform")
    access_roles: Optional[List[AccessRole]] = Field(None, description="Access roles for this transform")
    data_credentials: Optional[Credential] = Field(None, description="Data credentials for this transform")
    runtime_data_credentials: Optional[Credential] = Field(None, description="Runtime data credentials")
    description: Optional[str] = Field(None, description="Transform description")
    code_type: CodeType = Field(..., description="Type of code used in the transform")
    output_type: OutputType = Field(..., description="Type of output for this transform")
    code_config: Optional[Dict[str, Any]] = Field(None, description="Code configuration")
    custom_config: Optional[Dict[str, Any]] = Field(None, description="Custom configuration")
    code_encoding: CodeEncoding = Field(..., description="Code encoding method")
    code: Union[List[JoltOperation], List[Dict[str, Any]], str] = Field(..., description="Transform code")
    managed: bool = Field(default=False, description="Whether the transform is managed")
    data_sets: Optional[List[int]] = Field(None, description="Associated data set IDs")
    copied_from_id: Optional[int] = Field(None, description="ID of the transform this was copied from")
    tags: Optional[List[str]] = Field(None, description="Tags for this transform")
    public: Optional[bool] = Field(None, description="Whether the transform is public")


class TransformList(PaginatedList[Transform]):
    """Paginated list of transforms"""
    pass


class AttributeTransform(Transform):
    """Attribute transform resource model"""
    output_type: OutputType = Field(OutputType.ATTRIBUTE, description="Type of output (always attribute)")
    code: str = Field(..., description="Transform code (usually Base64 encoded)")


class AttributeTransformList(PaginatedList[AttributeTransform]):
    """Paginated list of attribute transforms"""
    pass


class CreateTransformRequest(BaseModel):
    """Request to create a new transform"""
    name: str = Field(..., description="Name of the transform")
    description: Optional[str] = Field(None, description="Description of the transform")
    output_type: OutputType = Field(..., description="Type of output for this transform")
    reusable: bool = Field(..., description="Whether the transform is reusable")
    code_type: CodeType = Field(..., description="Type of code used in the transform")
    code_encoding: CodeEncoding = Field(..., description="Code encoding method")
    code: Union[List[Dict[str, Any]], str] = Field(..., description="Transform code")
    custom_config: Optional[Dict[str, Any]] = Field(None, description="Custom configuration")
    tags: Optional[List[str]] = Field(None, description="Tags for this transform")


class UpdateTransformRequest(BaseModel):
    """Request to update a transform"""
    name: str = Field(..., description="Name of the transform")
    description: Optional[str] = Field(None, description="Description of the transform")
    data_credentials_id: Optional[int] = Field(None, description="Credential ID for accessing code repository")
    runtime_data_credentials_id: Optional[int] = Field(None, description="Runtime credential ID")
    output_type: OutputType = Field(..., description="Type of output for this transform")
    code_type: CodeType = Field(..., description="Type of code used in the transform")
    code_encoding: CodeEncoding = Field(..., description="Code encoding method")
    code: Union[List[Dict[str, Any]], str] = Field(..., description="Transform code")
    reusable: bool = Field(..., description="Whether the transform is reusable")
    tags: Optional[List[str]] = Field(None, description="Tags for this transform")
    custom_config: Optional[Dict[str, Any]] = Field(None, description="Custom configuration")


class CreateAttributeTransformRequest(BaseModel):
    """Request to create an attribute transform"""
    name: str = Field(..., description="Name of the attribute transform")
    description: Optional[str] = Field(None, description="Description of the attribute transform")
    output_type: OutputType = Field(OutputType.ATTRIBUTE, description="Type of output (always attribute)")
    reusable: bool = Field(True, description="Whether the transform is reusable (always true)")
    code_type: CodeType = Field(..., description="Type of code (python or javascript)")
    code_encoding: CodeEncoding = Field(CodeEncoding.BASE64, description="Code encoding (always base64)")
    code: str = Field(..., description="Base64-encoded transform code")
    custom_config: Optional[Dict[str, Any]] = Field(None, description="Custom configuration")
    tags: Optional[List[str]] = Field(None, description="Tags for this transform")


class DeleteTransformResponse(BaseModel):
    """Response from deleting a transform"""
    code: str = Field(..., description="Response status code")
    message: str = Field(..., description="Response status text") 