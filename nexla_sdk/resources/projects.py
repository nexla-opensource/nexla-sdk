from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.projects.responses import Project
from nexla_sdk.models.projects.requests import ProjectFlowList
from nexla_sdk.models.flows.responses import FlowResponse


class ProjectsResource(BaseResource):
    """Resource for managing projects."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/projects"
        self._model_class = Project
    
    def get_flows(self, project_id: int) -> FlowResponse:
        """
        Get flows in project.
        
        Args:
            project_id: Project ID
        
        Returns:
            Flow response
        """
        path = f"{self._path}/{project_id}/flows"
        response = self._make_request('GET', path)
        return FlowResponse(**response)
    
    def add_flows(self, project_id: int, flows: ProjectFlowList) -> FlowResponse:
        """
        Add flows to project.
        
        Args:
            project_id: Project ID
            flows: Flows to add
        
        Returns:
            Updated flow response
        """
        path = f"{self._path}/{project_id}/flows"
        response = self._make_request('PUT', path, json=flows.to_dict())
        return FlowResponse(**response)
    
    def replace_flows(self, project_id: int, flows: ProjectFlowList) -> FlowResponse:
        """
        Replace all flows in project.
        
        Args:
            project_id: Project ID
            flows: New flow list
        
        Returns:
            New flow response
        """
        path = f"{self._path}/{project_id}/flows"
        response = self._make_request('POST', path, json=flows.to_dict())
        return FlowResponse(**response)
    
    def remove_flows(self,
                     project_id: int,
                     flows: Optional[ProjectFlowList] = None) -> FlowResponse:
        """
        Remove flows from project.
        
        Args:
            project_id: Project ID
            flows: Flows to remove (None = remove all)
        
        Returns:
            Remaining flows
        """
        path = f"{self._path}/{project_id}/flows"
        data = flows.to_dict() if flows else None
        response = self._make_request('DELETE', path, json=data)
        return FlowResponse(**response)
