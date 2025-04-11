"""
Projects API endpoints
"""
from typing import Dict, Any, List, Optional, Union

from .base import BaseAPI
from ..models.projects import (
    Project, ProjectList, ProjectFlowResponse, ProjectFlowRequest,
    ProjectDataFlowRequest, CreateProjectRequest, DataFlow
)
from ..models.access import AccessRole


class ProjectsAPI(BaseAPI):
    """API client for projects endpoints"""
    
    def list(self, page: int = 1, per_page: int = 100, access_role: Optional[AccessRole] = None) -> ProjectList:
        """
        List projects
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            access_role: Filter by access role
            
        Returns:
            ProjectList containing projects
        """
        params = {"page": page, "per_page": per_page}
        if access_role:
            params["access_role"] = access_role.value
            
        return self._get("/projects", params=params, model_class=ProjectList)
        
    def get(self, project_id: str) -> Project:
        """
        Get a project by ID
        
        Args:
            project_id: Project ID
            
        Returns:
            Project object
        """
        return self._get(f"/projects/{project_id}", model_class=Project)
        
    def create(self, name: str, description: Optional[str] = None, 
               data_flows: Optional[List[Dict[str, int]]] = None) -> Project:
        """
        Create a new project
        
        Args:
            name: Project name (required)
            description: Project description
            data_flows: Initial data flows to add to the project
            
        Returns:
            Created Project object
        """
        project_data = CreateProjectRequest(
            name=name,
            description=description,
            data_flows=data_flows
        ).dict(exclude_none=True)
        
        return self._post("/projects", json=project_data, model_class=Project)
        
    def update(self, project_id: str, name: Optional[str] = None, 
               description: Optional[str] = None, 
               data_flows: Optional[List[Dict[str, int]]] = None) -> Project:
        """
        Update a project
        
        Args:
            project_id: Project ID
            name: New project name
            description: New project description
            data_flows: New data flows for the project
            
        Returns:
            Updated Project object
        """
        project_data = {}
        if name is not None:
            project_data["name"] = name
        if description is not None:
            project_data["description"] = description
        if data_flows is not None:
            project_data["data_flows"] = data_flows
            
        return self._put(f"/projects/{project_id}", json=project_data, model_class=Project)
        
    def delete(self, project_id: str) -> Dict[str, Any]:
        """
        Delete a project
        
        Args:
            project_id: Project ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/projects/{project_id}")
        
    def get_flows(self, project_id: str) -> ProjectFlowResponse:
        """
        Get flows belonging to a project
        
        Args:
            project_id: Project ID
            
        Returns:
            ProjectFlowResponse containing flow nodes and related resources
        """
        return self._get(f"/projects/{project_id}/flows", model_class=ProjectFlowResponse)
        
    def replace_flows(self, project_id: str, flows: List[int]) -> ProjectFlowResponse:
        """
        Replace flows belonging to a project
        
        Args:
            project_id: Project ID
            flows: List of flow IDs to replace existing flows
            
        Returns:
            ProjectFlowResponse containing updated flow nodes
        """
        request = ProjectFlowRequest(flows=flows)
        return self._post(
            f"/projects/{project_id}/flows",
            json=request.dict(),
            model_class=ProjectFlowResponse
        )
        
    def add_flows(self, project_id: str, flows: List[int]) -> ProjectFlowResponse:
        """
        Add flows to a project
        
        Args:
            project_id: Project ID
            flows: List of flow IDs to add to the project
            
        Returns:
            ProjectFlowResponse containing updated flow nodes
        """
        request = ProjectFlowRequest(flows=flows)
        return self._put(
            f"/projects/{project_id}/flows",
            json=request.dict(),
            model_class=ProjectFlowResponse
        )
        
    def remove_flows(self, project_id: str, flows: Optional[List[int]] = None) -> ProjectFlowResponse:
        """
        Remove flows from a project
        
        Args:
            project_id: Project ID
            flows: List of flow IDs to remove. If None, all flows will be removed.
            
        Returns:
            ProjectFlowResponse containing updated flow nodes
        """
        request = {}
        if flows is not None:
            request = ProjectFlowRequest(flows=flows).dict()
            
        return self._delete(
            f"/projects/{project_id}/flows",
            json=request if flows else None,
            model_class=ProjectFlowResponse
        )
        
    # Deprecated methods for backward compatibility
    
    def get_data_flows(self, project_id: str) -> List[DataFlow]:
        """
        Get data flows belonging to a project (deprecated)
        
        Args:
            project_id: Project ID
            
        Returns:
            List of DataFlow objects
        """
        return self._get(f"/projects/{project_id}/data_flows", model_class=List[DataFlow])
        
    def replace_data_flows(self, project_id: str, 
                           data_flows: List[Dict[str, int]]) -> List[DataFlow]:
        """
        Replace data flows belonging to a project (deprecated)
        
        Args:
            project_id: Project ID
            data_flows: List of data flow objects to replace existing flows
            
        Returns:
            List of updated DataFlow objects
        """
        request = ProjectDataFlowRequest(data_flows=data_flows)
        return self._post(
            f"/projects/{project_id}/data_flows",
            json=request.dict(),
            model_class=List[DataFlow]
        )
        
    def add_data_flows(self, project_id: str, 
                       data_flows: List[Dict[str, int]]) -> List[DataFlow]:
        """
        Add data flows to a project (deprecated)
        
        Args:
            project_id: Project ID
            data_flows: List of data flow objects to add to the project
            
        Returns:
            List of updated DataFlow objects
        """
        request = ProjectDataFlowRequest(data_flows=data_flows)
        return self._put(
            f"/projects/{project_id}/data_flows",
            json=request.dict(),
            model_class=List[DataFlow]
        )
        
    def remove_data_flows(self, project_id: str, 
                         data_flows: Optional[List[Dict[str, int]]] = None) -> List[DataFlow]:
        """
        Remove data flows from a project (deprecated)
        
        Args:
            project_id: Project ID
            data_flows: List of data flow objects to remove. If None, all flows will be removed.
            
        Returns:
            List of updated DataFlow objects
        """
        request = {}
        if data_flows is not None:
            request = ProjectDataFlowRequest(data_flows=data_flows).dict()
            
        return self._delete(
            f"/projects/{project_id}/data_flows",
            json=request if data_flows else None,
            model_class=List[DataFlow]
        )
        
    def list_resources(self, project_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        List resources in a project
        
        Args:
            project_id: Project ID
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            Resources in the project
        """
        return self._get(
            f"/projects/{project_id}/resources",
            params={"limit": limit, "offset": offset}
        )
        
    def add_resource(self, project_id: str, resource_type: str, resource_id: str) -> Project:
        """
        Add a resource to a project
        
        Args:
            project_id: Project ID
            resource_type: Resource type (e.g., "flow", "source", "destination")
            resource_id: Resource ID to add
            
        Returns:
            Updated Project object
        """
        return self._post(
            f"/projects/{project_id}/resources",
            json={"resource_type": resource_type, "resource_id": resource_id},
            model_class=Project
        )
        
    def remove_resource(self, project_id: str, resource_type: str, resource_id: str) -> Project:
        """
        Remove a resource from a project
        
        Args:
            project_id: Project ID
            resource_type: Resource type (e.g., "flow", "source", "destination")
            resource_id: Resource ID to remove
            
        Returns:
            Updated Project object
        """
        return self._delete(
            f"/projects/{project_id}/resources/{resource_type}/{resource_id}",
            model_class=Project
        ) 