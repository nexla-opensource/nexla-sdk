from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.destinations.responses import Destination
from nexla_sdk.models.destinations.requests import DestinationCreate, DestinationUpdate, DestinationCopyOptions


class DestinationsResource(BaseResource):
    """Resource for managing destinations (data sinks)."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/data_sinks"
        self._model_class = Destination
    
    def list(self, **kwargs) -> List[Destination]:
        """
        List all destinations.
        
        Args:
            **kwargs: Additional parameters (page, per_page, access_role, etc.)
        
        Returns:
            List of destinations
        """
        return super().list(**kwargs)
    
    def get(self, sink_id: int, expand: bool = False) -> Destination:
        """
        Get single destination by ID.
        
        Args:
            sink_id: Destination ID
            expand: Include expanded references
        
        Returns:
            Destination instance
        """
        return super().get(sink_id, expand)
    
    def create(self, data: DestinationCreate) -> Destination:
        """
        Create new destination.
        
        Args:
            data: Destination creation data
        
        Returns:
            Created destination
        """
        return super().create(data)
    
    def update(self, sink_id: int, data: DestinationUpdate) -> Destination:
        """
        Update destination.
        
        Args:
            sink_id: Destination ID
            data: Updated destination data
        
        Returns:
            Updated destination
        """
        return super().update(sink_id, data)
    
    def delete(self, sink_id: int) -> Dict[str, Any]:
        """
        Delete destination.
        
        Args:
            sink_id: Destination ID
        
        Returns:
            Response with status
        """
        return super().delete(sink_id)
    
    def activate(self, sink_id: int) -> Destination:
        """
        Activate destination.
        
        Args:
            sink_id: Destination ID
        
        Returns:
            Activated destination
        """
        return super().activate(sink_id)
    
    def pause(self, sink_id: int) -> Destination:
        """
        Pause destination.
        
        Args:
            sink_id: Destination ID
        
        Returns:
            Paused destination
        """
        return super().pause(sink_id)
    
    def copy(self, sink_id: int, options: Optional[DestinationCopyOptions] = None) -> Destination:
        """
        Copy a destination.
        
        Args:
            sink_id: Destination ID
            options: Copy options
        
        Returns:
            Copied destination
        """
        data = options.to_dict() if options else {}
        return super().copy(sink_id, data)