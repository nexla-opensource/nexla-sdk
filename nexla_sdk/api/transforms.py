"""
Transforms API endpoints
"""
from typing import Dict, Any, List, Optional, Union
from ..models.transforms import (
    Transform, TransformList, AttributeTransform, AttributeTransformList,
    CreateTransformRequest, UpdateTransformRequest, DeleteTransformResponse,
    CreateAttributeTransformRequest
)
from .base import BaseAPI


class TransformsAPI(BaseAPI):
    """API client for transforms endpoints"""
    
    def list(self, page: int = 1, per_page: int = 100, reusable: Optional[str] = None) -> TransformList:
        """
        Get all Reusable Record Transforms
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            reusable: Filter by reusable status, valid values are: 'all', '1', '0'
                      - 'all': Include both reusable and non-reusable transforms
                      - '1': Include only reusable transforms (default if not specified)
                      - '0': Include only non-reusable transforms
            
        Returns:
            TransformList containing transforms
        """
        params = {"page": page, "per_page": per_page}
        if reusable:
            params["reusable"] = reusable
            
        # Get raw response as a list of transforms
        response = self._get("/transforms", params=params)
        
        # If response is empty, return an empty TransformList
        if not response:
            return TransformList(items=[], total=0, page=page, page_size=per_page)
            
        # Convert the list of transforms to Transform objects
        transforms = [Transform.model_validate(transform) for transform in response]
        
        # Create and return a TransformList with the expected fields
        return TransformList(
            items=transforms,
            total=len(transforms),
            page=page,
            page_size=per_page
        )
    
    def list_public(self) -> List[Transform]:
        """
        Get all Public Reusable Record Transforms
        
        Returns:
            List of public transforms
        """
        response = self._get("/transforms/public")
        
        # If response is empty, return an empty list
        if not response:
            return []
            
        # Convert the list of transforms to Transform objects
        return [Transform.model_validate(transform) for transform in response]
        
    def get(self, transform_id: int) -> Transform:
        """
        Get A Reusable Record Transform by ID
        
        Args:
            transform_id: Transform ID
            
        Returns:
            Transform object
        """
        return self._get(f"/transforms/{transform_id}", model_class=Transform)
        
    def create(self, transform_data: Union[Dict[str, Any], CreateTransformRequest]) -> Transform:
        """
        Create a Reusable Record Transform
        
        Args:
            transform_data: Transform configuration
            
        Returns:
            Created Transform object
        """
        if isinstance(transform_data, CreateTransformRequest):
            transform_data = transform_data.model_dump(exclude_none=True)
        
        return self._post("/transforms", json=transform_data, model_class=Transform)
        
    def update(self, transform_id: int, transform_data: Union[Dict[str, Any], UpdateTransformRequest]) -> Transform:
        """
        Update Reusable Record Transform
        
        Args:
            transform_id: Transform ID
            transform_data: Transform configuration to update
            
        Returns:
            Updated Transform object
        """
        if isinstance(transform_data, UpdateTransformRequest):
            transform_data = transform_data.model_dump(exclude_none=True)
            
        return self._put(f"/transforms/{transform_id}", json=transform_data, model_class=Transform)
        
    def delete(self, transform_id: int) -> DeleteTransformResponse:
        """
        Delete a Reusable Record Transform
        
        Args:
            transform_id: Transform ID
            
        Returns:
            DeleteTransformResponse with status code and message
        """
        response = self._delete(f"/transforms/{transform_id}")
        
        # Convert the response to DeleteTransformResponse
        # If it's an empty dict, create a default response
        if not response or (isinstance(response, dict) and not response):
            return DeleteTransformResponse(code="200", message="Delete successful")
            
        return DeleteTransformResponse.model_validate(response)
        
    def copy(self, transform_id: int) -> Transform:
        """
        Copy a Reusable Record Transform
        
        Args:
            transform_id: Transform ID
            
        Returns:
            New Transform object
        """
        return self._post(f"/transforms/{transform_id}/copy", model_class=Transform)
    
    def list_attribute_transforms(self, page: int = 1, per_page: int = 100) -> List[AttributeTransform]:
        """
        Get all Attribute Transforms
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            
        Returns:
            List of attribute transforms
        """
        # Get raw response as a list of attribute transforms
        response = self._get("/attribute_transforms", params={"page": page, "per_page": per_page})
        
        # If response is empty, return an empty list
        if not response:
            return []
            
        # Convert the list of attribute transforms to AttributeTransform objects
        return [AttributeTransform.model_validate(transform) for transform in response]
    
    def list_public_attribute_transforms(self) -> List[AttributeTransform]:
        """
        Get all Public Attribute Transforms
        
        Returns:
            List of public attribute transforms
        """
        response = self._get("/attribute_transforms/public")
        
        # If response is empty, return an empty list
        if not response:
            return []
            
        # Convert the list of attribute transforms to AttributeTransform objects
        return [AttributeTransform.model_validate(transform) for transform in response]
        
    def get_attribute_transform(self, transform_id: int) -> AttributeTransform:
        """
        Get Attribute Transform by ID
        
        Args:
            transform_id: Attribute transform ID
            
        Returns:
            AttributeTransform object
        """
        return self._get(f"/attribute_transforms/{transform_id}", model_class=AttributeTransform)
        
    def create_attribute_transform(self, transform_data: Union[Dict[str, Any], CreateAttributeTransformRequest]) -> AttributeTransform:
        """
        Create an Attribute Transform
        
        Args:
            transform_data: Attribute transform configuration
            
        Returns:
            Created AttributeTransform object
        """
        if isinstance(transform_data, CreateAttributeTransformRequest):
            transform_data = transform_data.model_dump(exclude_none=True)
            
        return self._post("/attribute_transforms", json=transform_data, model_class=AttributeTransform)
        
    def update_attribute_transform(self, transform_id: int, transform_data: Union[Dict[str, Any], CreateAttributeTransformRequest]) -> AttributeTransform:
        """
        Update Attribute Transform
        
        Args:
            transform_id: Attribute transform ID
            transform_data: Attribute transform configuration to update
            
        Returns:
            Updated AttributeTransform object
        """
        if isinstance(transform_data, CreateAttributeTransformRequest):
            transform_data = transform_data.model_dump(exclude_none=True)
            
        return self._put(f"/attribute_transforms/{transform_id}", json=transform_data, model_class=AttributeTransform)
        
    def delete_attribute_transform(self, transform_id: int) -> DeleteTransformResponse:
        """
        Delete an Attribute Transform
        
        Args:
            transform_id: Attribute transform ID
            
        Returns:
            DeleteTransformResponse with status code and message
        """
        response = self._delete(f"/attribute_transforms/{transform_id}")
        
        # Convert the response to DeleteTransformResponse
        # If it's an empty dict, create a default response
        if not response or (isinstance(response, dict) and not response):
            return DeleteTransformResponse(code="200", message="Delete successful")
            
        return DeleteTransformResponse.model_validate(response) 