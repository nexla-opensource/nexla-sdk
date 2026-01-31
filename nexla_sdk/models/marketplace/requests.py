from typing import List, Optional

from nexla_sdk.models.base import BaseModel


class CustodianRef(BaseModel):
    """Reference to a user for custodians payload (by id or email)."""

    id: Optional[int] = None
    email: Optional[str] = None


class CustodiansPayload(BaseModel):
    custodians: List[CustodianRef]


class MarketplaceDomainCreate(BaseModel):
    org_id: Optional[int] = None
    owner_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    custodians: Optional[CustodiansPayload] = None


class MarketplaceDomainsItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    data_set_id: int
