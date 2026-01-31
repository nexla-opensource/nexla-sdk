from datetime import datetime
from typing import List, Optional

from pydantic import Field

from nexla_sdk.models.base import BaseModel
from nexla_sdk.models.common import Organization, Owner


class ProjectDataFlow(BaseModel):
    """Project data flow information."""

    id: int
    project_id: int
    data_source_id: Optional[int] = None
    data_set_id: Optional[int] = None
    data_sink_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Project(BaseModel):
    """Project response model."""

    id: int
    owner: Owner
    org: Organization
    name: str
    description: str
    access_roles: List[str]

    # Optional fields
    data_flows: List[ProjectDataFlow] = Field(default_factory=list)
    flows: List[ProjectDataFlow] = Field(default_factory=list)
    client_identifier: Optional[str] = None
    client_url: Optional[str] = None
    flows_count: Optional[int] = None
    tags: List[str] = Field(default_factory=list)
    copied_from_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
