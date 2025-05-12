"""
Nexsets API endpoints (Data Sets)
"""
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from .base import BaseAPI
from ..models.nexsets import Nexset, NexsetList, NexsetSchema, NexsetSample, NexsetCharacteristics, NexsetSampleWithMetadata
from ..models.access import AccessRole
from pydantic import ValidationError


class NexsetsAPI(BaseAPI):
    """API client for data sets (nexsets) endpoints"""
    
    def list(self, page: int = 1, per_page: int = 100, access_role: Optional[AccessRole] = None) -> NexsetList:
        """
        List data sets
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            access_role: Filter by access role
            
        Returns:
            NexsetList containing data sets
        """
        params = {"page": page, "per_page": per_page}
        if access_role:
            params["access_role"] = access_role.value
            
        # Get raw response as a list of nexsets
        response = self._get("/data_sets", params=params)
        
        # If response is empty, return an empty NexsetList
        if not response:
            return NexsetList(items=[], total=0, page=page, page_size=per_page)
            
        # Convert the list of nexsets to Nexset objects
        nexsets = []
        for nexset_data in response:
            try:
                nexset = Nexset.model_validate(nexset_data)
                nexsets.append(nexset)
            except ValidationError as e:
                # Log the error (in a real implementation) and continue
                print(f"Warning: Failed to validate nexset: {e}")
                continue
                
        return NexsetList(
            items=nexsets,
            total=len(nexsets),  # Use actual count as total
            page=page,
            page_size=per_page
        )
        
    def get(self, dataset_id: str, expand: bool = False) -> Nexset:
        """
        Get a data set by ID
        
        Args:
            dataset_id: Data set ID
            expand: Whether to expand the resource details
            
        Returns:
            Nexset object
        """
        path = f"/data_sets/{dataset_id}"
        if expand:
            path += "?expand=1"
            
        return self._get(path, model_class=Nexset)
        
    def create(self, dataset_data: Dict[str, Any]) -> Nexset:
        """
        Create a new data set
        
        Args:
            dataset_data: Data set configuration
            
        Returns:
            Created Nexset
        """
        return self._post("/data_sets", json=dataset_data, model_class=Nexset)
        
    def update(self, dataset_id: str, dataset_data: Dict[str, Any]) -> Nexset:
        """
        Update a data set
        
        Args:
            dataset_id: Data set ID
            dataset_data: Data set configuration to update
            
        Returns:
            Updated Nexset
        """
        return self._put(f"/data_sets/{dataset_id}", json=dataset_data, model_class=Nexset)
        
    def delete(self, dataset_id: str) -> Dict[str, Any]:
        """
        Delete a data set
        
        Args:
            dataset_id: Data set ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/data_sets/{dataset_id}")
        
    def get_schema(self, dataset_id: str) -> NexsetSchema:
        """
        Get the schema for a data set
        
        Args:
            dataset_id: Data set ID
            
        Returns:
            NexsetSchema object
        """
        return self._get(f"/data_sets/{dataset_id}/schema", model_class=NexsetSchema)
        
    def update_schema(self, dataset_id: str, schema_data: Dict[str, Any]) -> NexsetSchema:
        """
        Update the schema for a data set
        
        Args:
            dataset_id: Data set ID
            schema_data: Schema configuration to update
            
        Returns:
            Updated NexsetSchema
        """
        return self._put(f"/data_sets/{dataset_id}/schema", json=schema_data, model_class=NexsetSchema)
        
    def get_sample_data(
        self, 
        dataset_id: str, 
        limit: int = 10, 
        include_metadata: bool = False,
        live: bool = False
    ) -> Union[NexsetSample, List[NexsetSampleWithMetadata]]:
        """
        Get sample data for a data set
        
        Args:
            dataset_id: Data set ID
            limit: Number of sample records to return
            include_metadata: Whether to include Nexla metadata with each sample
            live: Whether to fetch live samples from the Nexset topic
            
        Returns:
            Sample data, either as NexsetSample or a list of NexsetSampleWithMetadata
        """
        params = {"limit": limit}
        if include_metadata:
            params["include_metadata"] = include_metadata
        if live:
            params["live"] = live
            
        return self._get(
            f"/data_sets/{dataset_id}/samples", 
            params=params, 
            model_class=List[NexsetSampleWithMetadata] if include_metadata else NexsetSample
        )
                       
    def get_characteristics(self, dataset_id: str) -> NexsetCharacteristics:
        """
        Get characteristics for a data set
        
        Args:
            dataset_id: Data set ID
            
        Returns:
            NexsetCharacteristics
        """
        return self._get(f"/data_sets/{dataset_id}/characteristics", 
                       model_class=NexsetCharacteristics)
                       
    def activate(self, dataset_id: str) -> Nexset:
        """
        Activate a data set
        
        Args:
            dataset_id: Data set ID
            
        Returns:
            Activated Nexset
        """
        return self._post(f"/data_sets/{dataset_id}/activate", model_class=Nexset)
        
    def pause(self, dataset_id: str) -> Nexset:
        """
        Pause a data set
        
        Args:
            dataset_id: Data set ID
            
        Returns:
            Paused Nexset
        """
        return self._post(f"/data_sets/{dataset_id}/pause", model_class=Nexset)
        
    def copy(
        self, 
        dataset_id: str, 
        new_name: Optional[str] = None,
        copy_access_controls: bool = False,
        owner_id: Optional[int] = None,
        org_id: Optional[int] = None
    ) -> Nexset:
        """
        Create a copy of a data set
        
        Args:
            dataset_id: Data set ID
            new_name: Optional new name for the copied data set
            copy_access_controls: Whether to copy access controls to the new data set
            owner_id: Optional owner ID for the new data set
            org_id: Optional organization ID for the new data set
            
        Returns:
            New Nexset
        """
        params = {}
        payload = {}
        
        if new_name:
            params["name"] = new_name
            
        if copy_access_controls:
            payload["copy_access_controls"] = copy_access_controls
            
        if owner_id:
            payload["owner_id"] = owner_id
            
        if org_id:
            payload["org_id"] = org_id
            
        return self._post(
            f"/data_sets/{dataset_id}/copy",
            params=params,
            json=payload if payload else None,
            model_class=Nexset
        )

    def get_quarantine_samples(
        self, 
        set_id: int, 
        page: int = 1, 
        per_page: int = 10,
        start_time: Optional[Union[int, str, datetime]] = None,
        end_time: Optional[Union[int, str, datetime]] = None
    ) -> Dict[str, Any]:
        """
        Get quarantine samples (error records) for a Nexset
        
        Args:
            set_id: ID of the Nexset
            page: Page number for pagination
            per_page: Items per page for pagination
            start_time: Start time for the sample query (timestamp in milliseconds or datetime)
            end_time: End time for the sample query (timestamp in milliseconds or datetime)
            
        Returns:
            Dictionary containing quarantine samples
        """
        data = {
            "page": page,
            "per_page": per_page
        }
        
        if start_time is not None:
            if isinstance(start_time, datetime):
                start_time = int(start_time.timestamp() * 1000)
            data["start_time"] = start_time
            
        if end_time is not None:
            if isinstance(end_time, datetime):
                end_time = int(end_time.timestamp() * 1000)
            data["end_time"] = end_time
            
        return self._post(
            f"/data_sets/{set_id}/probe/quarantine/sample",
            json=data,

        ) 