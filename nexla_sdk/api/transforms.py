"""
Transforms API endpoints
"""
from typing import Dict, Any, List, Optional

from .base import BaseAPI
from ..models.transforms import Transform, TransformList, TransformExpanded


class TransformsAPI(BaseAPI):
    """API client for transforms endpoints"""
    
    def list(self, limit: int = 100, offset: int = 0) -> TransformList:
        """
        List transforms
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            TransformList containing transforms
        """
        return self._get("/transforms", params={"limit": limit, "offset": offset}, model_class=TransformList)
        
    def get(self, transform_id: str, expand: bool = False) -> Transform:
        """
        Get a transform by ID
        
        Args:
            transform_id: Transform ID
            expand: Whether to expand the resource details
            
        Returns:
            Transform object
        """
        path = f"/transforms/{transform_id}"
        if expand:
            path += "?expand=1"
            
        return self._get(path, model_class=Transform if not expand else TransformExpanded)
        
    def create(self, transform_data: Dict[str, Any]) -> Transform:
        """
        Create a new transform
        
        Args:
            transform_data: Transform configuration
            
        Returns:
            Created Transform object
        """
        return self._post("/transforms", json=transform_data, model_class=Transform)
        
    def update(self, transform_id: str, transform_data: Dict[str, Any]) -> Transform:
        """
        Update a transform
        
        Args:
            transform_id: Transform ID
            transform_data: Transform configuration to update
            
        Returns:
            Updated Transform object
        """
        return self._put(f"/transforms/{transform_id}", json=transform_data, model_class=Transform)
        
    def delete(self, transform_id: str) -> Dict[str, Any]:
        """
        Delete a transform
        
        Args:
            transform_id: Transform ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/transforms/{transform_id}")
        
    def copy(self, transform_id: str, new_name: Optional[str] = None) -> Transform:
        """
        Create a copy of a transform
        
        Args:
            transform_id: Transform ID
            new_name: Optional new name for the copied transform
            
        Returns:
            New Transform object
        """
        params = {}
        if new_name:
            params["name"] = new_name
            
        return self._post(f"/transforms/{transform_id}/copy", params=params, model_class=Transform)
        
    def list_attribute_transforms(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        List attribute transforms
        
        Args:
            limit: Number of items to return
            offset: Pagination offset
            
        Returns:
            Dictionary containing attribute transforms
        """
        return self._get("/attribute_transforms", params={"limit": limit, "offset": offset})
        
    def get_attribute_transform(self, transform_id: str) -> Dict[str, Any]:
        """
        Get an attribute transform by ID
        
        Args:
            transform_id: Attribute transform ID
            
        Returns:
            Attribute transform details
        """
        return self._get(f"/attribute_transforms/{transform_id}")
        
    def create_attribute_transform(self, transform_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new attribute transform
        
        Args:
            transform_data: Attribute transform configuration
            
        Returns:
            Created attribute transform details
        """
        return self._post("/attribute_transforms", json=transform_data)
        
    def update_attribute_transform(self, transform_id: str, transform_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an attribute transform
        
        Args:
            transform_id: Attribute transform ID
            transform_data: Attribute transform configuration to update
            
        Returns:
            Updated attribute transform details
        """
        return self._put(f"/attribute_transforms/{transform_id}", json=transform_data)
        
    def delete_attribute_transform(self, transform_id: str) -> Dict[str, Any]:
        """
        Delete an attribute transform
        
        Args:
            transform_id: Attribute transform ID
            
        Returns:
            Empty dictionary on success
        """
        return self._delete(f"/attribute_transforms/{transform_id}") 