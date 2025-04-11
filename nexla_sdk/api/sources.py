"""
Sources API endpoints
"""
from typing import Dict, Any, Optional, List, Union

from .base import BaseAPI
from ..models.access import AccessRole
from ..models.sources import (
    Source, 
    SourceList, 
    SourceExpanded, 
    SourceWithExpandedDataSets,
    CreateSourceRequest,
    CopySourceRequest,
    DeleteSourceResponse
)


class SourcesAPI(BaseAPI):
    """API client for data sources endpoints"""
    
    def list(self, page: int = 1, per_page: int = 100, access_role: Optional[AccessRole] = None) -> SourceList:
        """
        List data sources
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            access_role: Filter by access role (e.g., AccessRole.ADMIN)
            
        Returns:
            SourceList containing data sources
        """
        params = {"page": page, "per_page": per_page}
        if access_role:
            params["access_role"] = access_role.value
            
        # Get raw response as a list of sources
        response = self._get("/data_sources", params=params)
        
        # Convert the list of sources to Source objects
        sources = [Source.model_validate(source) for source in response]
        
        # Create and return a SourceList object
        return SourceList(items=sources)
        
    def get(self, source_id: int, expand: bool = False) -> Union[Source, SourceExpanded, SourceWithExpandedDataSets]:
        """
        Get a data source by ID
        
        Args:
            source_id: Data source ID
            expand: Whether to expand the resource details
            
        Returns:
            Source object or SourceExpanded if expand=True
        """
        path = f"/data_sources/{source_id}"
        
        params = {}
        if expand:
            params["expand"] = 1
            model_class = SourceWithExpandedDataSets
        else:
            model_class = Source
            
        return self._get(path, params=params, model_class=model_class)
        
    def create(self, 
              name: str, 
              source_type: str, 
              source_config: Dict[str, Any],
              data_credentials_id: Optional[int] = None,
              description: Optional[str] = None) -> Source:
        """
        Create a new data source
        
        Args:
            name: Name of the source
            source_type: Type of source (connector codename)
            source_config: Source configuration properties
            data_credentials_id: ID of the data credential to use
            description: Optional description of the source
            
        Returns:
            Created Source
        """
        source_data = {
            "name": name,
            "source_type": source_type,
            "source_config": source_config
        }
        
        if data_credentials_id:
            source_data["data_credentials_id"] = data_credentials_id
            
        if description:
            source_data["description"] = description
            
        return self._post("/data_sources", json=source_data, model_class=Source)
        
    def update(self, 
              source_id: int, 
              name: Optional[str] = None,
              description: Optional[str] = None,
              source_type: Optional[str] = None,
              source_config: Optional[Dict[str, Any]] = None,
              data_credentials_id: Optional[int] = None) -> Source:
        """
        Update a data source
        
        Args:
            source_id: Data source ID
            name: New name for the source
            description: New description for the source
            source_type: New source type
            source_config: New source configuration
            data_credentials_id: New data credentials ID
            
        Returns:
            Updated Source
        """
        source_data = {}
        
        if name:
            source_data["name"] = name
            
        if description is not None:
            source_data["description"] = description
            
        if source_type:
            source_data["source_type"] = source_type
            
        if source_config:
            source_data["source_config"] = source_config
            
        if data_credentials_id:
            source_data["data_credentials_id"] = data_credentials_id
            
        return self._put(f"/data_sources/{source_id}", json=source_data, model_class=Source)
        
    def delete(self, source_id: int) -> DeleteSourceResponse:
        """
        Delete a data source
        
        Args:
            source_id: Data source ID
            
        Returns:
            Delete response with status code and message
        """
        return self._delete(f"/data_sources/{source_id}", model_class=DeleteSourceResponse)
        
    def activate(self, source_id: int) -> Source:
        """
        Activate a data source
        
        Args:
            source_id: Data source ID
            
        Returns:
            Activated Source
        """
        return self._put(f"/data_sources/{source_id}/activate", model_class=Source)
        
    def pause(self, source_id: int) -> Source:
        """
        Pause a data source
        
        Args:
            source_id: Data source ID
            
        Returns:
            Paused Source
        """
        return self._put(f"/data_sources/{source_id}/pause", model_class=Source)
        
    def copy(self, 
            source_id: int, 
            reuse_data_credentials: Optional[bool] = None,
            copy_access_controls: Optional[bool] = None,
            owner_id: Optional[int] = None,
            org_id: Optional[int] = None) -> Source:
        """
        Create a copy of a data source
        
        Args:
            source_id: Data source ID
            reuse_data_credentials: Whether to reuse the credentials of the source
            copy_access_controls: Whether to copy access controls to the new source
            owner_id: Owner ID for the new source
            org_id: Organization ID for the new source
            
        Returns:
            New Source
        """
        request_data = {}
        
        if reuse_data_credentials is not None:
            request_data["reuse_data_credentials"] = reuse_data_credentials
            
        if copy_access_controls is not None:
            request_data["copy_access_controls"] = copy_access_controls
            
        if owner_id:
            request_data["owner_id"] = owner_id
            
        if org_id:
            request_data["org_id"] = org_id
            
        return self._post(f"/data_sources/{source_id}/copy", json=request_data, model_class=Source) 