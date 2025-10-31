from typing import Any, Dict, Optional

from nexla_sdk.models.base import BaseModel


class AuthConfigPayload(BaseModel):
    id: Optional[int] = None
    owner_id: Optional[int] = None
    org_id: Optional[int] = None
    uid: Optional[str] = None
    protocol: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    global_: Optional[bool] = None
    enabled_by_default: Optional[bool] = None
    auto_create_users_enabled: Optional[bool] = None
    name_identifier_format: Optional[str] = None
    nexla_base_url: Optional[str] = None
    service_entity_id: Optional[str] = None
    assertion_consumer_url: Optional[str] = None
    idp_entity_id: Optional[str] = None
    idp_sso_target_url: Optional[str] = None
    idp_slo_target_url: Optional[str] = None
    idp_cert: Optional[str] = None
    security_settings: Optional[Dict[str, Any]] = None
    metadata: Optional[str] = None
    oidc_domain: Optional[str] = None
    oidc_keys_url_key: Optional[str] = None
    oidc_id_claims: Optional[Dict[str, Any]] = None
    oidc_access_claims: Optional[Dict[str, Any]] = None

