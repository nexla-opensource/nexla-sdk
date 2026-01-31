from datetime import datetime
from typing import Any, Dict, Optional

from nexla_sdk.models.base import BaseModel


class AuthConfig(BaseModel):
    id: int
    owner: Optional[Dict[str, Any]] = None
    org: Optional[Dict[str, Any]] = None
    uid: Optional[str] = None
    protocol: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    global_: Optional[bool] = None
    auto_create_users_enabled: Optional[bool] = None
    name_identifier_format: Optional[str] = None
    nexla_base_url: Optional[str] = None
    service_entity_id: Optional[str] = None
    assertion_consumer_url: Optional[str] = None
    logout_url: Optional[str] = None
    metadata_url: Optional[str] = None
    idp_entity_id: Optional[str] = None
    idp_sso_target_url: Optional[str] = None
    idp_slo_target_url: Optional[str] = None
    idp_cert: Optional[str] = None
    security_settings: Optional[str] = None
    oidc_domain: Optional[str] = None
    oidc_keys_url_key: Optional[str] = None
    oidc_token_verify_url: Optional[str] = None
    oidc_id_claims: Optional[str] = None
    oidc_access_claims: Optional[str] = None
    client_config: Optional[Dict[str, Any]] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
