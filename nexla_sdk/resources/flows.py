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
        List all flows.
        
        Args:
            flows_only: Only return flow structure without resource details
            include_run_metrics: Include run metrics in response
            **kwargs: Additional parameters
        
        Returns:
            List of flows
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
        params = {'flows_only': 1} if flows_only else {}
        return super().get(flow_id, expand=False)
    
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
    
    def activate(self, flow_id: int, all: bool = False) -> FlowResponse:
        """
        Activate a flow.
        
        Args:
            flow_id: Flow ID
            all: Activate entire flow tree
        
        Returns:
            Activated flow
        """
        path = f"{self._path}/{flow_id}/activate"
        params = {'all': 1} if all else {}
        
        response = self._make_request('PUT', path, params=params)
        return self._parse_response(response)
    
    def pause(self, flow_id: int, all: bool = False) -> FlowResponse:
        """
        Pause a flow.
        
        Args:
            flow_id: Flow ID
            all: Pause entire flow tree
        
        Returns:
            Paused flow
        """
        path = f"{self._path}/{flow_id}/pause"
        params = {'all': 1} if all else {}
        
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
        data = options.to_dict() if options else {}
        response = super().copy(flow_id, data)
        return response
    
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
                             all: bool = False) -> FlowResponse:
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
        params = {'all': 1} if all else {}
        
        response = self._make_request('PUT', path, params=params)
        return self._parse_response(response)
    
    def pause_by_resource(self,
                          resource_type: str,
                          resource_id: int,
                          all: bool = False) -> FlowResponse:
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
        params = {'all': 1} if all else {}
        
        response = self._make_request('PUT', path, params=params)
        return self._parse_response(response)
