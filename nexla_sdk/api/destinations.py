"""
Destinations API endpoints (Data Sinks)
"""
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from .base import BaseAPI
from ..models.access import AccessRole
from ..models.destinations import (
    DataSink, DataSinkList, CreateDataSinkRequest, UpdateDataSinkRequest,
    CopyDataSinkRequest, DeleteDataSinkResponse, Destination, DestinationList,
    SinkType, SinkStatus, LifetimeMetricsResponse, DailyMetricsResponse,
    RunSummaryMetricsResponse, FileStatsResponse, FileMetricsResponse,
    RawFileMetricsResponse, ConfigValidationResponse, FileStatus
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
    
    def validate_config(self, sink_id: str, config: Optional[Dict[str, Any]] = None) -> ConfigValidationResponse:
        """
        Validate destination configuration
        
        Args:
            sink_id: Data sink ID
            config: Optional configuration to validate (uses stored config if None)
            
        Returns:
            Configuration validation response
        """
        json_data = config if config else {}
        return self._post(f"/data_sinks/{sink_id}/config/validate", json=json_data, model_class=ConfigValidationResponse)
    
    def get_metrics(self, sink_id: str) -> LifetimeMetricsResponse:
        """
        Get lifetime write metrics for a destination
        
        Args:
            sink_id: Data sink ID
            
        Returns:
            Lifetime metrics response
        """
        return self._get(f"/data_sinks/{sink_id}/metrics", model_class=LifetimeMetricsResponse)
    
    def get_daily_metrics(
        self,
        sink_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: int = 1,
        size: int = 100
    ) -> DailyMetricsResponse:
        """
        Get daily write metrics for a destination
        
        Args:
            sink_id: Data sink ID
            from_date: Start date in ISO format (YYYY-MM-DDTHH:MM:SS)
            to_date: End date in ISO format (YYYY-MM-DDTHH:MM:SS)
            page: Page number for pagination
            size: Number of entries per page
            
        Returns:
            Daily metrics response
        """
        params = {"aggregate": 1, "page": page, "size": size}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
            
        return self._get(f"/data_sinks/{sink_id}/metrics", params=params, model_class=DailyMetricsResponse)
    
    def get_run_summary_metrics(
        self,
        sink_id: str,
        run_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: int = 1,
        size: int = 100
    ) -> RunSummaryMetricsResponse:
        """
        Get metrics aggregated by ingestion frequency
        
        Args:
            sink_id: Data sink ID
            run_id: Optional run ID to filter by
            from_date: Start date in ISO format (YYYY-MM-DDTHH:MM:SS)
            to_date: End date in ISO format (YYYY-MM-DDTHH:MM:SS)
            page: Page number for pagination
            size: Number of entries per page
            
        Returns:
            Run summary metrics response
        """
        params = {"page": page, "size": size}
        if run_id:
            params["runId"] = run_id
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
            
        return self._get(f"/data_sinks/{sink_id}/metrics/run_summary", params=params, model_class=RunSummaryMetricsResponse)
    
    def get_files_stats_metrics(
        self,
        sink_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        status: Optional[FileStatus] = None
    ) -> FileStatsResponse:
        """
        Get file status metrics for a destination
        
        Args:
            sink_id: Data sink ID
            from_date: Start date in ISO format (YYYY-MM-DDTHH:MM:SS)
            to_date: End date in ISO format (YYYY-MM-DDTHH:MM:SS)
            status: Optional status filter
            
        Returns:
            File stats response
        """
        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if status:
            params["status"] = status.value
            
        return self._get(f"/data_sinks/{sink_id}/metrics/files_stats", params=params, model_class=FileStatsResponse)
    
    def get_files_metrics(
        self,
        sink_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        status: Optional[FileStatus] = None,
        page: int = 1,
        size: int = 100
    ) -> FileMetricsResponse:
        """
        Get write history per file
        
        Args:
            sink_id: Data sink ID
            from_date: Start date in ISO format (YYYY-MM-DDTHH:MM:SS)
            to_date: End date in ISO format (YYYY-MM-DDTHH:MM:SS)
            status: Optional status filter
            page: Page number for pagination
            size: Number of entries per page
            
        Returns:
            File metrics response
        """
        params = {"page": page, "size": size}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if status:
            params["status"] = status.value
            
        return self._get(f"/data_sinks/{sink_id}/metrics/files", params=params, model_class=FileMetricsResponse)
    
    def get_files_raw_metrics(
        self,
        sink_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        status: Optional[FileStatus] = None,
        page: int = 1,
        size: int = 100
    ) -> RawFileMetricsResponse:
        """
        Get raw file write status metrics
        
        Args:
            sink_id: Data sink ID
            from_date: Start date in ISO format (YYYY-MM-DDTHH:MM:SS)
            to_date: End date in ISO format (YYYY-MM-DDTHH:MM:SS)
            status: Optional status filter
            page: Page number for pagination
            size: Number of entries per page
            
        Returns:
            Raw file metrics response
        """
        params = {"page": page, "size": size}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if status:
            params["status"] = status.value
            
        return self._get(f"/data_sinks/{sink_id}/metrics/files_raw", params=params, model_class=RawFileMetricsResponse)
    
    def get_quarantine_samples(
        self, 
        sink_id: int, 
        page: int = 1, 
        per_page: int = 10,
        start_time: Optional[Union[int, str, datetime]] = None,
        end_time: Optional[Union[int, str, datetime]] = None
    ) -> Dict[str, Any]:
        """
        Get quarantine samples (error records) for a destination
        
        Args:
            sink_id: ID of the destination
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
            f"/data_sinks/{sink_id}/probe/quarantine/sample",
            json=data,

        ) 