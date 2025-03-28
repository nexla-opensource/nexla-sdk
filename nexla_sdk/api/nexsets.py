"""
Nexsets API endpoints (Data Sets)
"""
from typing import Dict, Any, Optional, List, Union

from .base import BaseAPI
from ..models.nexsets import Nexset, NexsetList, NexsetSchema, NexsetSample, NexsetCharacteristics


class NexsetsAPI(BaseAPI):
    """API client for data sets (nexsets) endpoints"""
    
    def list(self, limit: int = 100, offset: int = 0) -> NexsetList:
        """
        List data sets
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            NexsetList containing data sets
        """
        return self._get("/data_sets", params={"limit": limit, "offset": offset}, model_class=NexsetList)
        
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
        
    def get_sample_data(self, dataset_id: str, limit: int = 10) -> NexsetSample:
        """
        Get sample data for a data set
        
        Args:
            dataset_id: Data set ID
            limit: Number of sample records to return
            
        Returns:
            NexsetSample containing sample records
        """
        return self._get(f"/data_sets/{dataset_id}/sample", 
                       params={"limit": limit}, 
                       model_class=NexsetSample)
                       
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
        
    def copy(self, dataset_id: str, new_name: Optional[str] = None) -> Nexset:
        """
        Create a copy of a data set
        
        Args:
            dataset_id: Data set ID
            new_name: Optional new name for the copied data set
            
        Returns:
            New Nexset
        """
        params = {}
        if new_name:
            params["name"] = new_name
            
        return self._post(f"/data_sets/{dataset_id}/copy", params=params, model_class=Nexset) 