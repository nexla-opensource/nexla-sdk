"""
Projects API endpoints
"""
from typing import Dict, Any, List, Optional

from .base import BaseAPI
from ..models.projects import Project, ProjectList


class ProjectsAPI(BaseAPI):
    """API client for projects endpoints"""
    
    def list(self, limit: int = 100, offset: int = 0) -> ProjectList:
        """
        List projects
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            ProjectList containing projects
        """
        return self._get("/projects", params={"limit": limit, "offset": offset}, model_class=ProjectList)
        
    def get(self, project_id: str) -> Project:
        """
        Get a project by ID
        
        Args:
            project_id: Project ID
            
        Returns:
            Project object
        """
        return self._get(f"/projects/{project_id}", model_class=Project)
        
    def create(self, project_data: Dict[str, Any]) -> Project:
        """
        Create a new project
        
        Args:
            project_data: Project configuration
            
        Returns:
            Created Project object
        """
        return self._post("/projects", json=project_data, model_class=Project)
        
    def update(self, project_id: str, project_data: Dict[str, Any]) -> Project:
        """
        Update a project
        
        Args:
            project_id: Project ID
            project_data: Project configuration to update
            
        Returns:
            Updated Project object
        """
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