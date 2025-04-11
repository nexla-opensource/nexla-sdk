"""
Webhooks API endpoints
"""
from typing import Dict, Any, List, Optional

from .base import BaseAPI
from ..models.webhooks import Webhook, WebhookList


class WebhooksAPI(BaseAPI):
    """API client for webhooks endpoints"""
    
    def list(self, page: int = 1, per_page: int = 100) -> WebhookList:
        """
        List webhooks
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            
        Returns:
            WebhookList containing webhooks
        """
        return self._get("/webhooks", params={"page": page, "per_page": per_page}, model_class=WebhookList)
        
    def get(self, webhook_id: str) -> Webhook:
        """
        Get a webhook by ID
        
        Args:
            webhook_id: Webhook ID
            
        Returns:
            Webhook object
        """
        return self._get(f"/webhooks/{webhook_id}", model_class=Webhook)
        
    def create(self, webhook_data: Dict[str, Any]) -> Webhook:
        """
        Create a new webhook
        
        Args:
            webhook_data: Webhook configuration
            
        Returns:
            Created Webhook object
        """
        return self._post("/webhooks", json=webhook_data, model_class=Webhook)
        
    def update(self, webhook_id: str, webhook_data: Dict[str, Any]) -> Webhook:
        """
        Update a webhook
        
        Args:
            webhook_id: Webhook ID
            webhook_data: Webhook configuration to update
            
        Returns:
            Updated Webhook object
        """
        return self._put(f"/webhooks/{webhook_id}", json=webhook_data, model_class=Webhook)
        
    def delete(self, webhook_id: str) -> Dict[str, Any]:
        """
        Delete a webhook
        
        Args:
            webhook_id: Webhook ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/webhooks/{webhook_id}")
        
    def activate(self, webhook_id: str) -> Webhook:
        """
        Activate a webhook
        
        Args:
            webhook_id: Webhook ID
            
        Returns:
            Activated Webhook
        """
        return self._post(f"/webhooks/{webhook_id}/activate", model_class=Webhook)
        
    def pause(self, webhook_id: str) -> Webhook:
        """
        Pause a webhook
        
        Args:
            webhook_id: Webhook ID
            
        Returns:
            Paused Webhook
        """
        return self._post(f"/webhooks/{webhook_id}/pause", model_class=Webhook) 