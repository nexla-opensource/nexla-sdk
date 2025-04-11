"""
Code Containers API endpoints
"""
from typing import Dict, Any, List, Optional, Union
from .base import BaseAPI
from ..models.code_containers import CodeContainer, CodeContainerList, CodeContainerContent, CodeType, CodeEncoding, OutputType


class CodeContainersAPI(BaseAPI):
    """API client for code containers endpoints"""
    
    def list(self, limit: int = 100, offset: int = 0) -> CodeContainerList:
        """
        Get all Code Containers
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            CodeContainerList containing code containers
        """
        return self._get("/code_containers", params={"limit": limit, "offset": offset}, model_class=CodeContainerList)
    
    def list_public(self) -> List[CodeContainer]:
        """
        Get all Public Code Containers
        
        The Nexla team regularly adds common code containers that are made available to all Nexla accounts.
        This endpoint fetches all such publicly available code containers.
        
        Returns:
            List of public code containers
        """
        return self._get("/code_containers/public", model_class=List[CodeContainer])
        
    def get(self, container_id: int) -> CodeContainer:
        """
        Get a Code Container by ID
        
        Args:
            container_id: Code Container ID
            
        Returns:
            CodeContainer object
        """
        return self._get(f"/code_containers/{container_id}", model_class=CodeContainer)
        
    def create(self, container_data: Dict[str, Any]) -> CodeContainer:
        """
        Create a new Code Container
        
        Args:
            container_data: Code Container configuration
            
        Returns:
            Created CodeContainer object
        """
        return self._post("/code_containers", json=container_data, model_class=CodeContainer)
        
    def update(self, container_id: int, container_data: Dict[str, Any]) -> CodeContainer:
        """
        Update a Code Container
        
        Args:
            container_id: Code Container ID
            container_data: Code Container configuration to update
            
        Returns:
            Updated CodeContainer object
        """
        return self._put(f"/code_containers/{container_id}", json=container_data, model_class=CodeContainer)
        
    def delete(self, container_id: int) -> Dict[str, Any]:
        """
        Delete a Code Container
        
        Args:
            container_id: Code Container ID
            
        Returns:
            Response with status code and message
        """
        return self._delete(f"/code_containers/{container_id}")
        
    def get_content(self, container_id: int) -> CodeContainerContent:
        """
        Get Code Container content
        
        Args:
            container_id: Code Container ID
            
        Returns:
            CodeContainerContent object with the actual code
        """
        return self._get(f"/code_containers/{container_id}/content", model_class=CodeContainerContent)
        
    def update_content(self, container_id: int, content_data: Dict[str, Any]) -> CodeContainerContent:
        """
        Update Code Container content
        
        Args:
            container_id: Code Container ID
            content_data: Content data to update
            
        Returns:
            Updated CodeContainerContent object
        """
        return self._put(f"/code_containers/{container_id}/content", json=content_data, model_class=CodeContainerContent) 