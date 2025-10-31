from datetime import datetime
from typing import Optional

from nexla_sdk.models.base import BaseModel


class MarketplaceDomain(BaseModel):
    id: int
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    org_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MarketplaceDomainsItem(BaseModel):
    id: int
    domain_id: Optional[int] = None
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
