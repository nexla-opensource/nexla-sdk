"""Webhook response models."""

from typing import Optional

from nexla_sdk.models.base import BaseModel


class WebhookResponse(BaseModel):
    """Response from sending data to a webhook.

    Attributes:
        dataset_id: Nexset ID of the Nexset receiving the record(s).
        processed: Number of records successfully processed.
    """

    dataset_id: Optional[int] = None
    processed: Optional[int] = None
