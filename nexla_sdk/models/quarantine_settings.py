"""
Quarantine Settings models for the Nexla SDK

Nexla detects errors during different stages of data flow such as ingestion, 
transformation, and output. Error records are quarantined and accessible to the user 
via APIs as well as files. With Quarantine Data Export Settings, you can configure 
Nexla to write files containing information about erroneous records across all resources 
owned by a user.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from .common import ResourceType
from .credentials import Credential


class QuarantineConfig(BaseModel):
    """Configuration for quarantine data export settings"""
    start_cron: str = Field(..., description="The interval at which Nexla should scan all quarantined records", alias="start.cron")
    path: str = Field(..., description="The base folder where all quarantined records will be exported")
    
    model_config = ConfigDict(populate_by_field_name=True)


class QuarantineResourceType(str, Enum):
    """Resource types for quarantine settings"""
    ORG = "ORG"
    USER = "USER"
    FLOW = "FLOW"
    PIPELINE = "PIPELINE"
    DATA_FLOW = "DATA_FLOW"
    CUSTOM_DATA_FLOW = "CUSTOM_DATA_FLOW"
    SOURCE = "SOURCE"
    DATASET = "DATASET"
    SINK = "SINK"


class QuarantineSettingsOwner(BaseModel):
    """Owner information for quarantine settings"""
    id: int = Field(..., description="Owner ID")
    full_name: str = Field(..., description="Owner's full name")
    email: str = Field(..., description="Owner's email address")
    email_verified_at: Optional[datetime] = Field(None, description="When the email was verified")


class QuarantineSettingsOrganization(BaseModel):
    """Organization information for quarantine settings"""
    id: int = Field(..., description="Organization ID")
    name: str = Field(..., description="Organization name")
    email_domain: str = Field(..., description="Organization email domain")
    email: Optional[str] = Field(None, description="Organization email")
    client_identifier: Optional[str] = Field(None, description="Client identifier")
    org_webhook_host: Optional[str] = Field(None, description="Organization webhook host")


class QuarantineSettings(BaseModel):
    """Quarantine data export settings"""
    id: int = Field(..., description="Unique ID of the quarantine settings")
    owner: QuarantineSettingsOwner = Field(..., description="Owner information")
    org: QuarantineSettingsOrganization = Field(..., description="Organization information")
    resource_type: QuarantineResourceType = Field(..., description="Type of resource associated with these settings")
    resource_id: int = Field(..., description="ID of the resource associated with these settings")
    config: QuarantineConfig = Field(..., description="Configuration for quarantine data export")
    data_credentials_id: int = Field(..., description="ID of the data credentials for exporting error data")
    credentials_type: str = Field(..., description="Type of the credentials used for exporting")
    data_credentials: Optional[Credential] = Field(None, description="Data credentials details")


class CreateQuarantineSettingsRequest(BaseModel):
    """Request model for creating quarantine data export settings"""
    data_credentials_id: int = Field(..., description="Nexla data credential ID to a file storage system")
    config: QuarantineConfig = Field(..., description="Configuration for quarantine data export")


class UpdateQuarantineSettingsRequest(BaseModel):
    """Request model for updating quarantine data export settings"""
    data_credentials_id: Optional[int] = Field(None, description="Nexla data credential ID to a file storage system")
    config: Optional[QuarantineConfig] = Field(None, description="Configuration for quarantine data export") 