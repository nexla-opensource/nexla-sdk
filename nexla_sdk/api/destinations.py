"""
Destinations API endpoints (Data Sinks)
"""
from typing import Dict, Any, Optional, List, Union

from .base import BaseAPI
from ..models.access import AccessRole
from ..models.destinations import (
    DataSink, DataSinkList, CreateDataSinkRequest, UpdateDataSinkRequest,
    CopyDataSinkRequest, DeleteDataSinkResponse, Destination, DestinationList,
    SinkType, SinkStatus
)
from ..models.credentials import Credential


class DestinationsAPI(BaseAPI):
    """API client for data sinks (destinations) endpoints"""
    
    def list(self, access_role: Optional[AccessRole] = None, page: int = 1, per_page: int = 100) -> DataSinkList:
        """
        List data sinks
        
        Args:
            access_role: Filter by access role (e.g., AccessRole.ADMIN)
            page: Page number for pagination
            per_page: Number of items per page
            
        Returns:
            DataSinkList containing data sinks
        """
        params = {"page": page, "per_page": per_page}
        if access_role:
            params["access_role"] = access_role.value
            
        # Get raw response as a list of data sinks
        response = self._get("/data_sinks", params=params)
        
        # If response is empty, return an empty DataSinkList
        if not response:
            return DataSinkList(items=[], total=0, page=page, page_size=per_page)
            
        # Convert the list of data sinks to DataSink objects
        data_sinks = [DataSink.model_validate(sink) for sink in response]
        
        # Create and return a DataSinkList with the expected fields
        return DataSinkList(
            items=data_sinks,
            total=len(data_sinks),  # Using length as total since API doesn't provide it
            page=page,
            page_size=per_page
        )
        
    def get(self, sink_id: str, expand: bool = False) -> DataSink:
        """
        Get a data sink by ID
        
        Args:
            sink_id: Data sink ID
            expand: Whether to expand the resource details with related resources
            
        Returns:
            DataSink object
        """
        path = f"/data_sinks/{sink_id}"
        
        if expand:
            path += "?expand=1"
            
        return self._get(path, model_class=DataSink)
        
    def create(self, request: Union[CreateDataSinkRequest, Dict[str, Any]]) -> DataSink:
        """
        Create a new data sink
        
        Args:
            request: Data sink creation request or dictionary with configuration
            
        Returns:
            Created DataSink
        """
        if isinstance(request, CreateDataSinkRequest):
            request = request.dict(exclude_none=True)
            
        return self._post("/data_sinks", json=request, model_class=DataSink)
        
    def update(self, sink_id: str, request: Union[UpdateDataSinkRequest, Dict[str, Any]]) -> DataSink:
        """
        Update a data sink
        
        Args:
            sink_id: Data sink ID
            request: Data sink update request or dictionary with configuration
            
        Returns:
            Updated DataSink
        """
        if isinstance(request, UpdateDataSinkRequest):
            request = request.dict(exclude_none=True)
            
        return self._put(f"/data_sinks/{sink_id}", json=request, model_class=DataSink)
        
    def delete(self, sink_id: str) -> DeleteDataSinkResponse:
        """
        Delete a data sink
        
        Args:
            sink_id: Data sink ID
            
        Returns:
            Response with status code and message
        """
        return self._delete(f"/data_sinks/{sink_id}", model_class=DeleteDataSinkResponse)
        
    def activate(self, sink_id: str) -> DataSink:
        """
        Activate a data sink
        
        Args:
            sink_id: Data sink ID
            
        Returns:
            Activated DataSink
        """
        return self._put(f"/data_sinks/{sink_id}/activate", model_class=DataSink)
        
    def pause(self, sink_id: str) -> DataSink:
        """
        Pause a data sink
        
        Args:
            sink_id: Data sink ID
            
        Returns:
            Paused DataSink
        """
        return self._put(f"/data_sinks/{sink_id}/pause", model_class=DataSink)
        
    def copy(self, sink_id: str, request: Optional[Union[CopyDataSinkRequest, Dict[str, Any]]] = None) -> DataSink:
        """
        Copy a data sink
        
        Args:
            sink_id: Data sink ID to copy
            request: Optional copy configuration
            
        Returns:
            New copied DataSink
        """
        if isinstance(request, CopyDataSinkRequest):
            request = request.dict(exclude_none=True)
            
        json_data = request if request else {}
        return self._post(f"/data_sinks/{sink_id}/copy", json=json_data, model_class=DataSink) 