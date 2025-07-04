from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.destinations.responses import Destination
from nexla_sdk.models.destinations.requests import DestinationCopyOptions


class DestinationsResource(BaseResource):
    """Resource for managing destinations (data sinks)."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/data_sinks"
        self._model_class = Destination
    
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