from typing import List, Optional, Dict, Any
from nexla_sdk.resources.base_resource import BaseResource
from nexla_sdk.models.projects.responses import Project
from nexla_sdk.models.projects.requests import ProjectCreate, ProjectUpdate, ProjectFlowList
from nexla_sdk.models.flows.responses import FlowResponse


class ProjectsResource(BaseResource):
    """Resource for managing projects."""
    
    def __init__(self, client):
        super().__init__(client)
        self._path = "/projects"
        self._model_class = Project
    
    def list(self, expand: bool = False, **kwargs) -> List[Project]:
        """
        List all projects.
        
        Args:
            expand: Include flows in the response
            **kwargs: Additional parameters (page, per_page, access_role, etc.)
        
        Returns:
            List of projects
        """
        if expand:
            kwargs['expand'] = 'true'
        return super().list(**kwargs)
    
    def get(self, project_id: int, expand: bool = False) -> Project:
        """
        Get single project by ID.
        
        Args:
            project_id: Project ID
            expand: Include expanded references
        
        Returns:
            Project instance
        """
        return super().get(project_id, expand)
    
    def create(self, data: ProjectCreate) -> Project:
        """
        Create new project.
        
        Args:
            data: Project creation data
        
        Returns:
            Created project
        """
        return super().create(data)
    
    def update(self, project_id: int, data: ProjectUpdate) -> Project:
        """
        Update project.
        
        Args:
            project_id: Project ID
            data: Updated project data
        
        Returns:
            Updated project
        """
        return super().update(project_id, data)
    
    def delete(self, project_id: int) -> Dict[str, Any]:
        """
        Delete project.
        
        Args:
            project_id: Project ID
        
        Returns:
            Response with status
        """
        return super().delete(project_id)

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
