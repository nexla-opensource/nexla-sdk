"""
Sources API endpoints
"""
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

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
from ..models.source_metrics import (
    SourceMetricsResponse,
    AggregatedMetricsResponse,
    RunMetricsResponse,
    FileStatsResponse,
    FileMetricsResponse,
    RawFileMetricsResponse,
    CronFileMetricsResponse,
    ConfigValidationResponse,
    ProbeTreeResponse,
    FileSampleResponse,
    ReingestionResponse,
    FileStatus
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
              source_config: Optional[Dict[str, Any]] = None,
              data_credentials_id: Optional[int] = None,
              description: Optional[str] = None) -> Source:
        """
        Create a new data source
        
        Args:
            name: Name of the source
            source_type: Type of source (connector codename)
            source_config: Source configuration properties (optional)
            data_credentials_id: ID of the data credential to use
            description: Optional description of the source
            
        Returns:
            Created Source
        """
        source_data = {
            "name": name,
            "source_type": source_type
        }

        if source_config:
            source_data["source_config"] = source_config
        
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
        try:
            # The delete endpoint may return an empty response with a 200 status code
            # In this case, we'll create a successful response object
            self._delete(f"/data_sources/{source_id}")
            return DeleteSourceResponse(code="200", message="Source deleted successfully")
        except Exception as e:
            # If there was an actual response with error details, it would be raised
            # by the _delete method, so we just pass through the exception
            raise
        
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
    
    def reingest_file(self, source_id: int, file_path: str) -> ReingestionResponse:
        """
        Re-ingest a file for a data source
        
        Args:
            source_id: Data source ID
            file_path: Path to the file to re-ingest
            
        Returns:
            Response indicating success or failure
        """
        return self._post(
            f"/data_sources/{source_id}/file/ingest", 
            json={"file": file_path},
            model_class=ReingestionResponse
        )
        
    def validate_config(self, source_id: int, config: Optional[Dict[str, Any]] = None) -> ConfigValidationResponse:
        """
        Validate a source configuration
        
        Args:
            source_id: Data source ID
            config: Optional configuration to validate, if None uses stored configuration
            
        Returns:
            Validation results
        """
        payload = {} if config is None else config
        return self._post(
            f"/data_sources/{source_id}/config/validate", 
            json=payload,
            model_class=ConfigValidationResponse
        )
        
    def probe_tree(
        self, 
        source_id: int, 
        depth: int = 1,
        **source_params
    ) -> ProbeTreeResponse:
        """
        Inspect the content hierarchy of a source
        
        Args:
            source_id: Data source ID
            depth: Depth to traverse in the hierarchy
            **source_params: Source-specific parameters (e.g., bucket, prefix, region for S3)
            
        Returns:
            Tree structure response
        """
        payload = {"depth": depth}
        payload.update(source_params)
        
        return self._post(
            f"/data_sources/{source_id}/probe/tree",
            json=payload,
            model_class=ProbeTreeResponse
        )
        
    def probe_files(self, source_id: int, path: str) -> FileSampleResponse:
        """
        Get a sample of a file from a source
        
        Args:
            source_id: Data source ID
            path: Path to the file to sample
            
        Returns:
            File sample response
        """
        return self._post(
            f"/data_sources/{source_id}/probe/files",
            json={"path": path},
            model_class=FileSampleResponse
        )
        
    def get_metrics(self, source_id: int) -> SourceMetricsResponse:
        """
        Get lifetime metrics for a source
        
        Args:
            source_id: Data source ID
            
        Returns:
            Metrics including records and size
        """
        return self._get(
            f"/data_sources/{source_id}/metrics",
            model_class=SourceMetricsResponse
        )
        
    def get_daily_metrics(
        self, 
        source_id: int, 
        from_date: Optional[Union[str, datetime]] = None,
        to_date: Optional[Union[str, datetime]] = None,
        page: int = 1,
        size: int = 100
    ) -> AggregatedMetricsResponse:
        """
        Get daily aggregated metrics for a source
        
        Args:
            source_id: Data source ID
            from_date: Start date for the metrics (UTC datetime in '%Y-%m-%dT%H:%M:%S' format)
            to_date: End date for the metrics (UTC datetime in '%Y-%m-%dT%H:%M:%S' format)
            page: Page number for pagination
            size: Number of items per page
            
        Returns:
            Daily aggregated metrics
        """
        params = {"aggregate": 1, "page": page, "size": size}
        
        if from_date:
            if isinstance(from_date, datetime):
                from_date = from_date.strftime('%Y-%m-%dT%H:%M:%S')
            params["from"] = from_date
            
        if to_date:
            if isinstance(to_date, datetime):
                to_date = to_date.strftime('%Y-%m-%dT%H:%M:%S')
            params["to"] = to_date
        
        return self._get(
            f"/data_sources/{source_id}/metrics",
            params=params,
            model_class=AggregatedMetricsResponse
        )
        
    def get_run_metrics(
        self, 
        source_id: int,
        run_id: Optional[int] = None,
        from_date: Optional[Union[str, datetime]] = None,
        to_date: Optional[Union[str, datetime]] = None,
        page: int = 1,
        size: int = 100
    ) -> RunMetricsResponse:
        """
        Get metrics aggregated by ingestion frequency
        
        Args:
            source_id: Data source ID
            run_id: Starting from unix epoch time of ingestion events
            from_date: Start date for the metrics (UTC datetime in '%Y-%m-%dT%H:%M:%S' format)
            to_date: End date for the metrics (UTC datetime in '%Y-%m-%dT%H:%M:%S' format)
            page: Page number for pagination
            size: Number of items per page
            
        Returns:
            Metrics aggregated by run ID
        """
        params = {"page": page, "size": size}
        
        if run_id:
            params["runId"] = run_id
            
        if from_date:
            if isinstance(from_date, datetime):
                from_date = from_date.strftime('%Y-%m-%dT%H:%M:%S')
            params["from"] = from_date
            
        if to_date:
            if isinstance(to_date, datetime):
                to_date = to_date.strftime('%Y-%m-%dT%H:%M:%S')
            params["to"] = to_date
        
        return self._get(
            f"/data_sources/{source_id}/metrics/run_summary",
            params=params,
            model_class=RunMetricsResponse
        )
        
    def get_files_stats(
        self, 
        source_id: int,
        status: Optional[FileStatus] = None,
        from_date: Optional[Union[str, datetime]] = None,
        to_date: Optional[Union[str, datetime]] = None
    ) -> FileStatsResponse:
        """
        Get ingestion status statistics for files
        
        Args:
            source_id: Data source ID
            status: Filter by file status
            from_date: Start date for the metrics (UTC datetime in '%Y-%m-%dT%H:%M:%S' format)
            to_date: End date for the metrics (UTC datetime in '%Y-%m-%dT%H:%M:%S' format)
            
        Returns:
            File status statistics
        """
        params = {}
        
        if status:
            params["status"] = status.value
            
        if from_date:
            if isinstance(from_date, datetime):
                from_date = from_date.strftime('%Y-%m-%dT%H:%M:%S')
            params["from"] = from_date
            
        if to_date:
            if isinstance(to_date, datetime):
                to_date = to_date.strftime('%Y-%m-%dT%H:%M:%S')
            params["to"] = to_date
        
        return self._get(
            f"/data_sources/{source_id}/metrics/files_stats",
            params=params,
            model_class=FileStatsResponse
        )
        
    def get_files_metrics(
        self, 
        source_id: int,
        status: Optional[FileStatus] = None,
        from_date: Optional[Union[str, datetime]] = None,
        to_date: Optional[Union[str, datetime]] = None,
        page: int = 1,
        size: int = 100
    ) -> FileMetricsResponse:
        """
        Get ingestion metrics per file
        
        Args:
            source_id: Data source ID
            status: Filter by file status
            from_date: Start date for the metrics (UTC datetime in '%Y-%m-%dT%H:%M:%S' format)
            to_date: End date for the metrics (UTC datetime in '%Y-%m-%dT%H:%M:%S' format)
            page: Page number for pagination
            size: Number of items per page
            
        Returns:
            Metrics for each file
        """
        params = {"page": page, "size": size}
        
        if status:
            params["status"] = status.value
            
        if from_date:
            if isinstance(from_date, datetime):
                from_date = from_date.strftime('%Y-%m-%dT%H:%M:%S')
            params["from"] = from_date
            
        if to_date:
            if isinstance(to_date, datetime):
                to_date = to_date.strftime('%Y-%m-%dT%H:%M:%S')
            params["to"] = to_date
        
        return self._get(
            f"/data_sources/{source_id}/metrics/files",
            params=params,
            model_class=FileMetricsResponse
        )
        
    def get_files_raw_metrics(
        self, 
        source_id: int,
        status: Optional[FileStatus] = None,
        from_date: Optional[Union[str, datetime]] = None,
        to_date: Optional[Union[str, datetime]] = None,
        page: int = 1,
        size: int = 100
    ) -> RawFileMetricsResponse:
        """
        Get raw ingestion metrics for all file processing attempts
        
        Args:
            source_id: Data source ID
            status: Filter by file status
            from_date: Start date for the metrics (UTC datetime in '%Y-%m-%dT%H:%M:%S' format)
            to_date: End date for the metrics (UTC datetime in '%Y-%m-%dT%H:%M:%S' format)
            page: Page number for pagination
            size: Number of items per page
            
        Returns:
            Raw metrics for each file processing attempt
        """
        params = {"page": page, "size": size}
        
        if status:
            params["status"] = status.value
            
        if from_date:
            if isinstance(from_date, datetime):
                from_date = from_date.strftime('%Y-%m-%dT%H:%M:%S')
            params["from"] = from_date
            
        if to_date:
            if isinstance(to_date, datetime):
                to_date = to_date.strftime('%Y-%m-%dT%H:%M:%S')
            params["to"] = to_date
        
        return self._get(
            f"/data_sources/{source_id}/metrics/files_raw",
            params=params,
            model_class=RawFileMetricsResponse
        )
        
    def get_files_cron_metrics(
        self, 
        source_id: int,
        status: Optional[FileStatus] = None,
        from_date: Optional[Union[str, datetime]] = None,
        to_date: Optional[Union[str, datetime]] = None,
        page: int = 1,
        size: int = 100
    ) -> CronFileMetricsResponse:
        """
        Get ingestion metrics per scheduled poll cycle
        
        Args:
            source_id: Data source ID
            status: Filter by file status
            from_date: Start date for the metrics (UTC datetime in '%Y-%m-%dT%H:%M:%S' format)
            to_date: End date for the metrics (UTC datetime in '%Y-%m-%dT%H:%M:%S' format)
            page: Page number for pagination
            size: Number of items per page
            
        Returns:
            Metrics for each file grouped by ingestion cycle
        """
        params = {"page": page, "size": size}
        
        if status:
            params["status"] = status.value
            
        if from_date:
            if isinstance(from_date, datetime):
                from_date = from_date.strftime('%Y-%m-%dT%H:%M:%S')
            params["from"] = from_date
            
        if to_date:
            if isinstance(to_date, datetime):
                to_date = to_date.strftime('%Y-%m-%dT%H:%M:%S')
            params["to"] = to_date
        
        return self._get(
            f"/data_sources/{source_id}/metrics/files_cron",
            params=params,
            model_class=CronFileMetricsResponse
        )

    def get_quarantine_samples(
        self, 
        source_id: int, 
        page: int = 1, 
        per_page: int = 10,
        start_time: Optional[Union[int, str, datetime]] = None,
        end_time: Optional[Union[int, str, datetime]] = None
    ) -> Dict[str, Any]:
        """
        Get quarantine samples (error records) for a source
        
        Args:
            source_id: ID of the source
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
            f"/data_sources/{source_id}/probe/quarantine/sample",
            json=data,
        ) 