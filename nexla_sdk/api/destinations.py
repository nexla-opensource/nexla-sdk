"""
Destinations API endpoints (Data Sinks)
"""
from typing import Dict, Any, Optional, List, Union

from .base import BaseAPI
from ..models.destinations import Destination, DestinationList, DestinationExpanded


class DestinationsAPI(BaseAPI):
    """API client for data sinks (destinations) endpoints"""
    
    def list(self, limit: int = 100, offset: int = 0) -> DestinationList:
        """
        List data sinks
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            DestinationList containing data sinks
        """
        return self._get("/data_sinks", params={"limit": limit, "offset": offset}, model_class=DestinationList)
        
    def get(self, sink_id: str, expand: bool = False) -> Union[Destination, DestinationExpanded]:
        """
        Get a data sink by ID
        
        Args:
            sink_id: Data sink ID
            expand: Whether to expand the resource details
            
        Returns:
            Destination or DestinationExpanded (if expand=True)
        """
        path = f"/data_sinks/{sink_id}"
        model_class = DestinationExpanded if expand else Destination
        
        if expand:
            path += "?expand=1"
            
        return self._get(path, model_class=model_class)
        
    def create(self, sink_data: Dict[str, Any]) -> Destination:
        """
        Create a new data sink
        
        Args:
            sink_data: Data sink configuration
            
        Returns:
            Created Destination
        """
        return self._post("/data_sinks", json=sink_data, model_class=Destination)
        
    def update(self, sink_id: str, sink_data: Dict[str, Any]) -> Destination:
        """
        Update a data sink
        
        Args:
            sink_id: Data sink ID
            sink_data: Data sink configuration to update
            
        Returns:
            Updated Destination
        """
        return self._put(f"/data_sinks/{sink_id}", json=sink_data, model_class=Destination)
        
    def delete(self, sink_id: str) -> Dict[str, Any]:
        """
        Delete a data sink
        
        Args:
            sink_id: Data sink ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/data_sinks/{sink_id}")
        
    def activate(self, sink_id: str) -> Destination:
        """
        Activate a data sink
        
        Args:
            sink_id: Data sink ID
            
        Returns:
            Activated Destination
        """
        return self._post(f"/data_sinks/{sink_id}/activate", model_class=Destination)
        
    def pause(self, sink_id: str) -> Destination:
        """
        Pause a data sink
        
        Args:
            sink_id: Data sink ID
            
        Returns:
            Paused Destination
        """
        return self._post(f"/data_sinks/{sink_id}/pause", model_class=Destination) 