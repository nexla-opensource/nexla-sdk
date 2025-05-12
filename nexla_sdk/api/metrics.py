"""
Metrics API endpoints
"""
from typing import Union, Optional, Dict, Any
from datetime import datetime

from .base import BaseAPI
from ..models.metrics import (
    AccountMetricsResponse, DailyMetricsResponse, RunMetricsResponse,
    FlowMetricsResponse, ResourceType, FlowLogsResponse
)


class MetricsAPI(BaseAPI):
    """API client for metrics endpoints"""

    def get_organization_account_metrics(
        self,
        org_id: int,
        from_date: Union[str, datetime],
        to_date: Optional[Union[str, datetime]] = None
    ) -> AccountMetricsResponse:
        """
        Get Total Account Metrics for An Organization
        
        Retrieves total account utilization metrics for an organization. The result consists
        of aggregated information about records processed within the specified date range
        by all resources owned by users in the organization.
        
        Args:
            org_id: The unique ID of the organization
            from_date: Start date for metrics aggregation period
            to_date: End date for metrics aggregation period (defaults to current date)
            
        Returns:
            Account metrics response
        """
        params = {"from": from_date}
        if to_date:
            params["to"] = to_date
            
        return self._get(
            f"/orgs/{org_id}/flows/account_metrics",
            params=params,
            model_class=AccountMetricsResponse
        )
        
    def get_resource_metrics_daily(
        self,
        resource_type: Union[ResourceType, str],
        resource_id: int,
        from_date: Union[str, datetime],
        to_date: Optional[Union[str, datetime]] = None
    ) -> DailyMetricsResponse:
        """
        Get Daily Metrics for a Resource of a Flow
        
        Retrieves daily data processing metrics of a data_source, data_set, or data_sink.
        
        Args:
            resource_type: Type of resource (data_sources, data_sinks, or data_sets)
            resource_id: ID of the resource to fetch metrics for
            from_date: Start date for metrics reporting period
            to_date: End date for metrics reporting period (defaults to current date)
            
        Returns:
            Daily metrics response
        """
        if isinstance(resource_type, ResourceType):
            resource_type = resource_type.value
            
        params = {
            "from": from_date,
            "aggregate": 1
        }
        
        if to_date:
            params["to"] = to_date
            
        return self._get(
            f"/{resource_type}/{resource_id}/metrics",
            params=params,
            model_class=DailyMetricsResponse
        )
        
    def get_resource_metrics_by_run(
        self,
        resource_type: Union[ResourceType, str],
        resource_id: int,
        groupby: Optional[str] = "runId",
        orderby: Optional[str] = "runId",
        page: Optional[int] = None,
        size: Optional[int] = None
    ) -> RunMetricsResponse:
        """
        Get Metrics By Run ID for a Resource of a Flow
        
        Retrieves data processing metrics of a data_source, data_set, or data_sink. 
        The reported metrics are grouped by run id to indicate the number of records 
        processed during each ingestion cycle of this flow.
        
        Args:
            resource_type: Type of resource (data_sources, data_sinks, or data_sets)
            resource_id: ID of the resource to fetch metrics for
            groupby: Rule for metrics grouping (runId or lastWritten)
            orderby: Order for sorting paginated results (runId or lastWritten)
            page: Page number for pagination
            size: Items per page for pagination
            
        Returns:
            Run metrics response
        """
        if isinstance(resource_type, ResourceType):
            resource_type = resource_type.value
            
        params: Dict[str, Any] = {}
        
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
            
        url = f"/{resource_type}/{resource_id}/metrics/run_summary"
        if groupby:
            url += f"?groupby={groupby}"
        if orderby:
            url += f"&orderby={orderby}" if "?" in url else f"?orderby={orderby}"
            
        return self._get(
            url,
            params=params,
            model_class=RunMetricsResponse
        )
        
    def get_flow_metrics(
        self,
        resource_type: Union[ResourceType, str],
        resource_id: int,
        from_date: Union[str, datetime],
        to_date: Optional[Union[str, datetime]] = None,
        groupby: Optional[str] = None,
        orderby: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None
    ) -> FlowMetricsResponse:
        """
        Get Metrics for a Flow
        
        Retrieves data processing metrics of a flow. Metrics are aggregated for each node 
        of the flow for the specified time range. They can be further grouped by run id to 
        indicate the number of records processed during each ingestion cycle of this flow.
        
        Args:
            resource_type: Type of resource (data_sources, data_sinks, or data_sets)
            resource_id: ID of the resource whose flow to fetch metrics for
            from_date: Start date for metrics aggregation period
            to_date: End date for metrics aggregation period (defaults to current date)
            groupby: Rule for metrics grouping (runId)
            orderby: Order for sorting paginated results (runId or created_at)
            page: Page number for pagination
            per_page: Items per page for pagination
            
        Returns:
            Flow metrics response
        """
        if isinstance(resource_type, ResourceType):
            resource_type = resource_type.value
            
        params: Dict[str, Any] = {"from": from_date}
        
        if to_date:
            params["to"] = to_date
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
            
        url = f"/data_flows/{resource_type}/{resource_id}/metrics"
        if groupby:
            url += f"?groupby={groupby}"
        if orderby:
            url += f"&orderby={orderby}" if "?" in url else f"?orderby={orderby}"
            
        return self._get(
            url,
            params=params,
            model_class=FlowMetricsResponse
        )

    def get_flow_logs(
        self,
        resource_type: Union[ResourceType, str],
        resource_id: int,
        run_id: int,
        from_timestamp: Union[int, str, datetime],
        to_timestamp: Optional[Union[int, str, datetime]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None
    ) -> FlowLogsResponse:
        """
        Get Flow Execution Logs for Run ID of a Flow
        
        Retrieves flow execution logs for a specific run id of a flow.
        
        Args:
            resource_type: Type of resource (data_sources, data_sinks, or data_sets)
            resource_id: ID of the resource whose flow to fetch logs for
            run_id: The run id (denoting the ingestion cycle) for which logs have to be fetched
            from_timestamp: The timestamp that should be considered as the start of the logs reporting period
            to_timestamp: The timestamp that should be considered as the end of the logs reporting period
            page: Page number for pagination
            per_page: Items per page for pagination
            
        Returns:
            Flow logs response
        """
        if isinstance(resource_type, ResourceType):
            resource_type = resource_type.value
            
        params: Dict[str, Any] = {
            "run_id": run_id,
            "from": from_timestamp
        }
        
        if to_timestamp:
            params["to"] = to_timestamp
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
            
        return self._get(
            f"/data_flows/{resource_type}/{resource_id}/logs",
            params=params,
            model_class=FlowLogsResponse
        ) 