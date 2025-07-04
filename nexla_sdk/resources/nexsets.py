from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.nexsets.responses import Nexset, NexsetSample
from nexla_sdk.models.nexsets.requests import NexsetCopyOptions


class NexsetsResource(BaseResource):
    """Resource for managing nexsets (data sets)."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/data_sets"
        self._model_class = Nexset
    
    def get_samples(self,
                    set_id: int,
                    count: int = 10,
                    include_metadata: bool = False,
                    live: bool = False) -> List[NexsetSample]:
        """
        Get sample records from a nexset.
        
        Args:
            set_id: Nexset ID
            count: Maximum number of samples
            include_metadata: Include Nexla metadata
            live: Fetch live samples from topic
        
        Returns:
            List of sample records
        """
        path = f"{self._path}/{set_id}/samples"
        params = {
            'count': count,
            'include_metadata': include_metadata,
            'live': live
        }
        
        response = self._make_request('GET', path, params=params)
        
        # Handle both response formats
        if isinstance(response, list):
            return [NexsetSample(**item) for item in response]
        return response
    
    def copy(self, set_id: int, options: Optional[NexsetCopyOptions] = None) -> Nexset:
        """
        Copy a nexset.
        
        Args:
            set_id: Nexset ID
            options: Copy options
        
        Returns:
            Copied nexset
        """
        data = options.to_dict() if options else {}
        return super().copy(set_id, data)
