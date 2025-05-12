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
        
        # Try to parse as new FlowResponse, fall back to legacy FlowList
        try:
            return self._get("/data_flows", params=params, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._get("/data_flows", params=params, model_class=FlowList)
        
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
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._get(f"/data_flows/{flow_id}", params=params, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._get(f"/data_flows/{flow_id}", model_class=Flow)
        
    def create(self, flow_data: Dict[str, Any]) -> Flow:
        """
        Create a new flow
        
        Args:
            flow_data: Flow configuration
            
        Returns:
            Created Flow object
        """
        try:
            # Try to use the /flows endpoint instead of /data_flows for creation
            # since some API endpoints might still use the older path format
            response_data = self._post("/flows", json=flow_data, model_class=Flow)
            return response_data
        except:
            # Fall back to the newer endpoint
            try:
                # Try to parse as new FlowResponse which contains data in a "flows" array
                response_data = self._post("/data_flows", json=flow_data, model_class=FlowResponse)
                if hasattr(response_data, "flows") and len(response_data.flows) > 0:
                    # Extract the first flow from the flows array
                    return response_data.flows[0]
                else:
                    # Fall back to direct conversion if the new format isn't found
                    return self._post("/data_flows", json=flow_data, model_class=Flow)
            except:
                # Last resort fallback to legacy model for backward compatibility
                return self._post("/data_flows", json=flow_data, model_class=Flow)
        
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
        # Handle both dictionary and keyword arguments
        data = flow_data or {}
        if kwargs:
            data.update(kwargs)
        
        # Try with the /flows endpoint first, fall back to /data_flows if needed
        try:
            return self._put(f"/flows/{flow_id}", json=data, model_class=Flow)
        except:
            return self._put(f"/data_flows/{flow_id}", json=data, model_class=Flow)
        
    def delete(self, flow_id: str, all: Optional[int] = None) -> Dict[str, Any]:
        """
        Delete a flow
        
        Args:
            flow_id: Flow ID
            all: Set to 1 to delete the entire flow, including upstream resources
            
        Returns:
            Response containing status code and message
        """
        params = {}
        if all is not None:
            params["all"] = all
        
        # Try with the /flows endpoint first, fall back to /data_flows if needed
        try:
            return self._delete(f"/flows/{flow_id}", params=params)
        except:
            return self._delete(f"/data_flows/{flow_id}", params=params)
        
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
        
        # Try to parse as new FlowResponse, fall back to legacy Flow and endpoint
        try:
            return self._put(f"/data_flows/{flow_id}/activate", params=params, model_class=FlowResponse)
        except:
            try:
                # Try the old endpoint with PUT
                return self._put(f"/flows/{flow_id}/activate", params=params, model_class=Flow)
            except:
                # Fall back to legacy method with POST
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
        
        # Try to parse as new FlowResponse, fall back to legacy Flow and endpoint
        try:
            return self._put(f"/data_flows/{flow_id}/pause", params=params, model_class=FlowResponse)
        except:
            try:
                # Try the old endpoint with PUT
                return self._put(f"/flows/{flow_id}/pause", params=params, model_class=Flow)
            except:
                # Fall back to legacy method with POST
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
        data = {"tags": tags}
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._post(f"/flows/{flow_id}/tags", json=data, model_class=FlowResponse)
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
        data = {"tags": tags}
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._delete(f"/flows/{flow_id}/tags", json=data, model_class=FlowResponse)
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
        data = run_params or {}
        
        return self._post(f"/flows/{flow_id}/run", json=data)
    
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
        Copy a flow
        
        Args:
            flow_id: Flow ID to copy
            reuse_data_credentials: Whether to reuse data credentials
            copy_access_controls: Whether to copy access controls
            copy_dependent_data_flows: Whether to copy dependent data flows
            owner_id: Owner ID for the new flow
            org_id: Organization ID for the new flow
            new_name: New name for the copied flow
            
        Returns:
            Copied flow
        """
        params = {}
        
        if reuse_data_credentials is not None:
            params["reuse_data_credentials"] = int(reuse_data_credentials)
            
        if copy_access_controls is not None:
            params["copy_access_controls"] = int(copy_access_controls)
            
        if copy_dependent_data_flows is not None:
            params["copy_dependent_data_flows"] = int(copy_dependent_data_flows)
            
        if owner_id is not None:
            params["owner_id"] = owner_id
            
        if org_id is not None:
            params["org_id"] = org_id
            
        if new_name is not None:
            params["new_name"] = new_name
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._post(f"/flows/{flow_id}/copy", params=params, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._post(f"/flows/{flow_id}/copy", params=params, model_class=Flow)
            
    def list_condensed(self) -> Dict[str, Any]:
        """
        List condensed flows
        
        Returns:
            Response containing condensed flow information
        """
        return self._get("/flows/condensed")
        
    def get_by_resource(
        self, 
        resource_type: Literal["data_sources", "data_sinks", "data_sets"], 
        resource_id: str,
        flows_only: Optional[int] = None
    ) -> Union[FlowResponse, Flow]:
        """
        Get flows by resource
        
        Args:
            resource_type: Resource type (data_sources, data_sinks, or data_sets)
            resource_id: Resource ID
            flows_only: Set to 1 to return only flow chains without resource details
            
        Returns:
            Flow response or Flow object
        """
        params = {}
        if flows_only is not None:
            params["flows_only"] = flows_only
            
        # Use the appropriate path based on resource type
        if resource_type == "data_sources":
            path = f"/data_flows/data_source/{resource_id}"
        elif resource_type == "data_sinks":
            path = f"/data_flows/data_sink/{resource_id}"
        elif resource_type == "data_sets":
            path = f"/data_flows/{resource_id}"
        else:
            raise ValueError(f"Unsupported resource type: {resource_type}")
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._get(path, params=params, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._get(path, model_class=Flow)
            
    def delete_by_resource(
        self, 
        resource_type: Literal["data_sources", "data_sinks", "data_sets"], 
        resource_id: str,
        all: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Delete flows by resource
        
        Args:
            resource_type: Resource type (data_sources, data_sinks, or data_sets)
            resource_id: Resource ID
            all: Set to 1 to delete the entire flow, including upstream resources
            
        Returns:
            Response containing status code and message
        """
        params = {}
        if all is not None:
            params["all"] = all
            
        # Use the appropriate path based on resource type
        if resource_type == "data_sources":
            path = f"/data_flows/data_source/{resource_id}"
        elif resource_type == "data_sinks":
            path = f"/data_flows/data_sink/{resource_id}"
        elif resource_type == "data_sets":
            path = f"/data_flows/{resource_id}"
        else:
            raise ValueError(f"Unsupported resource type: {resource_type}")
        
        return self._delete(path, params=params)
            
    def activate_by_resource(
        self, 
        resource_type: Literal["data_sources", "data_sinks", "data_sets"], 
        resource_id: str,
        all: Optional[int] = None
    ) -> Union[FlowResponse, Flow]:
        """
        Activate flows by resource
        
        Args:
            resource_type: Resource type (data_sources, data_sinks, or data_sets)
            resource_id: Resource ID
            all: Set to 1 to activate full flow chain
            
        Returns:
            Flow response or Flow object
        """
        params = {}
        if all is not None:
            params["all"] = all
            
        # Use the appropriate path based on resource type
        if resource_type == "data_sources":
            path = f"/data_flows/data_source/{resource_id}/activate"
        elif resource_type == "data_sinks":
            path = f"/data_flows/data_sink/{resource_id}/activate"
        elif resource_type == "data_sets":
            path = f"/data_flows/{resource_id}/activate"
        else:
            raise ValueError(f"Unsupported resource type: {resource_type}")
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._put(path, params=params, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._post(path, model_class=Flow)
            
    def pause_by_resource(
        self, 
        resource_type: Literal["data_sources", "data_sinks", "data_sets"], 
        resource_id: str,
        all: Optional[int] = None
    ) -> Union[FlowResponse, Flow]:
        """
        Pause flows by resource
        
        Args:
            resource_type: Resource type (data_sources, data_sinks, or data_sets)
            resource_id: Resource ID
            all: Set to 1 to pause full flow chain
            
        Returns:
            Flow response or Flow object
        """
        params = {}
        if all is not None:
            params["all"] = all
            
        # Use the appropriate path based on resource type
        if resource_type == "data_sources":
            path = f"/data_flows/data_source/{resource_id}/pause"
        elif resource_type == "data_sinks":
            path = f"/data_flows/data_sink/{resource_id}/pause"
        elif resource_type == "data_sets":
            path = f"/data_flows/{resource_id}/pause"
        else:
            raise ValueError(f"Unsupported resource type: {resource_type}")
        
        # Try to parse as new FlowResponse, fall back to legacy Flow
        try:
            return self._put(path, params=params, model_class=FlowResponse)
        except:
            # Fall back to legacy model for backward compatibility
            return self._post(path, model_class=Flow) 