from typing import Optional, List

from nexla_sdk.models.base import BaseModel


class OrgCustodianRef(BaseModel):
    """Reference to a user for organization custodians (by id or email)."""
    id: Optional[int] = None
    email: Optional[str] = None


class OrgCustodiansPayload(BaseModel):
    """Payload for organization custodians endpoints."""
    custodians: List[OrgCustodianRef]

