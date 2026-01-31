"""Webhook request models."""

from typing import Optional

from nexla_sdk.models.base import BaseModel


class WebhookSendOptions(BaseModel):
    """Options for sending data to a webhook.

    Attributes:
        include_headers: Include custom headers in ingested records.
            Custom headers will be added as `header_<header_name>` attributes.
            Standard headers like `Authorization` and `Content-Type` are ignored.
        include_url_params: Include custom query parameters in ingested records.
            Custom params will be added as `url_param_<param_name>` attributes.
            Standard params like `api_key` are ignored.
        force_schema_detection: Force schema detection for this record.
            Normally, schema detection only happens for the first few records.
            Set to True to force detection on every record.
    """

    include_headers: Optional[bool] = None
    include_url_params: Optional[bool] = None
    force_schema_detection: Optional[bool] = None
