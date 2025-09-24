from typing import Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.metrics.responses import (
    MetricsResponse,
    MetricsByRunResponse
)
from nexla_sdk.models.metrics.enums import ResourceType


class MetricsResource(BaseResource):
    """
    Resource for retrieving metrics.
    
    Note: This resource already uses strongly-typed Pydantic models
    for all return types and doesn't follow standard CRUD patterns,
    so no additional typed overrides are needed.
    """
    
    def __init__(self, client):
        super().__init__(client)
        self._path = ""  # Metrics endpoints are distributed
    
    def get_resource_daily_metrics(self,
                                   resource_type: ResourceType,
                                   resource_id: int,
                                   from_date: str,
                                   to_date: Optional[str] = None) -> MetricsResponse:
        """
        Get daily metrics for a resource.
        
        Args:
            resource_type: Type of resource (data_sources, data_sets, data_sinks)
            resource_id: Resource ID
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (optional)
        
        Returns:
            Daily metrics
        """
        path = f"/{resource_type}/{resource_id}/metrics"
        params = {
            'from': from_date,
            'aggregate': 1
        }
        if to_date:
            params['to'] = to_date
        
        response = self._make_request('GET', path, params=params)
        return MetricsResponse(**response)
    
    def get_resource_metrics_by_run(self,
                                    resource_type: ResourceType,
                                    resource_id: int,
                                    groupby: Optional[str] = None,
                                    orderby: Optional[str] = None,
                                    page: Optional[int] = None,
                                    size: Optional[int] = None) -> MetricsByRunResponse:
        """
        Get metrics by run for a resource.
        
        Args:
            resource_type: Type of resource
            resource_id: Resource ID
            groupby: Group by field (runId, lastWritten)
            orderby: Order by field (runId, lastWritten)
            page: Page number
            size: Page size
        
        Returns:
            Metrics by run
        """
        path = f"/{resource_type}/{resource_id}/metrics/run_summary"
        params = {}
        if groupby:
            params['groupby'] = groupby
        if orderby:
            params['orderby'] = orderby
        if page:
            params['page'] = page
        if size:
            params['size'] = size
        
        response = self._make_request('GET', path, params=params)
        return MetricsByRunResponse(**response)
    
    def get_rate_limits(self) -> Dict[str, Any]:
        """
        Get current rate limit and usage.
        
        Returns:
            Rate limit information
        """
        path = "/limits"
        return self._make_request('GET', path)
