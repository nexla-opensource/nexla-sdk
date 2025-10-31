from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.flows.responses import FlowResponse
from nexla_sdk.models.flows.requests import FlowCopyOptions


class FlowsResource(BaseResource):
    """Resource for managing data flows."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/flows"
        self._model_class = FlowResponse
    
    def list(self,
             flows_only: bool = False,
             include_run_metrics: bool = False,
             **kwargs) -> List[FlowResponse]:
        """
        List flows with optional filters.
        
        Args:
            flows_only: Only return flow structure without resource details
            include_run_metrics: Include run metrics in response
            page: Page number (via kwargs)
            per_page: Items per page (via kwargs)
            **kwargs: Additional query parameters
        
        Returns:
            List of flows
        
        Examples:
            client.flows.list(flows_only=True)
            client.flows.list(include_run_metrics=True, page=1, per_page=50)
        """
        params = kwargs.copy()
        if flows_only:
            params['flows_only'] = 1
        if include_run_metrics:
            params['include_run_metrics'] = 1
        
        response = self._make_request('GET', self._path, params=params)
        # API returns a single FlowResponse object for list
        return [self._parse_response(response)]
    
    def get(self, flow_id: int, flows_only: bool = False) -> FlowResponse:
        """
        Get flow by ID.
        
        Args:
            flow_id: Flow ID
            flows_only: Only return flow structure without resource details
        
        Returns:
            Flow response
        """
        path = f"{self._path}/{flow_id}"
        params = {'flows_only': 1} if flows_only else {}
        response = self._make_request('GET', path, params=params)
        return self._parse_response(response)
    
    def get_by_resource(self, 
                        resource_type: str,
                        resource_id: int,
                        flows_only: bool = False) -> FlowResponse:
        """
        Get flow by resource ID.
        
        Args:
            resource_type: Type of resource (data_sources, data_sets, data_sinks)
            resource_id: Resource ID
            flows_only: Only return flow structure
        
        Returns:
            Flow response
        """
        path = f"/{resource_type}/{resource_id}/flow"
        params = {'flows_only': 1} if flows_only else {}
        
        response = self._make_request('GET', path, params=params)
        return self._parse_response(response)
    
    def activate(self, flow_id: int, all: bool = False, full_tree: bool = False) -> FlowResponse:
        """
        Activate a flow.
        
        Args:
            flow_id: Flow ID
            all: Activate entire flow tree
        
        Returns:
            Activated flow
        """
        path = f"{self._path}/{flow_id}/activate"
        params = {}
        if all:
            params['all'] = 1
        if full_tree:
            params['full_tree'] = 1
        
        response = self._make_request('PUT', path, params=params)
        return self._parse_response(response)
    
    def pause(self, flow_id: int, all: bool = False, full_tree: bool = False) -> FlowResponse:
        """
        Pause a flow.
        
        Args:
            flow_id: Flow ID
            all: Pause entire flow tree
        
        Returns:
            Paused flow
        """
        path = f"{self._path}/{flow_id}/pause"
        params = {}
        if all:
            params['all'] = 1
        if full_tree:
            params['full_tree'] = 1
        
        response = self._make_request('PUT', path, params=params)
        return self._parse_response(response)
    
    def copy(self, flow_id: int, options: Optional[FlowCopyOptions] = None) -> FlowResponse:
        """
        Copy a flow.
        
        Args:
            flow_id: Flow ID
            options: Copy options
        
        Returns:
            Copied flow
        """
        return super().copy(flow_id, options)
    
    def delete(self, flow_id: int) -> Dict[str, Any]:
        """
        Delete flow.
        
        Args:
            flow_id: Flow ID
        
        Returns:
            Response with status
        """
        return super().delete(flow_id)
    
    def delete_by_resource(self, resource_type: str, resource_id: int) -> Dict[str, Any]:
        """
        Delete flow by resource ID.
        
        Args:
            resource_type: Type of resource
            resource_id: Resource ID
        
        Returns:
            Response status
        """
        path = f"/{resource_type}/{resource_id}/flow"
        return self._make_request('DELETE', path)
    
    def activate_by_resource(self,
                             resource_type: str,
                             resource_id: int,
                             all: bool = False,
                             full_tree: bool = False) -> FlowResponse:
        """
        Activate flow by resource ID.
        
        Args:
            resource_type: Type of resource
            resource_id: Resource ID
            all: Activate entire flow tree
        
        Returns:
            Activated flow
        """
        path = f"/{resource_type}/{resource_id}/activate"
        params = {}
        if all:
            params['all'] = 1
        if full_tree:
            params['full_tree'] = 1
        
        response = self._make_request('PUT', path, params=params)
        return self._parse_response(response)
    
    def pause_by_resource(self,
                          resource_type: str,
                          resource_id: int,
                          all: bool = False,
                          full_tree: bool = False) -> FlowResponse:
        """
        Pause flow by resource ID.
        
        Args:
            resource_type: Type of resource
            resource_id: Resource ID
            all: Pause entire flow tree
        
        Returns:
            Paused flow
        """
        path = f"/{resource_type}/{resource_id}/pause"
        params = {}
        if all:
            params['all'] = 1
        if full_tree:
            params['full_tree'] = 1
        
        response = self._make_request('PUT', path, params=params)
        return self._parse_response(response)

    def docs_recommendation(self, flow_id: int) -> Dict[str, Any]:
        """Generate AI suggestion for flow documentation."""
        path = f"{self._path}/{flow_id}/docs/recommendation"
        return self._make_request('POST', path)

    def get_logs(self,
                 resource_type: str,
                 resource_id: int,
                 run_id: int,
                 from_ts: int,
                 to_ts: int = None,
                 page: int = None,
                 per_page: int = None) -> Dict[str, Any]:
        """Get flow execution logs for a specific run id of a flow."""
        path = f"/data_flows/{resource_type}/{resource_id}/logs"
        params = {
            'run_id': run_id,
            'from': from_ts,
        }
        if to_ts is not None:
            params['to'] = to_ts
        if page is not None:
            params['page'] = page
        if per_page is not None:
            params['per_page'] = per_page
        return self._make_request('GET', path, params=params)

    def get_metrics(self,
                    resource_type: str,
                    resource_id: int,
                    from_date: str,
                    to_date: str = None,
                    groupby: str = None,
                    orderby: str = None,
                    page: int = None,
                    per_page: int = None) -> Dict[str, Any]:
        """Get flow metrics for a flow node keyed by resource id."""
        path = f"/data_flows/{resource_type}/{resource_id}/metrics"
        params = {'from': from_date}
        if to_date:
            params['to'] = to_date
        if groupby:
            params['groupby'] = groupby
        if orderby:
            params['orderby'] = orderby
        if page is not None:
            params['page'] = page
        if per_page is not None:
            params['per_page'] = per_page
        
        return self._make_request('GET', path, params=params)
