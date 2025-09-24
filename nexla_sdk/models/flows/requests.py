from typing import Optional
from nexla_sdk.models.base import BaseModel


class FlowCopyOptions(BaseModel):
    """Options for copying a flow."""
    reuse_data_credentials: bool = False
    copy_access_controls: bool = False
    copy_dependent_data_flows: bool = False
    owner_id: Optional[int] = None
    org_id: Optional[int] = None