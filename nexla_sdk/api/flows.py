"""
Flows API endpoints
"""
from typing import Dict, Any, Optional, List, Union

from .base import BaseAPI
from ..models.flows import Flow, FlowList, FlowCondensed


class FlowsAPI(BaseAPI):
    """API client for flows endpoints"""
    
    def list(self, limit: int = 100, offset: int = 0) -> FlowList:
        """
        List flows
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            FlowList object containing flows
        """
        return self._get("/flows", params={"limit": limit, "offset": offset}, model_class=FlowList)
        
    def get(self, flow_id: str) -> Flow:
        """
        Get a flow by ID
        
        Args:
            flow_id: Flow ID
            
        Returns:
            Flow object
        """
        return self._get(f"/flows/{flow_id}", model_class=Flow)
        
    def create(self, flow_data: Dict[str, Any]) -> Flow:
        """
        Create a new flow
        
        Args:
            flow_data: Flow configuration
            
        Returns:
            Created Flow object
        """
        return self._post("/flows", json=flow_data, model_class=Flow)
        
    def update(self, flow_id: str, flow_data: Dict[str, Any]) -> Flow:
        """
        Update a flow
        
        Args:
            flow_id: Flow ID
            flow_data: Flow configuration to update
            
        Returns:
            Updated Flow object
        """
        return self._put(f"/flows/{flow_id}", json=flow_data, model_class=Flow)
        
    def delete(self, flow_id: str) -> Dict[str, Any]:
        """
        Delete a flow
        
        Args:
            flow_id: Flow ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/flows/{flow_id}")
        
    def activate(self, flow_id: str) -> Flow:
        """
        Activate a flow
        
        Args:
            flow_id: Flow ID
            
        Returns:
            Updated Flow object
        """
        return self._post(f"/flows/{flow_id}/activate", model_class=Flow)
        
    def pause(self, flow_id: str) -> Flow:
        """
        Pause a flow
        
        Args:
            flow_id: Flow ID
            
        Returns:
            Updated Flow object
        """
        return self._post(f"/flows/{flow_id}/pause", model_class=Flow)
        
    def copy(self, flow_id: str, new_name: Optional[str] = None) -> Flow:
        """
        Create a copy of a flow
        
        Args:
            flow_id: Flow ID
            new_name: Optional new name for the copied flow
            
        Returns:
            Created Flow object
        """
        params = {}
        if new_name:
            params["name"] = new_name
            
        return self._post(f"/flows/{flow_id}/copy", params=params, model_class=Flow)
        
    def list_condensed(self) -> Dict[str, Any]:
        """
        List all flows in condensed format
        
        Returns:
            Dictionary containing condensed flows
        """
        return self._get("/flows/all/condensed")
        
    def get_by_resource(self, resource_type: str, resource_id: str) -> Flow:
        """
        Get a flow by resource ID
        
        Args:
            resource_type: Resource type (e.g., "data_sources", "data_sinks")
            resource_id: Resource ID
            
        Returns:
            Flow object
        """
        return self._get(f"/{resource_type}/{resource_id}/flow", model_class=Flow)
        
    def activate_by_resource(self, resource_type: str, resource_id: str) -> Flow:
        """
        Activate a flow by resource ID
        
        Args:
            resource_type: Resource type (e.g., "data_sources", "data_sinks")
            resource_id: Resource ID
            
        Returns:
            Flow object
        """
        return self._post(f"/{resource_type}/{resource_id}/activate", model_class=Flow)
        
    def pause_by_resource(self, resource_type: str, resource_id: str) -> Flow:
        """
        Pause a flow by resource ID
        
        Args:
            resource_type: Resource type (e.g., "data_sources", "data_sinks")
            resource_id: Resource ID
            
        Returns:
            Flow object
        """
        return self._post(f"/{resource_type}/{resource_id}/pause", model_class=Flow) 