"""
Webhook models for the Nexla SDK
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .common import Resource, PaginatedList


class WebhookConfig(Resource):
    """Webhook configuration resource model"""
    url: str = Field(..., description="Webhook URL")
    headers: Optional[Dict[str, str]] = Field(None, description="HTTP headers to include")
    method: str = Field(default="POST", description="HTTP method")
    auth_type: Optional[str] = Field(None, description="Authentication type")
    auth_config: Optional[Dict[str, Any]] = Field(None, description="Authentication configuration")
    is_active: bool = Field(default=True, description="Whether the webhook is active")
    owner_id: Optional[str] = Field(None, description="Owner user ID")
    org_id: Optional[str] = Field(None, description="Organization ID")


# Alias for API compatibility
Webhook = WebhookConfig


class WebhookList(PaginatedList[WebhookConfig]):
    """Paginated list of webhook configurations"""
    pass


class WebhookEvent(BaseModel):
    """Webhook event data"""
    event_type: str = Field(..., description="Type of event")
    event_id: str = Field(..., description="Event ID")
    timestamp: datetime = Field(..., description="Event timestamp")
    payload: Dict[str, Any] = Field(..., description="Event payload")
    source: Optional[str] = Field(None, description="Event source")


class WebhookResponse(BaseModel):
    """Response from a webhook call"""
    success: bool = Field(..., description="Whether the webhook call was successful")
    status_code: int = Field(..., description="HTTP status code")
    message: Optional[str] = Field(None, description="Response message")
    response_body: Optional[Dict[str, Any]] = Field(None, description="Response body")


class WebhookDelivery(BaseModel):
    """Webhook delivery attempt details"""
    id: str = Field(..., description="Delivery ID")
    webhook_id: str = Field(..., description="Webhook ID")
    event_id: str = Field(..., description="Event ID")
    timestamp: datetime = Field(..., description="Delivery timestamp")
    status: str = Field(..., description="Delivery status (success/failure)")
    status_code: Optional[int] = Field(None, description="HTTP status code")
    response: Optional[WebhookResponse] = Field(None, description="Response details")
    error: Optional[str] = Field(None, description="Error message if failed")
    retry_count: int = Field(default=0, description="Number of retry attempts")


class WebhookDeliveryList(PaginatedList[WebhookDelivery]):
    """Paginated list of webhook deliveries"""
    pass


class WebhookTestResult(BaseModel):
    """Result of testing a webhook"""
    success: bool = Field(..., description="Whether the test was successful")
    timestamp: datetime = Field(..., description="Test timestamp")
    request: Dict[str, Any] = Field(..., description="Request details sent")
    response: WebhookResponse = Field(..., description="Response from the webhook endpoint") 