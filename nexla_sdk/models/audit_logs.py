"""
Audit Logs models for the Nexla SDK
"""
from typing import List, Optional, Union, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class AssociationResource(BaseModel):
    """Information about resource relationships that were modified"""
    type: str = Field(..., description="The resource type of the resource whose relationship with this resource was modified")
    id: int = Field(..., description="The ID of the resource whose relationship with this resource was modified")


class AuditLogUser(BaseModel):
    """User details in audit log entries"""
    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email address")


class AuditLogEntry(BaseModel):
    """An entry in the audit log for a resource"""
    id: int = Field(..., description="Unique ID of this change event")
    item_type: str = Field(..., description="The type of resource that the change was performed on")
    item_id: int = Field(..., description="Unique ID of resource that the change was performed on")
    event: str = Field(..., description="The type of change event that was executed")
    change_summary: List[str] = Field(..., description="Summary of types of changes executed during this change event")
    object_changes: Optional[dict] = Field(None, description="Before and after information on each property that was modified")
    association_resource: Optional[AssociationResource] = Field(None, description="Information about the resource relationship that was modified")
    request_ip: Optional[str] = Field(None, description="IP Address of the device where this change event request originated")
    request_user_agent: Optional[str] = Field(None, description="User Agent of the browser where this change event request originated")
    request_url: Optional[str] = Field(None, description="Nexla UI or API URL that was accessed by the user to trigger this change event")
    user: Optional[AuditLogUser] = Field(None, description="Details about the user who triggered this change event")
    impersonator_id: Optional[str] = Field(None, description="ID of Nexla support team member if changes were made on behalf of a user")
    org_id: Optional[int] = Field(None, description="The ID of the organization that this resource belongs to")
    owner_id: Optional[int] = Field(None, description="The ID of the user that this resource belongs to")
    owner_email: Optional[str] = Field(None, description="Email ID of the user that this resource belongs to")
    created_at: datetime = Field(..., description="When this change event was created") 