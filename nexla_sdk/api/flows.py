"""
Flows API endpoints
"""
from typing import Dict, Any, Optional, List, Union, Literal

from .base import BaseAPI
from ..models.flows import Flow, FlowList, FlowCondensed, FlowResponse, FlowNode
from ..models.access import AccessRole


class FlowsAPI(BaseAPI):
    """API client for flows endpoints"""
    
    def list(
        self, 
        page: Optional[int] = None, 
        per_page: Optional[int] = None, 
        flows_only: Optional[int] = None,
        access_role: Optional[AccessRole] = None
    ) -> Union[FlowResponse, FlowList]:
        """
        List flows
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            flows_only: Set to 1 to return only flow chains without resource details
            access_role: Filter flows by access role (e.g., AccessRole.ADMIN)
            
        Returns:
            FlowResponse or FlowList object containing flows
        """
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if flows_only is not None:
            params["flows_only"] = flows_only
        if access_role is not None:
            params["access_role"] = access_role.value
            
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        
        # Try to parse as new FlowResponse, fall back to legacy FlowList
        try:
            return self._get("/flows", params=params, headers=headers, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._get("/flows", params=params, model_class=FlowList)
        
    def get(self, flow_id: str, flows_only: Optional[int] = None) -> Union[FlowResponse, Flow]:
        """
        Get a flow by ID
        
        Args:
            flow_id: Flow ID
            flows_only: Set to 1 to return only flow chains without resource details
            
        Returns:
            FlowResponse or Flow object
        """
        params = {}
        if flows_only is not None:
            params["flows_only"] = flows_only
            
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._get(f"/flows/{flow_id}", params=params, headers=headers, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._get(f"/flows/{flow_id}", model_class=Flow)
        
    def create(self, flow_data: Dict[str, Any]) -> Flow:
        """
        Create a new flow
        
        Args:
            flow_data: Flow configuration
            
        Returns:
            Created Flow object
        """
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        try:
            # Try to parse as new FlowResponse which contains data in a "flows" array
            response_data = self._post("/flows", json=flow_data, headers=headers, model_class=FlowResponse)
            if hasattr(response_data, "flows") and len(response_data.flows) > 0:
                # Extract the first flow from the flows array
                return response_data.flows[0]
            else:
                # Fall back to direct conversion if the new format isn't found
                return self._post("/flows", json=flow_data, headers=headers, model_class=Flow)
        except:
            # Last resort fallback to legacy model for backward compatibility
            return self._post("/flows", json=flow_data, model_class=Flow)
        
    def update(self, flow_id: str, flow_data: Optional[Dict[str, Any]] = None, **kwargs) -> Flow:
        """
        Update a flow
        
        Args:
            flow_id: Flow ID
            flow_data: Flow configuration to update as a dictionary
            **kwargs: Flow configuration to update as keyword arguments (alternative to flow_data)
            
        Returns:
            Updated Flow object
        """
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        
        # Handle both dictionary and keyword arguments
        data = flow_data or {}
        if kwargs:
            data.update(kwargs)
            
        return self._put(f"/flows/{flow_id}", json=data, headers=headers, model_class=Flow)
        
    def delete(self, flow_id: str) -> Dict[str, Any]:
        """
        Delete a flow
        
        Args:
            flow_id: Flow ID
            
        Returns:
            Response containing status code and message
        """
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        return self._delete(f"/flows/{flow_id}", headers=headers)
        
    def activate(self, flow_id: str, all: Optional[int] = None) -> Union[FlowResponse, Flow]:
        """
        Activate a flow
        
        Args:
            flow_id: Flow ID
            all: Set to 1 to activate full flow chain if flow_id is not an origin node
            
        Returns:
            Updated FlowResponse or Flow object
        """
        params = {}
        if all is not None:
            params["all"] = all
            
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._put(f"/flows/{flow_id}/activate", params=params, headers=headers, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._post(f"/flows/{flow_id}/activate", model_class=Flow)
        
    def pause(self, flow_id: str, all: Optional[int] = None) -> Union[FlowResponse, Flow]:
        """
        Pause a flow
        
        Args:
            flow_id: Flow ID
            all: Set to 1 to pause full flow chain if flow_id is not an origin node
            
        Returns:
            Updated FlowResponse or Flow object
        """
        params = {}
        if all is not None:
            params["all"] = all
            
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._put(f"/flows/{flow_id}/pause", params=params, headers=headers, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._post(f"/flows/{flow_id}/pause", model_class=Flow)
        
    def add_tags(self, flow_id: str, tags: List[str]) -> Union[FlowResponse, Flow]:
        """
        Add tags to a flow
        
        Args:
            flow_id: Flow ID
            tags: List of tags to add
            
        Returns:
            Updated FlowResponse or Flow object
        """
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        data = {"tags": tags}
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._post(f"/flows/{flow_id}/tags", json=data, headers=headers, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._post(f"/flows/{flow_id}/tags", json=data, model_class=Flow)
    
    def remove_tags(self, flow_id: str, tags: List[str]) -> Union[FlowResponse, Flow]:
        """
        Remove tags from a flow
        
        Args:
            flow_id: Flow ID
            tags: List of tags to remove
            
        Returns:
            Updated FlowResponse or Flow object
        """
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        data = {"tags": tags}
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._delete(f"/flows/{flow_id}/tags", json=data, headers=headers, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._delete(f"/flows/{flow_id}/tags", json=data, model_class=Flow)
    
    def run(self, flow_id: str, run_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run a flow
        
        Args:
            flow_id: Flow ID
            run_params: Optional parameters for the run
            
        Returns:
            Response containing run information
        """
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        data = run_params or {}
        
        return self._post(f"/flows/{flow_id}/run", json=data, headers=headers)
    
    def get_run_status(self, flow_id: str, run_id: str) -> Dict[str, Any]:
        """
        Get the status of a flow run
        
        Args:
            flow_id: Flow ID
            run_id: Flow run ID
            
        Returns:
            Response containing run status information
        """
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        return self._get(f"/flows/{flow_id}/runs/{run_id}", headers=headers)
        
    def copy(
        self, 
        flow_id: str, 
        reuse_data_credentials: Optional[bool] = None,
        copy_access_controls: Optional[bool] = None,
        copy_dependent_data_flows: Optional[bool] = None,
        owner_id: Optional[str] = None,
        org_id: Optional[str] = None,
        new_name: Optional[str] = None
    ) -> Union[FlowResponse, Flow]:
        """
        Create a copy of a flow
        
        Args:
            flow_id: Flow ID
            reuse_data_credentials: Whether to reuse credentials instead of cloning them
            copy_access_controls: Whether to copy access controls to the new flow
            copy_dependent_data_flows: Whether to clone flows that originate from sources that are children of destinations
            owner_id: ID of the user who should own the new flow
            org_id: ID of the organization where the new flow should be created
            new_name: Optional new name for the copied flow
            
        Returns:
            Created FlowResponse or Flow object
        """
        params = {}
        if new_name:
            params["name"] = new_name
            
        data = {}
        if reuse_data_credentials is not None:
            data["reuse_data_credentials"] = reuse_data_credentials
        if copy_access_controls is not None:
            data["copy_access_controls"] = copy_access_controls
        if copy_dependent_data_flows is not None:
            data["copy_dependent_data_flows"] = copy_dependent_data_flows
        if owner_id is not None:
            data["owner_id"] = owner_id
        if org_id is not None:
            data["org_id"] = org_id
            
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._post(f"/flows/{flow_id}/copy", params=params, json=data, headers=headers, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._post(f"/flows/{flow_id}/copy", params=params, model_class=Flow)
        
    def list_condensed(self) -> Dict[str, Any]:
        """
        List all flows in condensed format
        
        Returns:
            Dictionary containing condensed flows
        """
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        return self._get("/flows/all/condensed", headers=headers)
        
    def get_by_resource(
        self, 
        resource_type: Literal["data_sources", "data_sinks", "data_sets"], 
        resource_id: str,
        flows_only: Optional[int] = None
    ) -> Union[FlowResponse, Flow]:
        """
        Get a flow by resource ID
        
        This is a variant of flow endpoints where the flow node can be referenced
        not by its own ID, but by the ID of the unique resource that is linked to
        that flow node.
        
        Args:
            resource_type: Resource type ("data_sources", "data_sinks", "data_sets")
            resource_id: Resource ID
            flows_only: Set to 1 to return only flow chains without resource details
            
        Returns:
            FlowResponse or Flow object
        """
        params = {}
        if flows_only is not None:
            params["flows_only"] = flows_only
            
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._get(f"/{resource_type}/{resource_id}/flow", params=params, headers=headers, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._get(f"/{resource_type}/{resource_id}/flow", model_class=Flow)
    
    def delete_by_resource(
        self, 
        resource_type: Literal["data_sources", "data_sinks", "data_sets"], 
        resource_id: str
    ) -> Dict[str, Any]:
        """
        Delete a flow by resource ID
        
        This is a variant of flow endpoints where the flow node can be referenced
        not by its own ID, but by the ID of the unique resource that is linked to
        that flow node.
        
        Args:
            resource_type: Resource type ("data_sources", "data_sinks", "data_sets")
            resource_id: Resource ID
            
        Returns:
            Response containing status code and message
        """
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        return self._delete(f"/{resource_type}/{resource_id}/flow", headers=headers)
        
    def activate_by_resource(
        self, 
        resource_type: Literal["data_sources", "data_sinks", "data_sets"], 
        resource_id: str,
        all: Optional[int] = None
    ) -> Union[FlowResponse, Flow]:
        """
        Activate a flow by resource ID
        
        This is a variant of flow endpoints where the flow node can be referenced
        not by its own ID, but by the ID of the unique resource that is linked to
        that flow node.
        
        Args:
            resource_type: Resource type ("data_sources", "data_sinks", "data_sets")
            resource_id: Resource ID
            all: Set to 1 to activate full flow chain if the resource is not an origin node
            
        Returns:
            FlowResponse or Flow object
        """
        params = {}
        if all is not None:
            params["all"] = all
            
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._put(f"/{resource_type}/{resource_id}/activate", params=params, headers=headers, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._post(f"/{resource_type}/{resource_id}/activate", model_class=Flow)
        
    def pause_by_resource(
        self, 
        resource_type: Literal["data_sources", "data_sinks", "data_sets"], 
        resource_id: str,
        all: Optional[int] = None
    ) -> Union[FlowResponse, Flow]:
        """
        Pause a flow by resource ID
        
        This is a variant of flow endpoints where the flow node can be referenced
        not by its own ID, but by the ID of the unique resource that is linked to
        that flow node.
        
        Args:
            resource_type: Resource type ("data_sources", "data_sinks", "data_sets")
            resource_id: Resource ID
            all: Set to 1 to pause full flow chain if the resource is not an origin node
            
        Returns:
            FlowResponse or Flow object
        """
        params = {}
        if all is not None:
            params["all"] = all
            
        headers = {"Accept": "application/vnd.nexla.api.v1+json"}
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._put(f"/{resource_type}/{resource_id}/pause", params=params, headers=headers, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._post(f"/{resource_type}/{resource_id}/pause", model_class=Flow) 