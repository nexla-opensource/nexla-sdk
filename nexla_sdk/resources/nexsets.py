from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.nexsets.responses import Nexset, NexsetSample
from nexla_sdk.models.nexsets.requests import NexsetCreate, NexsetUpdate, NexsetCopyOptions


class NexsetsResource(BaseResource):
    """Resource for managing nexsets (data sets)."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/data_sets"
        self._model_class = Nexset
    
    def list(self, **kwargs) -> List[Nexset]:
        """
        List nexsets with optional filters.
        
        Args:
            page: Page number (via kwargs)
            per_page: Items per page (via kwargs)
            access_role: Filter by access role (via kwargs)
            **kwargs: Additional query parameters
        
        Returns:
            List of nexsets

        Examples:
            client.nexsets.list(page=1, per_page=50)
        """
        return super().list(**kwargs)
    
    def get(self, set_id: int, expand: bool = False) -> Nexset:
        """
        Get single nexset by ID.
        
        Args:
            set_id: Nexset ID
            expand: Include expanded references
        
        Returns:
            Nexset instance
        
        Examples:
            client.nexsets.get(789)
        """
        return super().get(set_id, expand)
    
    def create(self, data: NexsetCreate) -> Nexset:
        """
        Create new nexset.
        
        Args:
            data: Nexset creation data
        
        Returns:
            Created nexset
        
        Examples:
            new_set = client.nexsets.create(NexsetCreate(name="My Dataset", ...))
        """
        return super().create(data)
    
    def update(self, set_id: int, data: NexsetUpdate) -> Nexset:
        """
        Update nexset.
        
        Args:
            set_id: Nexset ID
            data: Updated nexset data
        
        Returns:
            Updated nexset
        """
        return super().update(set_id, data)
    
    def delete(self, set_id: int) -> Dict[str, Any]:
        """
        Delete nexset.
        
        Args:
            set_id: Nexset ID
        
        Returns:
            Response with status
        """
        return super().delete(set_id)
    
    def activate(self, set_id: int) -> Nexset:
        """
        Activate nexset.
        
        Args:
            set_id: Nexset ID
        
        Returns:
            Activated nexset
        """
        return super().activate(set_id)
    
    def pause(self, set_id: int) -> Nexset:
        """
        Pause nexset.
        
        Args:
            set_id: Nexset ID
        
        Returns:
            Paused nexset
        """
        return super().pause(set_id)

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

    def docs_recommendation(self, set_id: int) -> Dict[str, Any]:
        """Generate AI suggestion for Nexset documentation."""
        path = f"{self._path}/{set_id}/docs/recommendation"
        return self._make_request('POST', path)
