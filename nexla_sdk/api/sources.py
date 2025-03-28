"""
Sources API endpoints
"""
from typing import Dict, Any, Optional, List, Union

from .base import BaseAPI
from ..models.sources import Source, SourceList, SourceExpanded


class SourcesAPI(BaseAPI):
    """API client for data sources endpoints"""
    
    def list(self, limit: int = 100, offset: int = 0) -> SourceList:
        """
        List data sources
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            SourceList containing data sources
        """
        return self._get("/data_sources", params={"limit": limit, "offset": offset}, model_class=SourceList)
        
    def get(self, source_id: str, expand: bool = False) -> Union[Source, SourceExpanded]:
        """
        Get a data source by ID
        
        Args:
            source_id: Data source ID
            expand: Whether to expand the resource details
            
        Returns:
            Source or SourceExpanded (if expand=True)
        """
        path = f"/data_sources/{source_id}"
        model_class = SourceExpanded if expand else Source
        
        if expand:
            path += "?expand=1"
            
        return self._get(path, model_class=model_class)
        
    def create(self, source_data: Dict[str, Any]) -> Source:
        """
        Create a new data source
        
        Args:
            source_data: Data source configuration
            
        Returns:
            Created Source
        """
        return self._post("/data_sources", json=source_data, model_class=Source)
        
    def update(self, source_id: str, source_data: Dict[str, Any]) -> Source:
        """
        Update a data source
        
        Args:
            source_id: Data source ID
            source_data: Data source configuration to update
            
        Returns:
            Updated Source
        """
        return self._put(f"/data_sources/{source_id}", json=source_data, model_class=Source)
        
    def delete(self, source_id: str) -> Dict[str, Any]:
        """
        Delete a data source
        
        Args:
            source_id: Data source ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/data_sources/{source_id}")
        
    def activate(self, source_id: str) -> Source:
        """
        Activate a data source
        
        Args:
            source_id: Data source ID
            
        Returns:
            Activated Source
        """
        return self._post(f"/data_sources/{source_id}/activate", model_class=Source)
        
    def pause(self, source_id: str) -> Source:
        """
        Pause a data source
        
        Args:
            source_id: Data source ID
            
        Returns:
            Paused Source
        """
        return self._post(f"/data_sources/{source_id}/pause", model_class=Source)
        
    def copy(self, source_id: str, new_name: Optional[str] = None) -> Source:
        """
        Create a copy of a data source
        
        Args:
            source_id: Data source ID
            new_name: Optional new name for the copied data source
            
        Returns:
            New Source
        """
        params = {}
        if new_name:
            params["name"] = new_name
            
        return self._post(f"/data_sources/{source_id}/copy", params=params, model_class=Source) 